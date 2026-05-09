from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

REQUIRED_AGENT_FILES = ("agent.md", "interface.md", "input.schema.json", "output.schema.json")
SUPPORT_DIRS = ("examples", "policies", "templates", "checklists")
SEVERITY = {"info": 0, "warning": 1, "error": 2}
MAX_CODE_LINES = 300
CODE_SUFFIXES = {".py"}
SKIP_PARTS = {".git", ".venv", "__pycache__"}


@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    path: str = ""
    severity: str = "error"


@dataclass(frozen=True)
class AgentSpec:
    name: str
    root: Path


@dataclass(frozen=True)
class Report:
    root: str
    agents: int
    findings: tuple[Finding, ...]

    @property
    def passed(self) -> bool:
        return not any(f.severity == "error" for f in self.findings)

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "agents": self.agents,
            "passed": self.passed,
            "findings": [asdict(f) for f in self.findings],
        }

    def render(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        lines = [f"{status}: {self.agents} agent(s) checked"]
        for finding in self.findings:
            loc = f" [{finding.path}]" if finding.path else ""
            lines.append(f"- {finding.severity.upper()} {finding.code}{loc}: {finding.message}")
        return "\n".join(lines)


def run(root: str | Path = ".") -> Report:
    root = Path(root).resolve()
    findings: list[Finding] = []
    agents = discover_agents(root, findings)
    for agent in agents:
        findings.extend(check_agent(agent))
    findings.extend(check_code_line_budget(root))
    return Report(str(root), len(agents), tuple(findings))


def discover_agents(root: Path, findings: list[Finding] | None = None) -> list[AgentSpec]:
    agents_dir = root / ".harness" / "agents"
    if not agents_dir.is_dir():
        if findings is not None:
            findings.append(Finding("missing_agents_dir", "Expected .harness/agents directory", str(agents_dir)))
        return []
    agents = [AgentSpec(path.name, path) for path in sorted(agents_dir.iterdir()) if path.is_dir()]
    if not agents and findings is not None:
        findings.append(Finding("no_agents", "No agent directories found", str(agents_dir)))
    return agents


def check_agent(agent: AgentSpec) -> list[Finding]:
    findings: list[Finding] = []
    for name in REQUIRED_AGENT_FILES:
        if not (agent.root / name).is_file():
            findings.append(Finding("missing_required_file", f"{agent.name} lacks {name}", rel(agent.root / name)))
    for name in SUPPORT_DIRS:
        if not (agent.root / name).is_dir():
            findings.append(Finding("missing_support_dir", f"{agent.name} lacks {name}/", rel(agent.root / name), "warning"))
    input_schema = load_json(agent.root / "input.schema.json", findings)
    output_schema = load_json(agent.root / "output.schema.json", findings)
    for label, schema in (("input", input_schema), ("output", output_schema)):
        if isinstance(schema, dict):
            findings.extend(check_schema_shape(schema, agent.root / f"{label}.schema.json"))
    if (agent.root / "interface.md").is_file():
        findings.extend(check_interface(agent.root / "interface.md"))
    if isinstance(input_schema, dict) and isinstance(output_schema, dict):
        findings.extend(check_examples(agent, input_schema, output_schema))
    return findings


def load_json(path: Path, findings: list[Finding]) -> Any | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        findings.append(Finding("invalid_json", str(exc), rel(path)))
        return None


def check_schema_shape(schema: dict[str, Any], path: Path) -> list[Finding]:
    findings: list[Finding] = []
    if schema.get("type") != "object":
        findings.append(Finding("schema_root_not_object", "Root schema should describe an object", rel(path)))
    props = schema.get("properties", {})
    if not isinstance(props, dict):
        findings.append(Finding("schema_properties_invalid", "properties must be an object", rel(path)))
        props = {}
    for name in schema.get("required", []):
        if name not in props:
            findings.append(Finding("schema_required_unknown", f"required field {name!r} is not in properties", rel(path)))
    return findings


def check_interface(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    findings: list[Finding] = []
    for heading in ("## Purpose", "## Consumes", "## Produces", "## Must Not Do"):
        if heading not in text:
            findings.append(Finding("interface_section_missing", f"Missing {heading}", rel(path), "warning"))
    return findings


def check_examples(agent: AgentSpec, input_schema: dict[str, Any], output_schema: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    examples = sorted((agent.root / "examples").glob("*.json"))
    if not examples:
        return [Finding("missing_examples", f"{agent.name} has no JSON examples", rel(agent.root / "examples"), "warning")]
    for path in examples:
        data = load_json(path, findings)
        if data is None:
            continue
        schema = output_schema if "output" in path.name else input_schema if "request" in path.name else None
        if schema is None:
            findings.append(Finding("unclassified_example", "Example name should include request or output", rel(path), "warning"))
            continue
        for err in validate_json(data, schema):
            findings.append(Finding("example_schema_mismatch", err, rel(path)))
    return findings


def check_code_line_budget(root: Path, max_lines: int = MAX_CODE_LINES) -> list[Finding]:
    findings = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in CODE_SUFFIXES or SKIP_PARTS & set(path.parts):
            continue
        lines = len(path.read_text(encoding="utf-8").splitlines())
        if lines > max_lines:
            findings.append(
                Finding(
                    "code_line_budget_exceeded",
                    f"Code file has {lines} lines; limit is {max_lines}",
                    rel(path),
                )
            )
    return findings


def validate_json(data: Any, schema: dict[str, Any]) -> list[str]:
    return list(_validate(data, schema, "$", schema))


def _validate(data: Any, schema: dict[str, Any], where: str, root: dict[str, Any]) -> list[str]:
    if "$ref" in schema:
        schema = _resolve_ref(root, schema["$ref"])
    errors: list[str] = []
    expected = schema.get("type")
    if expected is not None and not _type_ok(data, expected):
        return [f"{where}: expected {expected}, got {type(data).__name__}"]
    if "enum" in schema and data not in schema["enum"]:
        errors.append(f"{where}: {data!r} is not one of {schema['enum']!r}")
    if isinstance(data, str) and data == "" and schema.get("minLength", 0) > 0:
        errors.append(f"{where}: string is shorter than {schema['minLength']}")
    if isinstance(data, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in data:
                errors.append(f"{where}.{key}: missing required property")
        for key, value in data.items():
            if key in props:
                errors.extend(_validate(value, props[key], f"{where}.{key}", root))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{where}.{key}: additional property is not allowed")
            elif isinstance(schema.get("additionalProperties"), dict):
                errors.extend(_validate(value, schema["additionalProperties"], f"{where}.{key}", root))
    if isinstance(data, list) and isinstance(schema.get("items"), dict):
        for index, item in enumerate(data):
            errors.extend(_validate(item, schema["items"], f"{where}[{index}]", root))
    return errors


def _resolve_ref(root: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"Only local JSON schema refs are supported: {ref}")
    node: Any = root
    for part in ref[2:].split("/"):
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node


def _type_ok(data: Any, expected: str | list[str]) -> bool:
    return any(_one_type_ok(data, item) for item in (expected if isinstance(expected, list) else [expected]))


def _one_type_ok(data: Any, expected: str) -> bool:
    checks = {
        "object": lambda x: isinstance(x, dict),
        "array": lambda x: isinstance(x, list),
        "string": lambda x: isinstance(x, str),
        "integer": lambda x: isinstance(x, int) and not isinstance(x, bool),
        "number": lambda x: (isinstance(x, int | float) and not isinstance(x, bool)),
        "boolean": lambda x: isinstance(x, bool),
        "null": lambda x: x is None,
    }
    return checks.get(expected, lambda _x: True)(data)


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)

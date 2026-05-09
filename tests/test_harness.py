from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from harness import run, validate_json


ROOT = Path(__file__).resolve().parents[1]


class SchemaTests(unittest.TestCase):
    def test_validator_catches_required_extra_enum_and_type_errors(self) -> None:
        schema = {
            "type": "object",
            "required": ["name", "status"],
            "additionalProperties": False,
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "status": {"type": "string", "enum": ["ok"]},
                "count": {"type": ["integer", "null"]},
            },
        }
        self.assertEqual(validate_json({"name": "agent", "status": "ok", "count": None}, schema), [])
        errors = validate_json({"name": "", "status": "bad", "extra": True}, schema)
        self.assertTrue(any("string is shorter" in err for err in errors))
        self.assertTrue(any("not one of" in err for err in errors))
        self.assertTrue(any("additional property" in err for err in errors))
        errors = validate_json({"name": "agent"}, schema)
        self.assertTrue(any("missing required property" in err for err in errors))

    def test_validator_resolves_local_refs(self) -> None:
        schema = {
            "type": "object",
            "properties": {"items": {"type": "array", "items": {"$ref": "#/$defs/item"}}},
            "$defs": {"item": {"type": "object", "required": ["id"], "properties": {"id": {"type": "string"}}}},
        }
        self.assertEqual(validate_json({"items": [{"id": "a"}]}, schema), [])
        self.assertTrue(validate_json({"items": [{}]}, schema))


class HarnessTests(unittest.TestCase):
    def make_agent(self, root: Path, name: str = "demo_agent") -> Path:
        agent = root / ".harness" / "agents" / name
        (agent / "examples").mkdir(parents=True)
        for dirname in ("policies", "templates", "checklists"):
            (agent / dirname).mkdir()
        (agent / "agent.md").write_text("# demo_agent\n", encoding="utf-8")
        (agent / "interface.md").write_text(
            "## Purpose\nx\n## Consumes\nx\n## Produces\nx\n## Must Not Do\nx\n",
            encoding="utf-8",
        )
        schema = {
            "type": "object",
            "required": ["status"],
            "additionalProperties": False,
            "properties": {"status": {"type": "string", "enum": ["ok"]}},
        }
        for filename in ("input.schema.json", "output.schema.json"):
            (agent / filename).write_text(json.dumps(schema), encoding="utf-8")
        for filename in ("demo_request.example.json", "demo_output.example.json"):
            (agent / "examples" / filename).write_text('{"status": "ok"}', encoding="utf-8")
        return agent

    def test_minimal_agent_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.make_agent(Path(tmp))
            self.assertTrue(run(tmp).passed)

    def test_code_line_budget_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_agent(root)
            (root / "long_file.py").write_text("\n".join("x = 1" for _ in range(301)), encoding="utf-8")
            report = run(root)
            self.assertFalse(report.passed)
            self.assertIn("code_line_budget_exceeded", {finding.code for finding in report.findings})

    def test_bad_agent_reports_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            agent = Path(tmp) / ".harness" / "agents" / "bad_agent"
            (agent / "examples").mkdir(parents=True)
            (agent / "agent.md").write_text("# bad_agent\n", encoding="utf-8")
            (agent / "interface.md").write_text("## Purpose\nx\n", encoding="utf-8")
            schema = {"type": "object", "required": ["status"], "properties": {"status": {"type": "string"}}}
            (agent / "input.schema.json").write_text(json.dumps(schema), encoding="utf-8")
            (agent / "output.schema.json").write_text(json.dumps(schema), encoding="utf-8")
            (agent / "examples" / "bad_output.example.json").write_text("{}", encoding="utf-8")
            report = run(tmp)
            self.assertFalse(report.passed)
            self.assertIn("example_schema_mismatch", {finding.code for finding in report.findings})

    def test_current_agent_contracts_are_valid(self) -> None:
        report = run(ROOT)
        errors = [finding for finding in report.findings if finding.severity == "error"]
        self.assertEqual(errors, [])

    def test_cli_json_report(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "harness", str(ROOT), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout)["passed"])


if __name__ == "__main__":
    unittest.main()

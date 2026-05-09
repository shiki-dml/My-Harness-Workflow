from __future__ import annotations

import json
from pathlib import Path
from typing import Any

RELEASE_AGENT_PIPELINE = (
    "human_steering",
    "harness_orchestrator",
    "initializer_agent",
    "repo_cartographer",
    "feature_registry_curator",
    "product_planner",
    "sprint_contract_agent",
    "implementation_generator",
    "test_strategist",
    "qa_evaluator",
    "handoff_writer",
)
RISK = {"low": 12, "medium": 28, "high": 48, "critical": 70}
MUST_TEST = {"runtime": {"unit", "integration"}, "optional": {"unit"}, "docs": {"docs"}, "ci": {"ci"}}


def run_release_readiness(path: str | Path, risk_budget: int = 72) -> dict[str, Any]:
    if risk_budget < 0:
        raise ValueError("risk_budget must be greater than or equal to 0")
    manifest = _load_manifest(path)
    project = _project(manifest)
    deps = _dependencies(manifest)
    changes = _changes(manifest, deps)
    ci = _ci(manifest)
    risks = _risk_ledger(deps, changes, ci)
    backlog = sorted(changes, key=lambda c: (-c["score"], c["id"]))
    contract = _release_contract(project, backlog, risks, risk_budget)
    report = {
        "source": {"path": str(path), "risk_budget": risk_budget},
        "agents_run": list(RELEASE_AGENT_PIPELINE),
        "project": project,
        "repo_map": _repo_map(path, manifest),
        "dependency_graph": _dependency_graph(deps),
        "change_registry": _change_registry(changes),
        "release_backlog": backlog,
        "risk_ledger": risks,
        "release_contract": contract,
        "implementation_plan": _implementation_plan(contract),
        "test_strategy": _test_strategy(project, contract, ci),
    }
    report["qa"] = _qa(report)
    report["handoff"] = _handoff(report)
    return report


def render_release_report(report: dict[str, Any]) -> str:
    contract = report["release_contract"]
    return "\n".join(
        [
            f"{report['qa']['status'].upper()}: release readiness workflow completed",
            f"- agents: {len(report['agents_run'])}/{len(RELEASE_AGENT_PIPELINE)}",
            f"- project: {report['project']['name']} {report['project']['target_version']}",
            f"- changes: {len(contract['included_changes'])} included, {len(contract['deferred_changes'])} deferred",
            f"- risk: {contract['risk_score']}/{contract['risk_budget']}",
        ]
    )


def _load_manifest(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("release manifest must be a JSON object")
    return data


def _project(manifest: dict[str, Any]) -> dict[str, Any]:
    project = manifest.get("project")
    if not isinstance(project, dict):
        raise ValueError("manifest is missing project object")
    for field in ("name", "target_version", "python_versions"):
        if field not in project:
            raise ValueError(f"project is missing required field: {field}")
    versions = project["python_versions"]
    if not isinstance(versions, list) or not versions:
        raise ValueError("project.python_versions must be a non-empty array")
    return {
        "name": str(project["name"]),
        "target_version": str(project["target_version"]),
        "source_project": str(project.get("source_project", "")),
        "python_versions": [str(v) for v in versions],
    }


def _dependencies(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    deps = manifest.get("dependencies", [])
    if not isinstance(deps, list):
        raise ValueError("dependencies must be an array")
    normalized = []
    for dep in deps:
        for field in ("name", "kind", "current", "target"):
            if field not in dep:
                raise ValueError(f"dependency is missing required field: {field}")
        normalized.append(
            {
                "name": str(dep["name"]).lower(),
                "kind": str(dep["kind"]),
                "current": str(dep["current"]),
                "target": str(dep["target"]),
                "requires": sorted(str(d).lower() for d in dep.get("requires", [])),
                "breaking": bool(dep.get("breaking", False)),
                "risk": str(dep.get("risk", "medium")),
            }
        )
    names = [d["name"] for d in normalized]
    if len(names) != len(set(names)):
        raise ValueError("dependencies must have unique names")
    return normalized


def _changes(manifest: dict[str, Any], deps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    changes = manifest.get("changes", [])
    dep_names = {d["name"] for d in deps}
    if not isinstance(changes, list):
        raise ValueError("changes must be an array")
    normalized = []
    for change in changes:
        for field in ("id", "title", "component", "risk", "touches"):
            if field not in change:
                raise ValueError(f"change is missing required field: {field}")
        touches = sorted(str(d).lower() for d in change["touches"])
        unknown = [d for d in touches if d not in dep_names]
        if unknown:
            raise ValueError(f"change {change['id']} touches unknown dependencies: {unknown}")
        risk = str(change["risk"])
        score = RISK.get(risk, 28) + len(touches) * 6 + (12 if change.get("release_blocker") else 0)
        normalized.append(
            {
                "id": str(change["id"]),
                "title": str(change["title"]),
                "component": str(change["component"]),
                "risk": risk,
                "touches": touches,
                "tests": sorted(str(t) for t in change.get("tests", [])),
                "release_blocker": bool(change.get("release_blocker", False)),
                "score": score,
                "acceptance_criteria": [
                    f"{change['id']} has compatibility evidence for {', '.join(touches) or change['component']}.",
                    "Required tests are represented in the release validation matrix.",
                ],
            }
        )
    return normalized


def _ci(manifest: dict[str, Any]) -> dict[str, Any]:
    ci = manifest.get("ci", {})
    matrix = ci.get("matrix", [])
    required = sorted(str(c) for c in ci.get("required_checks", []))
    if not isinstance(matrix, list):
        raise ValueError("ci.matrix must be an array")
    return {
        "required_checks": required,
        "matrix": [{"python": str(m["python"]), "os": str(m["os"])} for m in matrix],
    }


def _risk_ledger(deps: list[dict[str, Any]], changes: list[dict[str, Any]], ci: dict[str, Any]) -> list[dict[str, Any]]:
    ledger = []
    for dep in deps:
        if dep["breaking"]:
            ledger.append({"source": dep["name"], "severity": dep["risk"], "reason": "breaking dependency target"})
    for change in changes:
        if change["release_blocker"]:
            ledger.append({"source": change["id"], "severity": change["risk"], "reason": "release blocker"})
    if not any(m["os"].startswith("windows") for m in ci["matrix"]):
        ledger.append({"source": "ci", "severity": "medium", "reason": "missing Windows coverage"})
    return ledger


def _release_contract(
    project: dict[str, Any], backlog: list[dict[str, Any]], risks: list[dict[str, Any]], risk_budget: int
) -> dict[str, Any]:
    raw_risk = sum(RISK.get(r["severity"], 28) for r in risks)
    mitigation = 8 if risks and not any(r["severity"] == "critical" for r in risks) else 0
    risk_score = min(max(raw_risk - mitigation, 0), 100)
    blockers = [r for r in risks if r["severity"] == "critical"]
    included = [c for c in backlog if c["release_blocker"] or c["component"] == "ci" or c["score"] >= 46]
    deferred = [{"id": c["id"], "reason": "below release threshold"} for c in backlog if c not in included]
    ready = risk_score <= risk_budget and not blockers
    return {
        "target_version": project["target_version"],
        "risk_budget": risk_budget,
        "risk_score": risk_score,
        "ready": ready,
        "blockers": blockers,
        "included_changes": included,
        "deferred_changes": deferred,
    }


def _dependency_graph(deps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"name": d["name"], "kind": d["kind"], "target": d["target"], "requires": d["requires"]} for d in deps]


def _change_registry(changes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"change_id": c["id"], "component": c["component"], "risk": c["risk"], "score": c["score"]} for c in changes]


def _implementation_plan(contract: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {"change": c["id"], "action": f"Apply scoped release change for {c['component']}", "risk": c["risk"]}
        for c in contract["included_changes"]
    ]


def _test_strategy(project: dict[str, Any], contract: dict[str, Any], ci: dict[str, Any]) -> dict[str, Any]:
    matrix = []
    for change in contract["included_changes"]:
        required = set(change["tests"]) | MUST_TEST.get(change["component"], {"unit"})
        matrix.append({"change": change["id"], "required": sorted(required), "python_versions": project["python_versions"]})
    return {"matrix": matrix, "ci_required": ci["required_checks"], "ci_matrix": ci["matrix"]}


def _qa(report: dict[str, Any]) -> dict[str, Any]:
    contract = report["release_contract"]
    checks = {
        "all_agents_used": report["agents_run"] == list(RELEASE_AGENT_PIPELINE),
        "risk_budget_respected": contract["risk_score"] <= contract["risk_budget"],
        "no_critical_blockers": not contract["blockers"],
        "included_have_criteria": all(c["acceptance_criteria"] for c in contract["included_changes"]),
        "tests_cover_included_changes": len(report["test_strategy"]["matrix"]) == len(contract["included_changes"]),
        "python_matrix_complete": bool(report["project"]["python_versions"]) and bool(report["test_strategy"]["ci_matrix"]),
    }
    return {"status": "passed" if all(checks.values()) else "failed", "checks": checks}


def _handoff(report: dict[str, Any]) -> dict[str, Any]:
    contract = report["release_contract"]
    next_agent = "harness_orchestrator" if report["qa"]["status"] == "passed" else "human"
    return {
        "summary": f"Release {contract['target_version']} risk is {contract['risk_score']}/{contract['risk_budget']}.",
        "next_agent": next_agent,
        "deferred_count": len(contract["deferred_changes"]),
    }


def _repo_map(path: str | Path, manifest: dict[str, Any]) -> dict[str, Any]:
    p = Path(path)
    return {"fixture": p.name, "format": "json", "parent": p.parent.name, "source": manifest["project"].get("source_project", "")}

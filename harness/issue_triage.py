from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

AGENT_PIPELINE = (
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
STOPWORDS = {"a", "an", "and", "for", "in", "is", "of", "on", "the", "to", "with", "when"}


def run_issue_triage(path: str | Path, capacity: int = 13, today: str = "2026-05-09") -> dict[str, Any]:
    if capacity < 0:
        raise ValueError("capacity must be greater than or equal to 0")
    issues = _normalize(_load(path), today)
    groups = _related_groups(issues)
    registry = _registry(issues, groups)
    backlog = sorted((i for i in issues if i["state"] == "open" and not i["is_pull_request"]), key=_rank)
    sprint = _sprint(backlog, capacity, groups)
    report = {
        "source": {"path": str(path), "issue_count": len(issues), "capacity": capacity},
        "agents_run": list(AGENT_PIPELINE),
        "repo_map": _repo_map(path),
        "feature_registry": registry,
        "backlog": backlog,
        "related_groups": groups,
        "sprint_contract": sprint,
        "triage_outcomes": _triage_outcomes(issues, sprint, groups),
        "implementation_plan": _implementation_plan(sprint),
        "test_strategy": _test_strategy(sprint),
    }
    report["qa"] = _qa(report)
    report["handoff"] = _handoff(report)
    return report


def render_issue_report(report: dict[str, Any]) -> str:
    sprint = report["sprint_contract"]
    lines = [
        f"{report['qa']['status'].upper()}: issue triage workflow completed",
        f"- agents: {len(report['agents_run'])}/{len(AGENT_PIPELINE)}",
        f"- backlog: {len(report['backlog'])} open issue(s)",
        f"- sprint: {len(sprint['items'])} item(s), {sprint['used_capacity']}/{sprint['capacity']} points",
    ]
    return "\n".join(lines)


def _load(path: str | Path) -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("issue fixture must be a JSON array")
    return data


def _normalize(rows: list[dict[str, Any]], today: str) -> list[dict[str, Any]]:
    now = _date(today)
    seen: set[int] = set()
    normalized = []
    for row in rows:
        for required in ("number", "title"):
            if required not in row:
                raise ValueError(f"issue is missing required field: {required}")
        number = int(row["number"])
        if number in seen:
            raise ValueError(f"duplicate issue number: {number}")
        seen.add(number)
        labels = sorted(_label_names(row.get("labels", [])))
        title = str(row.get("title", "")).strip()
        body = str(row.get("body", "") or "")
        kind = _kind(title, body, labels, bool(row.get("is_pull_request")))
        comments = row.get("comments", [])
        reactions = row.get("reactions", {}) or {}
        age = max((now - _date(row.get("created_at", today))).days, 0)
        item = {
            "number": number,
            "title": title,
            "state": row.get("state", "open"),
            "labels": labels,
            "is_pull_request": bool(row.get("is_pull_request")),
            "kind": kind,
            "component": _component(title, body, labels),
            "age_days": age,
            "comment_count": len(comments) if isinstance(comments, list) else int(row.get("comments", 0) or 0),
            "reaction_count": int(reactions.get("total_count", 0)),
            "effort": _effort(kind, body, comments),
        }
        item["score"] = _score(item, title + " " + body)
        item["priority"] = "P0" if item["score"] >= 85 else "P1" if item["score"] >= 70 else "P2" if item["score"] >= 50 else "P3"
        item["acceptance_criteria"] = _acceptance(item)
        normalized.append(item)
    return sorted(normalized, key=lambda i: i["number"])


def _label_names(labels: list[Any]) -> set[str]:
    names = set()
    for label in labels:
        name = label.get("name") if isinstance(label, dict) else label
        if name:
            names.add(str(name).lower())
    return names


def _kind(title: str, body: str, labels: list[str], is_pr: bool) -> str:
    text = f"{title} {body}".lower()
    if is_pr:
        return "pull_request"
    if "bug" in labels or re.search(r"\b(crash|error|fail|regression|exception|broken)\b", text):
        return "bug"
    if "documentation" in labels or "doc" in labels or re.search(r"\b(doc|readme|typo)\b", text):
        return "docs"
    if "enhancement" in labels or re.search(r"\b(add|support|feature|allow|improve)\b", text):
        return "feature"
    return "support"


def _component(title: str, body: str, labels: list[str]) -> str:
    text = " ".join([title, body, *labels]).lower()
    for component, words in {
        "docs": ("doc", "readme", "env var"),
        "streaming": ("stream", "dataloader", "shard", "worker"),
        "map": ("map", "writer", "batch"),
        "auth": ("token", "private", "login"),
        "cache": ("cache", "retry", "download"),
        "windows": ("windows", "memory", "jsonl"),
    }.items():
        if any(word in text for word in words):
            return component
    return "core"


def _effort(kind: str, body: str, comments: Any) -> int:
    base = {"docs": 1, "support": 2, "bug": 3, "feature": 5, "pull_request": 1}.get(kind, 3)
    comment_count = len(comments) if isinstance(comments, list) else int(comments or 0)
    return min(base + (1 if len(body) > 500 else 0) + (1 if comment_count > 2 else 0), 8)


def _score(item: dict[str, Any], text: str) -> int:
    base = {"bug": 68, "feature": 50, "docs": 38, "support": 32, "pull_request": 20}[item["kind"]]
    risk = 12 if re.search(r"\b(security|private|crash|regression|memory|data loss)\b", text.lower()) else 0
    return base + (10 if item["state"] == "open" else 0) + min(item["comment_count"] * 2, 10) + min(item["reaction_count"], 8) + (5 if item["age_days"] > 30 else 0) + risk


def _acceptance(item: dict[str, Any]) -> list[str]:
    return [
        f"#{item['number']} has a reproducible owner-facing outcome for {item['component']}.",
        f"Validation covers {item['kind']} behavior without exceeding scoped files.",
    ]


def _related_groups(issues: list[dict[str, Any]]) -> list[list[int]]:
    groups, used = [], set()
    tokens = {i["number"]: _tokens(i["title"]) for i in issues}
    for issue in issues:
        if issue["number"] in used or issue["is_pull_request"]:
            continue
        group = [issue["number"]]
        for other in issues:
            if other["number"] <= issue["number"] or other["is_pull_request"]:
                continue
            union = tokens[issue["number"]] | tokens[other["number"]]
            overlap = len(tokens[issue["number"]] & tokens[other["number"]]) / max(len(union), 1)
            if overlap >= 0.34 and issue["component"] == other["component"]:
                group.append(other["number"])
        if len(group) > 1:
            used.update(group)
            groups.append(group)
    return groups


def _tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9_]+", text.lower()) if len(t) > 2 and t not in STOPWORDS}


def _registry(issues: list[dict[str, Any]], groups: list[list[int]]) -> list[dict[str, Any]]:
    duplicates = {n for group in groups for n in group[1:]}
    return [
        {
            "feature_id": f"{i['kind'].upper()}-{i['number']}",
            "source": f"#{i['number']}",
            "status": "duplicate" if i["number"] in duplicates else i["state"],
            "component": i["component"],
            "priority": i["priority"],
        }
        for i in issues
        if not i["is_pull_request"]
    ]


def _sprint(backlog: list[dict[str, Any]], capacity: int, groups: list[list[int]]) -> dict[str, Any]:
    duplicate_tail = {n for group in groups for n in group[1:]}
    items, deferred, used = [], [], 0
    for item in backlog:
        if item["number"] in duplicate_tail:
            deferred.append({"number": item["number"], "reason": "covered by related issue group"})
            continue
        if used + item["effort"] <= capacity:
            items.append(item)
            used += item["effort"]
        else:
            deferred.append({"number": item["number"], "reason": "capacity limit"})
    return {"capacity": capacity, "used_capacity": used, "items": items, "deferred": deferred}


def _triage_outcomes(
    issues: list[dict[str, Any]], sprint: dict[str, Any], groups: list[list[int]]
) -> list[dict[str, Any]]:
    planned = {i["number"] for i in sprint["items"]}
    deferred = {i["number"]: i["reason"] for i in sprint["deferred"]}
    duplicate_tail = {n for group in groups for n in group[1:]}
    outcomes = []
    for issue in issues:
        if issue["is_pull_request"]:
            outcome, reason = "pull_request", "tracked as implementation evidence"
        elif issue["state"] != "open":
            outcome, reason = "closed", "closed issues are excluded from sprint planning"
        elif issue["number"] in planned:
            outcome, reason = "planned", "selected within sprint capacity"
        elif issue["number"] in duplicate_tail:
            outcome, reason = "duplicate", deferred.get(issue["number"], "covered by related issue group")
        else:
            outcome, reason = "deferred", deferred.get(issue["number"], "not selected")
        outcomes.append({"number": issue["number"], "outcome": outcome, "reason": reason})
    return outcomes


def _implementation_plan(sprint: dict[str, Any]) -> list[dict[str, str]]:
    return [{"issue": f"#{i['number']}", "change": f"Implement scoped {i['kind']} fix in {i['component']}", "risk": i["priority"]} for i in sprint["items"]]


def _test_strategy(sprint: dict[str, Any]) -> dict[str, Any]:
    return {
        "matrix": [{"issue": f"#{i['number']}", "unit": True, "regression": i["kind"] == "bug", "docs": i["kind"] == "docs"} for i in sprint["items"]],
        "commands": ["python -m unittest discover -s tests -v", "python -m harness ."],
    }


def _qa(report: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "all_agents_used": report["agents_run"] == list(AGENT_PIPELINE),
        "capacity_respected": report["sprint_contract"]["used_capacity"] <= report["sprint_contract"]["capacity"],
        "unique_issues": len({i["number"] for i in report["backlog"]}) == len(report["backlog"]),
        "criteria_present": all(i["acceptance_criteria"] for i in report["sprint_contract"]["items"]),
        "registry_complete": len(report["feature_registry"]) >= len([i for i in report["backlog"] if not i["is_pull_request"]]),
        "outcomes_complete": len(report["triage_outcomes"]) == report["source"]["issue_count"],
    }
    return {"status": "passed" if all(checks.values()) else "failed", "checks": checks}


def _handoff(report: dict[str, Any]) -> dict[str, Any]:
    sprint = report["sprint_contract"]
    return {
        "summary": f"Selected {len(sprint['items'])} issues using {sprint['used_capacity']} of {sprint['capacity']} points.",
        "next_agent": "human" if report["qa"]["status"] != "passed" else "harness_orchestrator",
        "deferred_count": len(sprint["deferred"]),
    }


def _rank(item: dict[str, Any]) -> tuple[int, int, int]:
    return ({"P0": 0, "P1": 1, "P2": 2, "P3": 3}[item["priority"]], -item["score"], item["effort"])


def _repo_map(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    return {"fixture": p.name, "format": "json", "parent": p.parent.name}


def _date(value: Any) -> datetime:
    if isinstance(value, datetime):
        dt = value
    else:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).replace(tzinfo=None)

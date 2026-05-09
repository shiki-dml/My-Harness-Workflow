from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

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


def load_json_file(path: str | Path, expected_type: type, label: str) -> Any:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, expected_type):
        raise ValueError(f"{label} must be a JSON {expected_type.__name__}")
    return data


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def require_fields(row: dict[str, Any], fields: Iterable[str], label: str) -> None:
    for field in fields:
        if field not in row:
            raise ValueError(f"{label} is missing required field: {field}")


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    return value


def ensure_non_negative(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} must be greater than or equal to 0")


def status(checks: dict[str, bool]) -> str:
    return "passed" if all(checks.values()) else "failed"


def render_status(status_text: str, title: str, facts: Iterable[str]) -> str:
    return "\n".join([f"{status_text.upper()}: {title}", *[f"- {fact}" for fact in facts]])

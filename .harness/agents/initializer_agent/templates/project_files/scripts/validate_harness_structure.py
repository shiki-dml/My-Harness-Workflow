#!/usr/bin/env python3
"""Validate the minimal initialized harness scaffold.

This script is read-only. It uses only the Python standard library and does not
install dependencies, call the network, modify files, or delete files.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys


EXPECTED_PATHS = [
    "AGENTS.md",
    "PROGRESS.md",
    "feature_registry.json",
    "docs/project_overview.md",
    "docs/workflow_overview.md",
    "docs/approval_policy.md",
    ".harness/agents/human_steering",
    ".harness/agents/harness_orchestrator",
    ".harness/agents/initializer_agent",
]


def main() -> int:
    root = Path.cwd()
    missing = [path for path in EXPECTED_PATHS if not (root / path).exists()]

    json_errors = []
    registry_path = root / "feature_registry.json"
    if registry_path.exists():
        try:
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            json_errors.append(f"feature_registry.json is not valid JSON: {exc}")
        else:
            if registry.get("features") != []:
                json_errors.append("feature_registry.json must start with an empty features array")

    if missing:
        print("Missing expected scaffold paths:")
        for path in missing:
            print(f"- {path}")

    if json_errors:
        print("JSON validation errors:")
        for error in json_errors:
            print(f"- {error}")

    if missing or json_errors:
        return 1

    print("Harness scaffold validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

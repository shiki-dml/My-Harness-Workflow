from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import run
from .issue_triage import render_issue_report, run_issue_triage
from .release_readiness import render_release_report, run_release_readiness


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["issue-triage"]:
        return issue_triage_main(argv[1:])
    if argv[:1] == ["release-readiness"]:
        return release_readiness_main(argv[1:])

    parser = argparse.ArgumentParser(description="Validate a contract-driven agent harness.")
    parser.add_argument("root", nargs="?", default=".", help="Project root containing .harness/agents")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable report")
    args = parser.parse_args(argv)

    report = run(Path(args.root))
    return _finish(report.to_dict(), report.render(), report.passed, args.json)


def issue_triage_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run the all-agent issue triage sample workflow.")
    parser.add_argument("issues", help="JSON file containing GitHub-like issues")
    parser.add_argument("--capacity", type=int, default=13, help="Sprint point capacity")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable report")
    args = parser.parse_args(argv)

    report = run_issue_triage(Path(args.issues), capacity=args.capacity)
    return _finish(report, render_issue_report(report), report["qa"]["status"] == "passed", args.json)


def release_readiness_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run the all-agent release readiness sample workflow.")
    parser.add_argument("manifest", help="JSON file containing a release readiness manifest")
    parser.add_argument("--risk-budget", type=int, default=72, help="Maximum accepted release risk score")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable report")
    args = parser.parse_args(argv)

    report = run_release_readiness(Path(args.manifest), risk_budget=args.risk_budget)
    return _finish(report, render_release_report(report), report["qa"]["status"] == "passed", args.json)


def _finish(payload: dict, text: str, passed: bool, as_json: bool) -> int:
    print(json.dumps(payload, indent=2, ensure_ascii=False) if as_json else text)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())

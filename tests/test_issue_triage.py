from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from harness import AGENT_PIPELINE, run_issue_triage

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "issue_triage" / "issues.json"


class IssueTriageTests(unittest.TestCase):
    def test_workflow_runs_every_existing_agent(self) -> None:
        report = run_issue_triage(FIXTURE, capacity=13)
        self.assertEqual(report["agents_run"], list(AGENT_PIPELINE))
        self.assertEqual(len(report["agents_run"]), 11)
        self.assertEqual(report["qa"]["status"], "passed")

    def test_scoring_prioritizes_bugs_and_security_relevant_items(self) -> None:
        report = run_issue_triage(FIXTURE, capacity=13)
        top = report["backlog"][0]
        self.assertEqual(top["number"], 7965)
        self.assertEqual(top["priority"], "P0")
        self.assertEqual(top["kind"], "bug")

    def test_related_issue_detection_defers_duplicate_tail(self) -> None:
        report = run_issue_triage(FIXTURE, capacity=20)
        self.assertIn([7988, 7990], report["related_groups"])
        deferred = {item["number"]: item["reason"] for item in report["sprint_contract"]["deferred"]}
        self.assertEqual(deferred[7990], "covered by related issue group")

    def test_sprint_respects_capacity_and_keeps_acceptance_criteria(self) -> None:
        report = run_issue_triage(FIXTURE, capacity=9)
        sprint = report["sprint_contract"]
        self.assertLessEqual(sprint["used_capacity"], 9)
        self.assertTrue(sprint["deferred"])
        self.assertTrue(all(item["acceptance_criteria"] for item in sprint["items"]))

    def test_closed_issues_and_pull_requests_do_not_enter_backlog(self) -> None:
        report = run_issue_triage(FIXTURE, capacity=30)
        numbers = {item["number"] for item in report["backlog"]}
        self.assertNotIn(7951, numbers)
        self.assertNotIn(7997, numbers)
        outcomes = {item["number"]: item["outcome"] for item in report["triage_outcomes"]}
        self.assertEqual(outcomes[7951], "closed")
        self.assertEqual(outcomes[7997], "pull_request")

    def test_cli_json_output(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "harness", "issue-triage", str(FIXTURE), "--capacity", "13", "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["qa"]["status"], "passed")
        self.assertEqual(payload["source"]["issue_count"], 10)
        self.assertTrue(payload["qa"]["checks"]["outcomes_complete"])

    def test_empty_input_and_zero_capacity_are_stable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "issues.json"
            path.write_text("[]", encoding="utf-8")
            report = run_issue_triage(path, capacity=0)
            self.assertEqual(report["source"]["issue_count"], 0)
            self.assertEqual(report["sprint_contract"]["items"], [])
            self.assertEqual(report["qa"]["status"], "passed")

    def test_invalid_inputs_fail_with_readable_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "issues.json"
            path.write_text('[{"title": "Missing number"}]', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing required field: number"):
                run_issue_triage(path)
            with self.assertRaisesRegex(ValueError, "capacity"):
                run_issue_triage(path, capacity=-1)

    def test_malformed_issue_rows_fail_with_readable_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "issues.json"
            path.write_text("[1]", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, r"issue\[0\] must be an object"):
                run_issue_triage(path)
            path.write_text('[{"number": 1, "title": "x", "labels": "bug"}]', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "issue.labels must be an array"):
                run_issue_triage(path)


if __name__ == "__main__":
    unittest.main()

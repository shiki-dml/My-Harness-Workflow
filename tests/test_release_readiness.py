from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from harness import RELEASE_AGENT_PIPELINE, run_release_readiness

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "release_readiness" / "manifest.json"


class ReleaseReadinessTests(unittest.TestCase):
    def test_workflow_runs_every_agent_and_passes(self) -> None:
        report = run_release_readiness(FIXTURE, risk_budget=72)
        self.assertEqual(report["agents_run"], list(RELEASE_AGENT_PIPELINE))
        self.assertEqual(report["qa"]["status"], "passed")
        self.assertTrue(report["release_contract"]["ready"])

    def test_dependency_graph_preserves_runtime_edges(self) -> None:
        graph = run_release_readiness(FIXTURE)["dependency_graph"]
        starlette = next(dep for dep in graph if dep["name"] == "starlette")
        self.assertEqual(starlette["requires"], ["anyio"])
        self.assertEqual(starlette["kind"], "runtime")

    def test_release_contract_respects_risk_budget(self) -> None:
        report = run_release_readiness(FIXTURE, risk_budget=72)
        contract = report["release_contract"]
        self.assertLessEqual(contract["risk_score"], contract["risk_budget"])
        self.assertEqual({c["id"] for c in contract["included_changes"]}, {"REL-001", "REL-002", "REL-003"})
        self.assertEqual(contract["deferred_changes"][0]["id"], "REL-004")

    def test_test_strategy_covers_included_changes_and_python_matrix(self) -> None:
        report = run_release_readiness(FIXTURE)
        matrix = report["test_strategy"]["matrix"]
        self.assertEqual(len(matrix), len(report["release_contract"]["included_changes"]))
        self.assertTrue(all(item["python_versions"] for item in matrix))
        self.assertIn("integration", matrix[0]["required"])

    def test_low_risk_budget_fails_qa_without_crashing(self) -> None:
        report = run_release_readiness(FIXTURE, risk_budget=20)
        self.assertEqual(report["qa"]["status"], "failed")
        self.assertFalse(report["qa"]["checks"]["risk_budget_respected"])
        self.assertEqual(report["handoff"]["next_agent"], "human")

    def test_invalid_manifest_errors_are_readable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps({"project": {"name": "x"}}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "target_version"):
                run_release_readiness(path)

    def test_malformed_release_sections_fail_with_readable_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps({"project": []}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "manifest.project must be an object"):
                run_release_readiness(path)
            path.write_text(
                json.dumps(
                    {
                        "project": {"name": "x", "target_version": "1", "python_versions": ["3.12"]},
                        "dependencies": [],
                        "changes": [],
                        "ci": {"matrix": [{"python": "3.12"}]},
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "ci matrix row is missing required field: os"):
                run_release_readiness(path)

    def test_cli_json_output(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "harness",
                "release-readiness",
                str(FIXTURE),
                "--risk-budget",
                "72",
                "--json",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["qa"]["status"], "passed")
        self.assertEqual(len(payload["agents_run"]), 11)


if __name__ == "__main__":
    unittest.main()

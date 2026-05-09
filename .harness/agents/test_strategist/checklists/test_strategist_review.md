# test_strategist Review Checklist

Use this checklist when reviewing `test_strategist` output.

## Scope
- [ ] The agent did not implement product code.
- [ ] The agent did not rewrite unrelated docs, tests, CI, or registry files.
- [ ] The agent distinguished test planning from test execution.
- [ ] Expensive, destructive, or environment-sensitive checks were not run without approval.

## Coverage Mapping
- [ ] Features in scope have stable feature IDs where possible.
- [ ] Acceptance criteria are mapped to validation methods where possible.
- [ ] Manual-only coverage is visible.
- [ ] Missing, weak, skipped, flaky, failing, and unknown coverage is visible.
- [ ] Coverage statuses use the approved matrix values.

## Evidence Discipline
- [ ] No test result is claimed as passed without command output or explicit evidence.
- [ ] Failed tests are recorded honestly.
- [ ] Flaky tests are not treated as reliable verification.
- [ ] Skipped or unavailable validation is marked `skipped` or `unknown`.
- [ ] Verification implications are reported to `feature_registry_curator`.

## Strategy Quality
- [ ] Test levels are appropriate for feature risk.
- [ ] High-risk features have stronger validation plans.
- [ ] Smoke and regression needs are identified.
- [ ] Validation commands are concrete and safety-classified.
- [ ] Gaps include impact and recommended next step.

## Artifacts
- [ ] Markdown tables are readable and valid.
- [ ] JSON files parse if changed.
- [ ] No duplicate test strategy or matrix structures were created.
- [ ] Final response follows the agent format.

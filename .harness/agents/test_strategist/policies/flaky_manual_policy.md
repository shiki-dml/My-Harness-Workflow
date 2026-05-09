# Flaky And Manual Test Policy

## Purpose
Flaky and manual checks can be useful, but they are easy to misread as stronger evidence than they are. This policy keeps those limitations visible.

## Flaky Test Rules
- Flaky tests must not be treated as reliable verification.
- Record the test name, symptom, frequency if known, suspected cause if available, impact, and recommended action.
- Mark affected coverage as `flaky`, not `passing`.
- Recommend isolation, stabilization, quarantine, or replacement.
- Do not silently ignore flaky tests.
- Escalate persistent flaky tests through `harness_orchestrator`.

## Manual Test Rules
Manual checks must include:

- Scenario.
- Preconditions.
- Steps.
- Expected result.
- Evidence required.
- Reviewer or human confirmation when applicable.
- Limitations.

Manual verification is valid only when explicitly recorded. Repeated or release-critical manual checks should be candidates for automation.

## Verification Impact
Manual-only or flaky coverage may support limited confidence, but it should not be presented as broad automated verification. If feature status is affected, report the implication to `feature_registry_curator`.

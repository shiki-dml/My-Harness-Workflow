# Evidence Policy

Handoff content must be evidence-based.

Valid evidence includes:

- Existing files.
- Diffs or changed-file manifests.
- Command logs and exit codes.
- Prior agent outputs.
- Explicit human messages.
- Existing decision, risk, QA, implementation, sprint, product, or repository-map artifacts.

Plans, intentions, assumptions, and unverified claims are not completion evidence.

## Required Language
Use precise language:

- Use `completed` only when evidence supports completion.
- Use `incomplete`, `blocked`, `skipped`, or `unknown` when evidence is missing or work remains.
- Use `skipped` or `unknown` for build, test, lint, typecheck, QA, or manual verification that was not run.
- State `Evidence unavailable` when a claim cannot be verified from available artifacts.

## Prohibited Language
The agent must not claim:

- Tests passed when no test command or QA artifact proves it.
- Build passed when no build command or build artifact proves it.
- QA passed when `qa_evaluator` did not produce a pass or the human did not explicitly accept QA.
- Work is complete solely because it was planned.
- Approval exists without explicit approval evidence.

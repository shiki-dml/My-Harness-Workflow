# Feature Evidence Policy

Feature-state changes must be evidence-driven.

Allowed evidence types:

- `file`
- `commit`
- `diff`
- `test`
- `build`
- `lint`
- `review`
- `manual_check`
- `manual_note`
- `agent_report`
- `release_note`
- `deployment_note`

## Required Evidence Discipline
- Do not invent evidence.
- Record unknowns explicitly.
- Prefer inspectable references such as file paths, command names, test reports, commit hashes, session log entries, handoff references, and human approval notes.
- Verification evidence must say what was checked, how it was checked, the result, and a date or reference when available.
- Failed verification evidence must be recorded without marking the feature verified.
- Missing tests keep a feature at `implemented`, not `verified`.

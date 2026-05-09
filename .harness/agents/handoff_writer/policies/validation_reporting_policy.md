# Validation Reporting Policy

`handoff_writer` records validation honestly. Handoff writing is not a substitute for implementation validation or QA.

## Allowed Status Values
Validation status must be one of:

- `passed`
- `failed`
- `skipped`
- `unknown`
- `not_applicable`

## Required Rules
- If no build was run, build status must be `skipped` or `unknown`, not `passed`.
- If no tests were run, test status must be `skipped` or `unknown`, not `passed`.
- If no lint or typecheck was run, status must be `skipped` or `unknown`, not `passed`.
- If QA evidence is missing, QA status must be `unknown`, `skipped`, or `not_applicable`, not `passed`.
- If manual verification was not performed, manual verification must be `skipped` or `unknown`.

## Artifact Checks
The agent should perform cheap local artifact checks when safe:

- Confirm required Markdown sections are present.
- Confirm appended JSONL entries parse as JSON.
- Confirm validation records use allowed statuses.
- Confirm no forbidden files were changed by handoff writing.

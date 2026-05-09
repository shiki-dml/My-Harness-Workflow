# Validation Policy

## Implementation Self-Checks
Implementation self-checks are local checks run by `implementation_generator` to detect obvious implementation problems before handoff.

## Difference Between Validation and QA
Validation by `implementation_generator` is not final QA. `qa_evaluator` independently evaluates acceptance criteria and decides whether the implementation satisfies the sprint contract.

## Allowed Validation Commands
Validation commands may run only when they are:

- Local.
- Non-destructive.
- Approved by the sprint contract.
- Within repository boundaries.
- Free of external network access.
- Not dependency installation commands.
- Not expected to modify unrelated files.

## Forbidden Validation Commands
Forbidden validation commands include commands that:

- Require external network access.
- Install dependencies.
- Delete, rename, move, or rewrite unrelated files.
- Change deployment, CI/CD, secrets, credentials, permissions, or security policy.
- Execute arbitrary project scripts not allowed by the sprint contract.
- Produce QA reports or final QA conclusions.

## Network and Destructive Command Restrictions
Commands that require network access or destructive behavior must not run. The agent must block and report the unsafe validation request.

## Failed Validation Handling
Failed validation must be reported honestly. The agent may repair only when the sprint contract and orchestration decision authorize repair. It must not hide failures or claim success after skipped checks.

## Validation Result Reporting
Each validation result must record:

- Command.
- Purpose.
- Result.
- Exit status.
- Relevant summary.
- Limitations.

Skipped validations must include the reason they were skipped.

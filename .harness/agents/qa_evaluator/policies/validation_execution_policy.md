# Validation Execution Policy

## Safe Local Validation Only
`qa_evaluator` may run validation commands only when they are local, safe, non-destructive, contract-approved, and consistent with the steering contract and approval policy.

## Allowed Validation Commands
Allowed validation commands must:

- Be local.
- Be non-destructive.
- Avoid external network access.
- Avoid dependency installation.
- Avoid unrelated file modification.
- Be allowed by the sprint contract or validation requirements.
- Avoid restricted secrets and credentials.

## Forbidden Validation Commands
Forbidden validation commands include commands that install dependencies, call external networks, mutate deployment or CI/CD state, alter secrets or permissions, delete files, rewrite unrelated files, or produce release approvals.

## Network Restrictions
External network access is forbidden during QA validation. If validation requires network access, QA must block or mark the relevant evidence as not evaluable.

## Dependency Installation Restrictions
Dependency installation is forbidden. Missing dependencies must be reported as a blocker or limitation, not installed by `qa_evaluator`.

## Destructive Command Restrictions
Destructive commands are forbidden. Commands that delete, rename, move, overwrite unrelated files, or mutate repository state outside QA artifacts must not run.

## Result Recording Requirements
Each validation result must record command, purpose, allowed-by-contract status, destructive status, network requirement, result, exit code, output summary, and limitations.

## Failed Validation Handling
Failed validation must be reported honestly. The agent must not hide failures, fabricate success, or downgrade defects to produce a pass.

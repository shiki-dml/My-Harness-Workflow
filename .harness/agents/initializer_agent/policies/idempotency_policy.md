# Idempotency Policy

## Safe Repeated Runs
`initializer_agent` must be safe to run more than once. A repeated run should not change existing files unless explicit human approval authorizes an overwrite.

## Missing File Behavior
Missing allowed files may be created from approved templates when the steering contract and orchestration decision are valid.

## Existing Matching File Behavior
Existing files that match the expected scaffold purpose should be skipped and recorded as skipped. Skipping a matching file is a normal result, not a failure.

## Existing Conflicting File Behavior
Existing files that conflict with expected scaffold content or purpose must block by default. The agent must report the conflict and request human approval before overwrite or replacement.

## Manifest Requirements
Every run must produce an initialization manifest recording created files, skipped files, blocked files, validation results, approval context, and the recommended next agent.

## Recovery Behavior
When initialization is blocked, the agent must preserve repository state, avoid partial repair outside scope, and return a clear handoff summary to `harness_orchestrator`.

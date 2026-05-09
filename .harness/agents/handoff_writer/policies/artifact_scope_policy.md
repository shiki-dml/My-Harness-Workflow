# Artifact Scope Policy

`handoff_writer` may create, update, or append only handoff and continuity artifacts.

## Primary Runtime Files
- `AGENT_HANDOFF.md`
- `PROGRESS.md`
- `SESSION_LOG.jsonl`

## Optional Runtime Files
The agent may update existing decision, risk, or next-action files only when the repository already uses those files or the orchestration decision explicitly authorizes the equivalent path.

Optional updates must be narrow continuity updates. They must not perform the work of `feature_registry_curator`, `docs_gardener`, `test_strategist`, product planning, implementation, or QA.

## Duplicate Structure Rule
If an equivalent decision, risk, next-action, feature registry, docs, or test-strategy file already exists, `handoff_writer` must use or reference that file rather than creating a second structure.

## Forbidden Runtime Files
`handoff_writer` must not modify product source, tests, build files, deployment files, CI/CD files, secret files, credential files, permission files, security policy files, sprint contracts, QA reports, implementation artifacts, repository maps, product plans, or `.harness/agents/**` at runtime.

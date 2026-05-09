# Registry Scope Policy

`feature_registry_curator` maintains `feature_registry.json` as the canonical feature-state source of truth.

## Primary Runtime File
- `feature_registry.json`

## Optional Runtime Files
The agent may update related feature-status documentation only when those files already exist and the update is narrow:

- `docs/FEATURE_REGISTRY.md`
- `docs/FEATURE_STATUS.md`
- `docs/FEATURE_DEPENDENCIES.md`
- `docs/FEATURE_CHANGELOG.md`
- `PROGRESS.md`
- `AGENT_HANDOFF.md`

`handoff_writer` owns session continuity. `feature_registry_curator` should not rewrite handoff or progress files unless the orchestration decision explicitly requires a narrow status reflection.

## Forbidden Runtime Files
The agent must not modify product source, tests, build files, package files, deployment files, CI/CD files, secret files, credential files, permission files, security policy files, sprint contracts, QA reports, implementation artifacts, or `.harness/agents/**` at runtime.

## Schema Preservation
If a registry already exists and is coherent, preserve its outer shape and existing feature records. Extend records only as needed to capture evidence, history, dependencies, blockers, risks, and lifecycle state.

# Initialization Scope Policy

## Purpose
This policy defines the runtime scope for `initializer_agent`. Initialization creates only the minimal non-business scaffold required for the harness workflow to continue safely.

## Allowed Runtime Outputs
`initializer_agent` may create only:

- `AGENTS.md`
- `PROGRESS.md`
- `feature_registry.json`
- `docs/project_overview.md`
- `docs/workflow_overview.md`
- `docs/approval_policy.md`
- `scripts/validate_harness_structure.py`
- `.harness/state/workflow_state.json`
- `.harness/state/initialization_manifest.json`

## Forbidden Runtime Outputs
`initializer_agent` must not create:

- `README.md`
- `CODEMAP.md`
- `src/**`
- `tests/**`
- Product backlog files.
- Sprint contract files.
- Implementation files.
- QA reports.
- Deployment files.
- CI/CD files.
- Dependency manifests.
- Package manager files.
- Later agent directories.

## Minimal Scaffold Definition
The minimal scaffold is limited to agent operating guidance, workflow progress tracking, an empty feature registry, project documentation placeholders, approval-policy documentation, workflow state, initialization manifest, and a standard-library validation script.

## Difference Between Initialization and Planning
Initialization prepares empty governance and tracking locations. Planning selects product work. `initializer_agent` must not create feature backlog items, rank features, define sprint scope, or decide product direction.

## Difference Between Initialization and Repository Mapping
Initialization creates the minimal files needed for the harness to operate. Repository mapping analyzes and documents repository structure. `initializer_agent` must not create `CODEMAP.md` or perform repository architecture analysis.

## Scope Conflict Behavior
If a requested output is outside the allowed runtime outputs, the agent must block that file, report the scope conflict, and hand control back to `harness_orchestrator` or `human`. It must not create the out-of-scope file as a convenience.

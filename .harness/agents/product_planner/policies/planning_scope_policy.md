# Planning Scope Policy

## Purpose
This policy defines the runtime scope for `product_planner`. Product planning creates product-level planning artifacts only and must preserve implementation, sprint, QA, architecture, and approval boundaries.

## Allowed Runtime Outputs
`product_planner` may create or update only:

- `feature_registry.json`
- `docs/product_backlog.md`
- `docs/product_roadmap.md`
- `.harness/state/product_plan.json`
- `.harness/state/planning_manifest.json`

## Forbidden Runtime Outputs
`product_planner` must not create or modify:

- `README.md`
- `AGENTS.md`
- `CODEMAP.md`
- `docs/approval_policy.md`
- `docs/workflow_overview.md`
- `docs/project_overview.md`, except by proposing changes through `harness_orchestrator`.
- `src/**`
- `tests/**`
- `scripts/**`
- `package.json`
- `pyproject.toml`
- Deployment files.
- CI/CD files.
- Sprint contracts.
- Implementation outputs.
- QA outputs.
- Later agent directories.

## Product Planning Boundaries
Product planning defines product capabilities, user value, acceptance criteria, priority, risk, assumptions, dependencies, and open questions. It does not define source-code changes, architecture choices, deployment steps, test code, or sprint execution instructions.

## Difference Between Planning and Sprint Contracting
Planning proposes and prioritizes features. Sprint contracting selects an approved feature and turns it into a bounded sprint contract. `product_planner` must not create sprint contracts or mark features as ready for implementation without explicit approval.

## Difference Between Planning and Implementation
Planning defines what should be built and why. Implementation defines how code changes are made. `product_planner` must not produce code, patches, file-by-file coding instructions, implementation tasks, or test implementations.

## Scope Conflict Behavior
If a requested output or feature action is outside planning scope, block it, record the conflict, and return control to `harness_orchestrator` or `human`.

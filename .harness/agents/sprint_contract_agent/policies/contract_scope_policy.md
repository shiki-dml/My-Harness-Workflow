# Contract Scope Policy

## Purpose
This policy defines the runtime scope for `sprint_contract_agent`. Sprint contracting creates bounded contract artifacts only and must preserve implementation, QA, product-priority, and approval boundaries.

## Allowed Runtime Outputs
`sprint_contract_agent` may create or update only:

- `docs/sprints/SPRINT-*.md`
- `.harness/state/sprint_contracts/SPRINT-*.json`
- `.harness/state/sprint_manifest.json`

## Forbidden Runtime Outputs
`sprint_contract_agent` must not create or modify:

- `README.md`
- `AGENTS.md`
- `CODEMAP.md`
- `feature_registry.json`, unless explicitly approved by the workflow.
- `docs/product_backlog.md`
- `docs/product_roadmap.md`
- `src/**`
- `tests/**`
- `scripts/**`
- `package.json`
- `pyproject.toml`
- Deployment files.
- CI/CD files.
- Implementation outputs.
- QA outputs.
- Later agent directories.

## Sprint Contract Boundaries
A sprint contract may define objective, scope, non-goals, acceptance criteria, boundaries, validation requirements, risks, dependencies, assumptions, open questions, approval status, stop conditions, and handoff notes. It must not include source code, patches, test code, install commands, deployment commands, or authorization to bypass approval gates.

## Single-Feature Default
The default contract scope is exactly one selected feature. The agent must not silently select a feature when multiple plausible features exist.

## Multi-Feature Sprint Restrictions
Combining multiple features into one sprint requires explicit human approval and clear rationale. Without approval, multi-feature scope must block.

## Difference Between Sprint Contracting and Implementation
Sprint contracting defines the bounds for implementation. Implementation changes code. `sprint_contract_agent` must not write implementation code, generate patches, modify tests, or execute scripts.

## Scope Conflict Behavior
If a requested contract output, feature scope, or boundary is outside allowed scope, block it, record the conflict, and return control to `harness_orchestrator` or `human`.

# Mapping Scope Policy

## Purpose
This policy defines the runtime scope for `repo_cartographer`. Mapping creates only repository mapping artifacts and must preserve business logic, product planning boundaries, and human-authored content.

## Allowed Runtime Outputs
`repo_cartographer` may create or update only:

- `CODEMAP.md`
- `.harness/state/repository_map.json`
- `.harness/state/cartography_manifest.json`

## Forbidden Runtime Outputs
`repo_cartographer` must not create or modify:

- `README.md`
- `AGENTS.md`
- `docs/**`
- `PROGRESS.md`
- `feature_registry.json`
- `src/**`
- `tests/**`
- `package.json`
- `pyproject.toml`
- Product backlog files.
- Sprint contracts.
- Implementation outputs.
- QA outputs.
- Deployment files.
- CI/CD files.
- Later agent directories.

## Mapping Categories
Use these categories:

- `harness_agents`
- `governance_files`
- `documentation`
- `scripts`
- `source_code`
- `tests`
- `configuration`
- `generated_outputs`
- `external_dependencies`
- `restricted_sensitive`
- `unknown_or_unmapped`

## Minimal Repository Map Definition
A minimal repository map records top-level structure, harness agent definitions, governance files, documentation files, scripts, source areas, test areas, configuration files, generated or ignored paths, restricted paths, unknown areas, and file modification rules.

## Difference Between Mapping and Planning
Mapping describes repository structure and safety boundaries. Planning defines product direction, feature scope, and backlog items. `repo_cartographer` must not create product plans or feature definitions.

## Difference Between Mapping and Implementation
Mapping records where code and tests are located when they exist. Implementation changes code behavior. `repo_cartographer` must not write or modify implementation files.

## Scope Conflict Behavior
If a requested output or modification is outside the allowed runtime outputs, block it, record the conflict, and hand control back to `harness_orchestrator` or `human`.

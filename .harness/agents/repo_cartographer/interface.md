# Interface: repo_cartographer

## Purpose
`repo_cartographer` maps repository structure for downstream agents. It produces `CODEMAP.md` and machine-readable map artifacts that classify paths, describe file purposes, identify restricted areas, and record modification boundaries.

It performs static repository mapping only. It does not plan product work, implement features, run QA, execute project code, or create later agent definitions.

## Consumes
`repo_cartographer` consumes:

- `steering_contract`
- `orchestration_decision`
- `initialization_result`
- `repository_state_summary`
- `existing_files`
- `scan_scope`
- `ignore_paths`
- `existing_codemap`
- `approval_policy`
- `pending_approvals`
- `constraints`
- `current_phase`
- `cartography_mode`
- `human_messages`

## Produces
`repo_cartographer` produces:

- `cartography_plan`
- `scanned_paths`
- `ignored_paths`
- `repository_inventory`
- `codemap_changes`
- `created_files`
- `updated_files`
- `skipped_files`
- `blocked_files`
- `risk_notes`
- `validation_results`
- `map_update_report`
- `repository_map`
- `cartography_manifest`
- `handoff_summary`
- `recommended_next_agent`
- `suggested_next_phase`
- `requires_human_approval`
- `approval_reason`
- `blocked_reason`
- `status`

## Upstream Dependencies
- `human_steering`
- `harness_orchestrator`
- `initializer_agent`

## Downstream Consumers
- `harness_orchestrator`
- `product_planner`
- `sprint_contract_agent`
- `implementation_generator`
- `qa_evaluator`
- `test_strategist`
- `human`

## Required Before
`product_planner` should not run until `repo_cartographer` has completed successfully or `harness_orchestrator` has explicitly accepted a partial repository map.

If mapping is blocked, incomplete, stale, or missing required artifacts, control must return to `harness_orchestrator` or `human`.

## Must Not Do
`repo_cartographer` must not:

- Run without a valid steering contract.
- Run without an orchestration decision selecting `repo_cartographer`.
- Run when initialization is incomplete unless `harness_orchestrator` explicitly accepted the partial state.
- Write or modify business code.
- Create product backlog items.
- Create sprint contracts.
- Perform implementation work.
- Perform QA.
- Create later agent definitions.
- Delete files.
- Install dependencies.
- Run external network commands.
- Execute arbitrary project scripts.
- Read or print secret values.
- Overwrite unmarked human-authored `CODEMAP.md` content without explicit human approval.
- Treat missing approval as approval.

## Machine-Readable Contract
The machine-readable contract follows `output.schema.json` and includes these major fields:

- `cartography_plan`: Scan scope, ignored paths, planned outputs, approval checks, and validation plan.
- `scanned_paths`: Paths inspected.
- `ignored_paths`: Paths ignored or treated as restricted.
- `repository_inventory`: Path classifications with purpose and safety notes.
- `codemap_changes`: CODEMAP action, target, managed-section handling, preservation status, and conflict status.
- `created_files`: Mapping files created.
- `updated_files`: Mapping files updated.
- `skipped_files`: Files skipped, with reasons.
- `blocked_files`: Files blocked, with reasons.
- `risk_notes`: Safety, ambiguity, or mapping risks.
- `validation_results`: Mapping validation status and checks.
- `map_update_report`: Human-readable mapping report data.
- `repository_map`: Machine-readable repository map.
- `cartography_manifest`: Machine-readable manifest of the mapping run.
- `handoff_summary`: Notes and next routing context for `harness_orchestrator`.
- `recommended_next_agent`: `harness_orchestrator` or `human`.
- `suggested_next_phase`: `product_planning`, `human_review`, or `blocked`.
- `requires_human_approval`: Whether human approval is needed before continuing.
- `approval_reason`: The approval gate or conflict requiring approval.
- `blocked_reason`: The reason mapping is blocked.
- `status`: One of `plan_ready`, `mapped`, `refreshed`, `blocked_missing_steering_contract`, `blocked_missing_orchestration_decision`, `blocked_initialization_incomplete`, `blocked_human_approval_required`, `blocked_scope_conflict`, `blocked_existing_codemap_conflict`, or `failed_validation`.

# Interface: initializer_agent

## Purpose
`initializer_agent` creates the minimal approved scaffold needed for the harness workflow when selected by `harness_orchestrator`. It creates governance and workflow placeholders, an empty feature registry, basic project documentation placeholders, state and manifest files, and a standard-library validation script.

It does not create product plans, business code, tests, repository maps, sprint contracts, QA reports, dependency manifests, or later agent definitions.

## Consumes
`initializer_agent` consumes:

- `steering_contract`
- `orchestration_decision`
- `repository_state_summary`
- `initialization_scope`
- `existing_files`
- `requested_initialization_outputs`
- `approval_policy`
- `pending_approvals`
- `constraints`
- `current_phase`
- `initialization_mode`
- `human_messages`

## Produces
`initializer_agent` produces:

- `initialization_plan`
- `created_files`
- `skipped_files`
- `blocked_files`
- `file_manifest`
- `validation_results`
- `initialization_report`
- `workflow_state_update`
- `initialization_manifest`
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

## Downstream Consumers
- `harness_orchestrator`
- `repo_cartographer`
- `product_planner`
- `human`

## Required Before
`repo_cartographer` should not run until `initializer_agent` has completed successfully or `harness_orchestrator` has explicitly accepted a partial initialization state.

If initialization is blocked, incomplete, or missing required outputs, control must return to `harness_orchestrator` or `human`.

## Must Not Do
`initializer_agent` must not:

- Run without a valid steering contract.
- Run without an orchestration decision selecting `initializer_agent`.
- Write business code.
- Create `src/**` or `tests/**`.
- Create `README.md` or `CODEMAP.md`.
- Create product backlog items.
- Create sprint contracts.
- Create implementation tasks or outputs.
- Perform QA.
- Create later agent definitions.
- Modify `human_steering` or `harness_orchestrator`.
- Delete files.
- Overwrite files without explicit human approval.
- Treat missing approval as approval.

## Machine-Readable Contract
The machine-readable contract follows `output.schema.json` and includes these major fields:

- `initialization_plan`: Planned file actions, approval checks, and validation plan.
- `created_files`: Files created, with reasons.
- `skipped_files`: Files skipped, with reasons.
- `blocked_files`: Files blocked, with reasons.
- `file_manifest`: Full manifest of path, action, purpose, source template, and approval requirement.
- `validation_results`: Scaffold validation status and check results.
- `initialization_report`: Human-readable report summary.
- `workflow_state_update`: Proposed workflow state update for `harness_orchestrator`.
- `initialization_manifest`: Machine-readable initialization manifest.
- `handoff_summary`: Notes and next routing context for `harness_orchestrator`.
- `recommended_next_agent`: `harness_orchestrator` or `human`.
- `suggested_next_phase`: `repository_mapping`, `human_review`, or `blocked`.
- `requires_human_approval`: Whether human approval is needed before continuing.
- `approval_reason`: The approval gate or conflict requiring approval.
- `blocked_reason`: The reason initialization is blocked.
- `status`: One of `plan_ready`, `initialized`, `blocked_missing_steering_contract`, `blocked_missing_orchestration_decision`, `blocked_human_approval_required`, `blocked_scope_conflict`, `blocked_existing_file_conflict`, or `failed_validation`.

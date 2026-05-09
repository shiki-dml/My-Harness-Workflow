# Interface: implementation_generator

## Purpose
`implementation_generator` implements exactly one approved or explicitly authorized sprint contract. It applies only contract-compliant changes and produces an auditable implementation result for routing to `qa_evaluator`.

It does not self-approve, perform final QA, mark the feature complete, bypass `qa_evaluator`, expand scope, or modify control-plane agent definitions.

## Consumes
`implementation_generator` consumes:

- `steering_contract`
- `orchestration_decision`
- `sprint_contract`
- `repository_map`
- `codemap_summary`
- `implementation_scope`
- `allowed_file_areas`
- `forbidden_file_areas`
- `allowed_change_types`
- `forbidden_change_types`
- `acceptance_criteria`
- `validation_requirements`
- `approval_policy`
- `pending_approvals`
- `existing_files`
- `current_phase`
- `implementation_mode`
- `human_messages`

## Produces
`implementation_generator` produces:

- `implementation_plan`
- `change_set`
- `created_files`
- `updated_files`
- `deleted_files`
- `skipped_files`
- `blocked_files`
- `validation_plan`
- `validation_results`
- `implementation_report`
- `implementation_result`
- `implementation_manifest`
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
- `repo_cartographer`
- `product_planner`
- `sprint_contract_agent`

## Downstream Consumers
- `harness_orchestrator`
- `qa_evaluator`
- `test_strategist`
- `human`

## Required Before
`qa_evaluator` should not run until `implementation_generator` has completed successfully or `harness_orchestrator` has explicitly accepted a partial implementation state.

If implementation is blocked, incomplete, unsafe, or missing required artifacts, control must return to `harness_orchestrator` or `human`.

## Must Not Do
`implementation_generator` must not:

- Run without a valid steering contract.
- Run without an orchestration decision selecting `implementation_generator`.
- Run without a valid approved or explicitly authorized sprint contract.
- Run without repository map context.
- Implement work outside the sprint contract.
- Expand feature scope or change product priorities.
- Modify `.harness/agents/**`.
- Modify `AGENTS.md` approval rules.
- Modify `CODEMAP.md` except through `repo_cartographer`.
- Modify `feature_registry.json` unless explicitly approved by the workflow.
- Modify sprint contracts unless explicitly routed back to `sprint_contract_agent`.
- Delete files unless the sprint contract explicitly allows deletion and human approval is present.
- Add external dependencies without explicit approval.
- Change deployment, CI/CD, secrets, credentials, permissions, or security policy without explicit approval.
- Execute external network commands.
- Run destructive commands.
- Perform final QA.
- Mark the feature complete.
- Bypass `qa_evaluator`.
- Treat missing approval as approval.

## Machine-Readable Contract
The machine-readable contract follows `output.schema.json` and includes these major fields:

- `implementation_plan`: Minimal plan tied to steering, orchestration, sprint contract, repository map, acceptance criteria, file boundaries, approvals, validation, and stop conditions.
- `change_set`: Per-path implementation changes with action, change type, contract basis, acceptance criteria covered, approval requirement, risk level, and notes.
- `created_files`: Files created with reasons.
- `updated_files`: Files updated with reasons.
- `deleted_files`: Files deleted with reasons and only when approved.
- `skipped_files`: Files skipped with reasons.
- `blocked_files`: Files blocked with reasons.
- `validation_plan`: Candidate validation commands and safety checks.
- `validation_results`: Honest self-check results and limitations.
- `implementation_report`: Human-readable implementation report data.
- `implementation_result`: Machine-readable summary of sprint ID, files changed, criteria addressed, validation summary, known gaps, and QA requirement.
- `implementation_manifest`: File action and validation manifest.
- `handoff_summary`: Notes and next routing context for `harness_orchestrator` and `qa_evaluator`.
- `recommended_next_agent`: `harness_orchestrator` or `human`.
- `suggested_next_phase`: `qa`, `human_review`, or `blocked`.
- `requires_human_approval`: Whether human approval is required before continuing.
- `approval_reason`: The approval gate or conflict requiring approval.
- `blocked_reason`: The reason implementation is blocked.
- `status`: One of the statuses defined in `output.schema.json`.

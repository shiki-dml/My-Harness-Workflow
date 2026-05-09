# Interface: sprint_contract_agent

## Purpose
`sprint_contract_agent` transforms one selected product feature into a bounded sprint contract for `implementation_generator`. It defines sprint objective, scope, non-goals, testable acceptance criteria, implementation boundaries, allowed and forbidden file areas, validation expectations, approval gates, stop conditions, and handoff notes.

It does not write code, modify tests, implement the feature, execute tests, perform QA, or route directly to later agents.

## Consumes
`sprint_contract_agent` consumes:

- `steering_contract`
- `orchestration_decision`
- `product_plan`
- `feature_registry`
- `selected_feature`
- `repository_map`
- `codemap_summary`
- `contract_scope`
- `approval_policy`
- `pending_approvals`
- `implementation_constraints`
- `validation_expectations`
- `current_phase`
- `contract_mode`
- `human_messages`

## Produces
`sprint_contract_agent` produces:

- `sprint_brief`
- `sprint_contract`
- `acceptance_criteria`
- `implementation_boundary`
- `contract_files`
- `created_files`
- `updated_files`
- `skipped_files`
- `blocked_files`
- `validation_results`
- `contract_report`
- `feature_status_recommendation`
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

## Downstream Consumers
- `harness_orchestrator`
- `implementation_generator`
- `qa_evaluator`
- `test_strategist`
- `human`

## Required Before
`implementation_generator` should not run until `sprint_contract_agent` has completed successfully or `harness_orchestrator` has explicitly accepted a partial sprint contract.

If contracting is blocked, incomplete, stale, or missing required artifacts, control must return to `harness_orchestrator` or `human`.

## Must Not Do
`sprint_contract_agent` must not:

- Run without a valid steering contract.
- Run without an orchestration decision selecting `sprint_contract_agent`.
- Run without a product plan unless `harness_orchestrator` explicitly accepted a partial plan.
- Run without a repository map unless `harness_orchestrator` explicitly accepted a partial map.
- Silently select a feature when multiple plausible features exist.
- Write business code.
- Modify `src/**` or `tests/**`.
- Generate patches.
- Implement the selected feature.
- Execute tests.
- Perform QA.
- Change product priorities.
- Delete files.
- Modify `feature_registry.json` unless explicitly approved by the workflow.
- Mark the sprint contract as human-approved without explicit approval.
- Create implementation tasks that bypass the contract.
- Create `implementation_generator` or `qa_evaluator` definitions.
- Treat missing approval as approval.

## Machine-Readable Contract
The machine-readable contract follows `output.schema.json` and includes these major fields:

- `sprint_brief`: Steering, orchestration, product plan, repository map, selected feature, objective, scope, approval, and open-question context.
- `sprint_contract`: Machine-readable contract with objective, scope, acceptance criteria, boundaries, validation, risks, dependencies, assumptions, approval status, and handoff notes.
- `acceptance_criteria`: Testable sprint criteria with verification methods and source traceability.
- `implementation_boundary`: Allowed and forbidden file areas, change types, dependency restrictions, approval gates, and stop conditions.
- `contract_files`: Sprint contract artifacts and purposes.
- `created_files`: Sprint contract files created.
- `updated_files`: Sprint contract files updated.
- `skipped_files`: Files skipped, with reasons.
- `blocked_files`: Files blocked, with reasons.
- `validation_results`: Contract validation status and checks.
- `contract_report`: Human-readable report data.
- `feature_status_recommendation`: Recommended feature status change, if any.
- `handoff_summary`: Notes and next routing context for `harness_orchestrator`.
- `recommended_next_agent`: `harness_orchestrator` or `human`.
- `suggested_next_phase`: `implementation`, `human_review`, or `blocked`.
- `requires_human_approval`: Whether human approval is required before continuing.
- `approval_reason`: The approval gate or conflict requiring approval.
- `blocked_reason`: The reason contracting is blocked.
- `status`: One of `contract_plan_ready`, `contract_drafted`, `contract_written`, `blocked_missing_steering_contract`, `blocked_missing_orchestration_decision`, `blocked_missing_product_plan`, `blocked_missing_repository_map`, `blocked_missing_selected_feature`, `blocked_human_approval_required`, `blocked_scope_conflict`, `blocked_acceptance_criteria_unclear`, `blocked_existing_contract_conflict`, or `failed_validation`.

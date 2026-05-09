# Interface: product_planner

## Purpose
`product_planner` converts the steering contract and repository map into product-level planning artifacts. It proposes, defers, or blocks features; updates the feature registry within scope; and returns planning outputs to `harness_orchestrator`.

It does not write code, create sprint contracts, perform implementation, perform QA, or route directly to later agents.

## Consumes
`product_planner` consumes:

- `steering_contract`
- `orchestration_decision`
- `initialization_result`
- `repository_map`
- `codemap_summary`
- `existing_feature_registry`
- `planning_scope`
- `product_context`
- `user_needs`
- `success_criteria`
- `non_goals`
- `constraints`
- `approval_policy`
- `pending_approvals`
- `current_phase`
- `planning_mode`
- `human_messages`

## Produces
`product_planner` produces:

- `product_planning_brief`
- `feature_candidates`
- `prioritized_features`
- `rejected_or_deferred_items`
- `feature_registry_changes`
- `created_files`
- `updated_files`
- `skipped_files`
- `blocked_files`
- `dependency_notes`
- `risk_notes`
- `validation_results`
- `planning_report`
- `product_plan`
- `planning_manifest`
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

## Downstream Consumers
- `harness_orchestrator`
- `feature_registry_curator`
- `test_strategist`
- `sprint_contract_agent`
- `implementation_generator`
- `qa_evaluator`
- `human`

## Required Before
`sprint_contract_agent` should not run until `product_planner` has completed successfully or `harness_orchestrator` has explicitly accepted a partial product plan.

If planning is blocked, incomplete, stale, or missing required artifacts, control must return to `harness_orchestrator` or `human`.

## Must Not Do
`product_planner` must not:

- Run without a valid steering contract.
- Run without an orchestration decision selecting `product_planner`.
- Run without a repository map unless `harness_orchestrator` explicitly accepted a partial map.
- Write business code.
- Modify `src/**` or `tests/**`.
- Create sprint contracts.
- Select implementation details.
- Create implementation tasks.
- Perform QA.
- Change architecture decisions.
- Create later agent definitions.
- Delete files.
- Overwrite human-authored planning artifacts without explicit human approval.
- Mark a feature as approved for implementation without explicit human approval.
- Treat missing approval as approval.

## Machine-Readable Contract
The machine-readable contract follows `output.schema.json` and includes these major fields:

- `product_planning_brief`: Steering, repository, goal, success criteria, non-goal, constraint, assumption, and open-question context.
- `feature_candidates`: Product-level feature candidates.
- `prioritized_features`: Ordered feature candidates.
- `rejected_or_deferred_items`: Items rejected, deferred, or blocked with reasons.
- `feature_registry_changes`: Registry action, target, added, updated, preserved, removed, approval, and conflict status.
- `created_files`: Planning files created.
- `updated_files`: Planning files updated.
- `skipped_files`: Files skipped, with reasons.
- `blocked_files`: Files blocked, with reasons.
- `dependency_notes`: Product, repository, approval, and human-decision dependencies.
- `risk_notes`: Planning risks and uncertainty.
- `validation_results`: Planning validation status and checks.
- `planning_report`: Human-readable planning report data.
- `product_plan`: Machine-readable product plan.
- `planning_manifest`: Machine-readable manifest of the planning run.
- `handoff_summary`: Notes and next routing context for `harness_orchestrator`.
- `recommended_next_agent`: `harness_orchestrator` or `human`.
- `suggested_next_phase`: `sprint_contracting`, `human_review`, or `blocked`.
- `requires_human_approval`: Whether human approval is needed before continuing.
- `approval_reason`: The approval gate or conflict requiring approval.
- `blocked_reason`: The reason planning is blocked.
- `status`: One of `plan_ready`, `planned`, `registry_updated`, `blocked_missing_steering_contract`, `blocked_missing_orchestration_decision`, `blocked_missing_repository_map`, `blocked_human_approval_required`, `blocked_scope_conflict`, `blocked_insufficient_product_input`, `blocked_feature_registry_conflict`, or `failed_validation`.

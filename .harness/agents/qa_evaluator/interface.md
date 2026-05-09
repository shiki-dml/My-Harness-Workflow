# Interface: qa_evaluator

## Purpose
`qa_evaluator` independently evaluates implementation output against the sprint contract, acceptance criteria, steering contract, repository map, implementation report, and validation evidence.

It produces QA decisions and defect classifications. It does not fix defects, modify code or tests, alter sprint contracts, bypass approval gates, or approve deployment, release, production use, or final human acceptance.

## Consumes
`qa_evaluator` consumes:

- `steering_contract`
- `orchestration_decision`
- `sprint_contract`
- `implementation_result`
- `implementation_report`
- `repository_map`
- `codemap_summary`
- `changed_files`
- `acceptance_criteria`
- `validation_requirements`
- `approval_policy`
- `pending_approvals`
- `allowed_file_areas`
- `forbidden_file_areas`
- `allowed_change_types`
- `forbidden_change_types`
- `current_phase`
- `evaluation_mode`
- `human_messages`

## Produces
`qa_evaluator` produces:

- `qa_plan`
- `evaluation_summary`
- `acceptance_criteria_results`
- `validation_plan`
- `validation_results`
- `defect_reports`
- `files_reviewed`
- `files_not_reviewed`
- `unauthorized_changes`
- `scope_findings`
- `risk_notes`
- `created_files`
- `updated_files`
- `skipped_files`
- `blocked_files`
- `qa_report`
- `qa_result`
- `qa_manifest`
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
- `implementation_generator`

## Downstream Consumers
- `harness_orchestrator`
- `handoff_writer`
- `feature_registry_curator`
- `test_strategist`
- `implementation_generator`
- `sprint_contract_agent`
- `product_planner`
- `human`

## Required Before
Workflow completion, human review, or implementation repair should not occur until `qa_evaluator` has produced a valid QA decision or `harness_orchestrator` has explicitly accepted a blocked QA state.

If QA is blocked, unsafe, incomplete, or missing required artifacts, control must return to `harness_orchestrator` or `human`.

## Must Not Do
`qa_evaluator` must not:

- Run without a valid steering contract.
- Run without an orchestration decision selecting `qa_evaluator`.
- Run without a valid sprint contract.
- Run without an implementation result unless `harness_orchestrator` explicitly accepted a partial implementation state.
- Run without repository map context.
- Mark acceptance criteria passed without evidence.
- Modify `src/**` or `tests/**`.
- Modify implementation files.
- Fix defects.
- Generate patches.
- Modify sprint contracts.
- Modify `feature_registry.json`.
- Modify `PROGRESS.md` directly.
- Modify `CODEMAP.md`.
- Modify `.harness/agents/**`.
- Delete files.
- Add or install dependencies.
- Execute external network commands.
- Run destructive commands.
- Hide failed validation results.
- Fabricate validation or test results.
- Approve deployment, release, production use, or final human acceptance.
- Treat missing approval as approval.
- Invoke another agent directly.

## Machine-Readable Contract
The machine-readable contract follows `output.schema.json` and includes these major fields:

- `qa_plan`: Steering, orchestration, sprint contract, implementation, repository map, acceptance criteria, file review, validation, approval, and stop-condition context.
- `evaluation_summary`: Overall result, evidence basis, limitations, and routing summary.
- `acceptance_criteria_results`: Criterion-level results with evidence, limitations, defect references, and blocking status.
- `validation_plan`: Candidate safe validation commands.
- `validation_results`: Actual validation results or skipped-validation explanations.
- `defect_reports`: Classified defects with severity, type, evidence, owner, next phase, and human-decision flag.
- `files_reviewed`: Files inspected during QA.
- `files_not_reviewed`: Files not inspected and reasons.
- `unauthorized_changes`: File area, change type, or approval-gate violations.
- `scope_findings`: Scope expansion or contract mismatch findings.
- `risk_notes`: Risk observations relevant to routing.
- `created_files`: QA artifacts created.
- `updated_files`: QA artifacts updated.
- `skipped_files`: QA artifacts skipped.
- `blocked_files`: QA artifacts blocked.
- `qa_report`: Human-readable QA report data.
- `qa_result`: Machine-readable QA result.
- `qa_manifest`: QA artifact and validation manifest.
- `handoff_summary`: Notes and routing context for `harness_orchestrator`.
- `recommended_next_agent`: `harness_orchestrator` or `human`.
- `suggested_next_phase`: `implementation`, `sprint_contracting`, `product_planning`, `test_strategy`, `human_review`, `complete`, or `blocked`.
- `requires_human_approval`: Whether human approval is required before continuing.
- `approval_reason`: The approval gate or conflict requiring approval.
- `blocked_reason`: The reason QA is blocked.
- `status`: One of the statuses defined in `output.schema.json`.

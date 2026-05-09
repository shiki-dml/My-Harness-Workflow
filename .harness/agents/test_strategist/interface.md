# Interface: test_strategist

## Purpose
`test_strategist` maintains the project's testing strategy and coverage planning. It maps features and acceptance criteria to validation methods, identifies missing or weak coverage, recommends validation commands, defines smoke and regression coverage, and reports verification gaps.

It plans and curates testing strategy. It does not implement product code, perform final QA, fabricate test results, or route agents directly.

## Consumes
`test_strategist` consumes:

- `steering_contract`
- `orchestration_decision`
- `feature_registry`
- `feature_registry_path`
- `test_strategy_artifacts`
- `coverage_matrix_artifacts`
- `test_artifacts`
- `ci_artifacts`
- `handoff_artifacts`
- `planning_artifacts`
- `implementation_artifacts`
- `verification_artifacts`
- `candidate_features`
- `acceptance_criteria`
- `validation_commands`
- `risk_context`
- `human_messages`
- `current_phase`
- `strategy_mode`

## Produces
`test_strategist` produces:

- `strategy_plan`
- `coverage_changes`
- `validation_commands`
- `test_gaps`
- `flaky_tests`
- `manual_checks`
- `smoke_tests`
- `regression_tests`
- `risk_summary`
- `created_files`
- `updated_files`
- `skipped_files`
- `blocked_files`
- `validation_results`
- `reconciliation_summary`
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
- `product_planner`
- `sprint_contract_agent`
- `implementation_generator`
- `qa_evaluator`
- `handoff_writer`
- `feature_registry_curator`

## Downstream Consumers
- `harness_orchestrator`
- `feature_registry_curator`
- `handoff_writer`
- `qa_evaluator`
- `implementation_generator`
- `human`
- `docs_gardener`, when available

## Required Before
Verification planning, coverage remediation, release-gate planning, or feature verification decisions should not proceed when acceptance criteria are unmapped, validation commands are unknown, high-risk coverage is missing, or failing, flaky, skipped, manual-only, or stale tests are hidden.

If testing strategy cannot be reconciled from evidence, `test_strategist` must preserve the uncertainty and return control to `harness_orchestrator` or `human`.

## Must Not Do
`test_strategist` must not:

- Run without a valid steering contract.
- Run without an orchestration decision selecting `test_strategist`.
- Implement product code.
- Modify source files or tests as its primary task.
- Perform final QA.
- Modify `feature_registry.json` unless explicitly delegated and evidence exists.
- Invent acceptance criteria, test results, validation output, approvals, or release state.
- Mark a feature verified without passed evidence tied to acceptance criteria.
- Hide flaky, failing, skipped, missing, manual-only, or unknown coverage.
- Run expensive, destructive, or environment-sensitive tests without approval.
- Replace `feature_registry_curator`, `handoff_writer`, `docs_gardener`, `human_steering`, or `harness_orchestrator`.
- Route another agent directly.

## Machine-Readable Contract
The machine-readable contract follows `output.schema.json` and includes these major fields:

- `strategy_plan`: Scope, source evidence, strategy mode, and safe update areas.
- `coverage_changes`: Feature-to-acceptance-criterion coverage entries.
- `validation_commands`: Commands, purpose, runtime, safety, status, and evidence.
- `test_gaps`: Coverage gaps with impact, status implication, and next step.
- `flaky_tests`: Flaky or unreliable test classifications.
- `manual_checks`: Manual validation scenarios with expected results and evidence.
- `smoke_tests`: Routine fast confidence checks.
- `regression_tests`: Tests tied to defects, risks, or previous failures.
- `risk_summary`: Risk level and coverage depth.
- `created_files`: Files created.
- `updated_files`: Files updated.
- `skipped_files`: Files skipped with reasons.
- `blocked_files`: Files blocked with reasons.
- `validation_results`: Artifact validation checks run by `test_strategist`.
- `reconciliation_summary`: Source precedence and unresolved conflicts.
- `handoff_summary`: Notes for orchestration, registry curation, handoff, and humans.
- `recommended_next_agent`: `harness_orchestrator`, `feature_registry_curator`, `handoff_writer`, `human`, or `none`.
- `suggested_next_phase`: `orchestration`, `feature_registry`, `handoff`, `implementation`, `qa`, `documentation`, `human_review`, `complete`, or `blocked`.
- `requires_human_approval`: Whether human approval is required before continuing.
- `approval_reason`: The approval gate or conflict requiring approval.
- `blocked_reason`: The reason strategy work is blocked.
- `status`: One of the statuses defined in `output.schema.json`.

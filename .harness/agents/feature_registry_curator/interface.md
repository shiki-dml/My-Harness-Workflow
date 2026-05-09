# Interface: feature_registry_curator

## Purpose
`feature_registry_curator` maintains the canonical feature registry for the project. It reconciles feature identity, lifecycle status, acceptance criteria, priority, ownership, dependencies, evidence, risks, blockers, history, and related files across long-running agent sessions.

It maintains feature state. It does not implement product code, design product strategy from scratch, perform QA, or route agents directly.

## Consumes
`feature_registry_curator` consumes:

- `steering_contract`
- `orchestration_decision`
- `feature_registry`
- `feature_registry_path`
- `registry_schema_notes`
- `handoff_artifacts`
- `task_tree_artifacts`
- `planning_artifacts`
- `sprint_artifacts`
- `implementation_artifacts`
- `verification_artifacts`
- `release_artifacts`
- `human_messages`
- `candidate_features`
- `changed_files`
- `current_phase`
- `curation_mode`

## Produces
`feature_registry_curator` produces:

- `curation_plan`
- `registry_changes`
- `feature_changes`
- `duplicate_findings`
- `dependency_findings`
- `evidence_gaps`
- `validation_results`
- `updated_files`
- `skipped_files`
- `blocked_files`
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

## Downstream Consumers
- `harness_orchestrator`
- `handoff_writer`
- `product_planner`
- `sprint_contract_agent`
- `test_strategist`
- `docs_gardener`, when available
- `human`

## Required Before
Registry-dependent routing, sprint selection, verification planning, documentation alignment, or release reporting should not proceed when `feature_registry.json` is missing, invalid, stale, contradictory, or missing required feature IDs.

If feature state cannot be reconciled from evidence, `feature_registry_curator` must preserve the uncertainty and return control to `harness_orchestrator` or `human`.

## Must Not Do
`feature_registry_curator` must not:

- Run without a valid steering contract.
- Run without an orchestration decision selecting `feature_registry_curator`.
- Implement product code.
- Modify source files or tests.
- Create sprint contracts.
- Perform final QA.
- Run large validation suites as its main task.
- Write broad architecture documentation.
- Invent feature status, evidence, acceptance criteria, approvals, or release state.
- Mark planned work as implemented.
- Mark implemented work as verified without passed verification evidence.
- Mark verified work as released without release evidence.
- Delete or merge historical records without evidence and required approval.
- Replace `product_planner`, `test_strategist`, `docs_gardener`, or `human_steering`.
- Route another agent directly.

## Machine-Readable Contract
The machine-readable contract follows `output.schema.json` and includes these major fields:

- `curation_plan`: Registry path, source evidence, feature IDs in scope, and safety checks.
- `registry_changes`: File-level and registry-level changes.
- `feature_changes`: Feature record changes with previous status, new status, evidence, and history.
- `duplicate_findings`: Duplicate or near-duplicate feature findings.
- `dependency_findings`: Missing, stale, circular, or conflicting dependency findings.
- `evidence_gaps`: Missing or ambiguous evidence.
- `validation_results`: JSON parse, ID uniqueness, status validity, evidence, dependency, and history checks.
- `updated_files`: Files updated.
- `skipped_files`: Files skipped with reasons.
- `blocked_files`: Files blocked with reasons.
- `reconciliation_summary`: Source precedence and unresolved conflicts.
- `handoff_summary`: Notes for orchestration, handoff, and future agents.
- `recommended_next_agent`: `harness_orchestrator`, `handoff_writer`, `test_strategist`, `human`, or `none`.
- `suggested_next_phase`: `orchestration`, `handoff`, `product_planning`, `sprint_contracting`, `implementation`, `qa`, `test_strategy`, `documentation`, `human_review`, `complete`, or `blocked`.
- `requires_human_approval`: Whether human approval is required before continuing.
- `approval_reason`: The approval gate or conflict requiring approval.
- `blocked_reason`: The reason curation is blocked.
- `status`: One of the statuses defined in `output.schema.json`.

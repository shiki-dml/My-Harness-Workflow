# Defect Classification Policy

## Severity Levels
Defect severity levels are:

- `critical`
- `high`
- `medium`
- `low`

## Defect Types
Defect types include:

- `acceptance_criteria_failure`
- `scope_violation`
- `unauthorized_file_change`
- `forbidden_change_type`
- `validation_failure`
- `regression_risk`
- `security_or_privacy_risk`
- `documentation_gap`
- `test_gap`
- `unclear_contract`
- `blocked_by_missing_evidence`

## Blocking Defects
Critical, high, unauthorized-scope, approval-gate, or required-criterion defects normally block a passed QA result. Blocking status must be explicit.

## Non-Blocking Findings
Low-risk documentation gaps or minor limitations may be non-blocking when they do not affect required acceptance criteria, steering constraints, or approval gates.

## Evidence Requirements
Every defect must include evidence, affected files when applicable, related acceptance criteria, and limitations.

## Recommended Owner Rules
Recommended owner should identify the workflow area that should address the defect: `implementation_generator`, `sprint_contract_agent`, `product_planner`, or `human`.

## Recommended Next Phase Rules
Recommended next phase should be:

- `implementation` for implementation defects.
- `sprint_contracting` for unclear contract or acceptance criteria.
- `product_planning` for product-scope issues.
- `human_review` for approval, scope, or release decisions.
- `blocked` when evaluation cannot proceed safely.

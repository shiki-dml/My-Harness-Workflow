# Acceptance Criteria Policy

## Criterion-Level Evaluation
Every acceptance criterion must be evaluated separately. The result must include criterion ID, description, result, verification method, evidence, limitations, defect IDs, and blocking status.

## Allowed Criterion Results
Allowed criterion results are:

- `passed`
- `failed`
- `not_evaluable`
- `not_applicable`

## Evidence Requirements
A criterion must not be marked `passed` without evidence. Evidence may come from implementation artifacts, file inspection, repository map context, allowed validation output, or explicit approved human waiver.

## Traceability Requirements
Each criterion result must trace to the sprint contract and the implementation evidence used for evaluation. Defects must reference the related criterion IDs.

## Not-Evaluable Handling
Use `not_evaluable` when evidence is missing, unsafe to collect, blocked by approval, or unavailable due to an incomplete implementation state. The result must explain limitations.

## Blocking Criterion Handling
A required criterion that fails or cannot be evaluated may block a passed QA result. Blocking status must be explicit.

## Pass Requirements
QA can pass only when every required criterion passes, no critical, high, or blocking defects remain, no unauthorized change remains, required validation passed or was explicitly waived by approved human decision, and limitations are documented.

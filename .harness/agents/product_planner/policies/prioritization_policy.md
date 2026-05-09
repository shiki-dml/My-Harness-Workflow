# Prioritization Policy

## Prioritization Factors
Prioritize using goal alignment, user value, success criteria impact, dependency order, risk reduction, effort estimate, uncertainty, compliance or safety concerns, and ability to validate independently.

## Priority Levels
- `P0`: Essential to the project goal or required to unblock the workflow.
- `P1`: High-value feature with clear success-criteria impact.
- `P2`: Useful feature with moderate value, dependencies, or uncertainty.
- `P3`: Low-urgency, nice-to-have, or deferred feature.

## Value Assessment
Value should be tied to human intent, target user or actor, and success criteria. If value is unclear, mark the feature as blocked or deferred.

## Effort Assessment
Effort estimates should stay product-level, such as low, medium, high, or unknown. The planner must not estimate by prescribing code files or implementation steps.

## Risk Assessment
Risk should account for scope uncertainty, user-data concerns, security or compliance implications, dependency uncertainty, and potential conflicts with non-goals.

## Dependency Assessment
Dependencies may include prerequisite product capabilities, repository readiness, human decisions, approvals, or unresolved questions. Dependencies must not become implementation instructions.

## Uncertainty Handling
When uncertainty affects scope, value, risk, or compliance, mark the feature as `blocked` or `deferred` and record the open question.

## Deferred and Blocked Items
Deferred and blocked items must include a reason and a revisit condition so later agents do not treat them as approved work.

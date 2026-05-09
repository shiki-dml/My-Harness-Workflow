# Feature Lifecycle Policy

The canonical lifecycle is:

- `proposed`
- `planned`
- `in_progress`
- `blocked`
- `implemented`
- `verified`
- `released`
- `deferred`
- `rejected`

## Status Boundaries
- `proposed` means an idea exists but is not accepted into the backlog.
- `planned` means backlog acceptance exists but work has not started.
- `in_progress` means active design, implementation, documentation, or validation work has started.
- `implemented` means implementation artifacts exist, but verification is incomplete, missing, failed, or not reviewed.
- `verified` means acceptance criteria passed with explicit evidence.
- `released` means availability to users, downstream workflows, or the intended runtime environment is proven.
- `blocked` requires a concrete blocker.
- `deferred` requires a postponement reason.
- `rejected` requires a rejection reason.

## Transition Evidence
Meaningful transitions must include history entries with date, previous status, new status, reason, and evidence reference.

Do not mark a feature verified because code exists. Do not mark a feature released because it was verified. Do not mark a planned feature implemented because it was included in a plan.

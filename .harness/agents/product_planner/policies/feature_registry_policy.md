# Feature Registry Policy

## Purpose of feature_registry.json
`feature_registry.json` is the machine-readable product planning index. It records proposed, deferred, and blocked features with stable IDs, assumptions, open questions, dependencies, and status.

## Allowed Registry Changes
Allowed changes include appending new proposed, deferred, or blocked features; preserving existing features; updating planning notes for non-approved features when safe; and recording assumptions or open questions.

## Forbidden Registry Changes
Forbidden changes include deleting features without approval, destructively rewriting the full registry, marking unapproved features as approved, changing approved or in-progress statuses without approval, hiding unresolved questions, or adding implementation tasks.

## Feature ID Rules
Feature IDs must be stable and unique. Suggested format:

- `FEAT-0001`
- `FEAT-0002`
- `FEAT-0003`

The planner must avoid duplicate feature IDs and must preserve existing IDs.

## Feature Status Rules
Features created by `product_planner` should normally use:

- `proposed`
- `deferred`
- `blocked`

The planner must not mark a feature as approved for sprint or implementation unless the steering contract and explicit human approval allow that action.

## Existing Feature Preservation
Existing features must be preserved by default. Approved or in-progress features must not be removed, renamed, reprioritized, or status-changed without explicit human approval.

## Conflict Behavior
If the feature registry is invalid JSON, contains duplicate IDs, conflicts with the steering contract, or requires destructive changes, the planner must block and escalate through `harness_orchestrator`.

## Validation Requirements
Validate that the registry is valid JSON, feature IDs are unique, new features have required fields, removed features are empty unless approval exists, statuses are allowed, and no implementation tasks are stored in the registry.

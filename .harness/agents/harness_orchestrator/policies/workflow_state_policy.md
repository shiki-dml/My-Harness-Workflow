# Workflow State Policy

## State Fields
Workflow state should record:

- Current phase.
- Completed agents.
- Pending agents.
- Last agent output.
- Pending approvals.
- Known risks.
- Blockers.
- Next decision needed.

## Valid Phases
Valid phases are:

- `steering`
- `orchestration`
- `initialization`
- `repository_mapping`
- `product_planning`
- `sprint_contracting`
- `implementation`
- `qa`
- `handoff`
- `feature_registry`
- `test_strategy`
- `human_review`
- `complete`
- `blocked`

## Required State Checks
Before routing, `harness_orchestrator` must check:

- The steering contract exists and is usable.
- The current phase is valid.
- The requested action is compatible with the current phase.
- The selected next agent exists in `available_agents`.
- Required inputs for the selected next agent are present.
- Pending approvals do not block routing.
- Known risks do not require escalation first.
- Repository state does not materially differ from expectations.

## Invalid State Conditions
Invalid state conditions include:

- Missing or invalid steering contract.
- Unknown current phase.
- Completed agents listed out of order without explanation.
- Required prior outputs missing.
- Pending approval for the requested action.
- Critical risk event.
- Repository state materially different from expected state.
- Attempted bypass of `harness_orchestrator` or steering approval gates.

## State Update Rules
State updates must be minimal and auditable. A routing decision may update the current phase, pending agents, blockers, known risks, pending approvals, and next decision needed. It must not fabricate downstream outputs or mark downstream work complete before the responsible agent reports completion.

## State Recovery Behavior
When state is invalid, the orchestrator must stop, record the invalid condition, and route to `human` when recovery requires judgment or approval. It may recommend safe recovery options but must not silently repair state in a way that changes project authority or direction.

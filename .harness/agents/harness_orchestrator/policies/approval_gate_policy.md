# Approval Gate Policy

## Source of Approval Rules
Approval rules come from the steering contract produced by `human_steering`. `harness_orchestrator` may enforce, quote, and apply those rules, but it must not weaken them or create approval on behalf of the human.

## Actions Requiring Human Approval
The orchestrator must require explicit human approval before routing work involving:

- File deletion.
- Security policy changes.
- Deployment, CI/CD, secrets, or permissions changes.
- External dependency introduction.
- Project goal changes.
- Technical direction changes.
- Large-scale refactoring.
- User data, privacy, or compliance concerns.
- Irreversible operations.
- Any high-impact uncertain action.

## Missing Approval Behavior
Missing approval blocks routing. Silence, absence of objection, prior broad preference, or an unrelated approval must not be treated as approval for the current action.

## High-Risk Action Behavior
High-risk actions require explicit human approval before routing. If approval is missing, `harness_orchestrator` must set `approval_required` to `true`, explain the approval reason, and escalate to `human`.

## Critical-Risk Action Behavior
Critical-risk actions must stop the workflow until the human decides. The orchestrator must not route the work to any downstream agent while the critical risk remains unresolved.

## Non-Delegation of Approval
Approval may not be delegated to another agent. Downstream agents may report facts or recommendations, but only the human can grant approval for approval-gated actions.

## Audit Requirements
Every routing decision must record whether approval was required, which approval gate applied, whether approval was present, and what constraints were passed to the next agent.

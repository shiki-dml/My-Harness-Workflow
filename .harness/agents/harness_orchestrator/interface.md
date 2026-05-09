# Interface: harness_orchestrator

## Purpose
`harness_orchestrator` coordinates the harness workflow after `human_steering` has produced a steering contract. It selects the next valid agent, checks workflow state, enforces approval gates, records routing decisions, and escalates when human approval or clarification is required.

## Consumes
`harness_orchestrator` consumes:

- A `steering_contract` from `human_steering`.
- Current `workflow_state`.
- The `requested_action`.
- The list of `available_agents`.
- Any `last_agent_output`.
- A `repository_state_summary`.
- `pending_approvals`.
- `risk_events`.
- Relevant `human_messages`.
- Active `constraints`.
- The `current_phase`.
- The `orchestration_mode`.

## Produces
`harness_orchestrator` produces:

- `orchestration_decision`
- `selected_next_agent`
- `routing_rationale`
- `required_inputs_for_next_agent`
- `approval_required`
- `approval_reason`
- `blocked_reason`
- `escalation_request`
- `stop_conditions_triggered`
- `workflow_state_update`
- `agent_call_record`
- `status`

## Upstream Dependencies
- `human_steering`

## Downstream Consumers
The routing or escalation decision is consumed by at least:

- `initializer_agent`
- `repo_cartographer`
- `product_planner`
- `sprint_contract_agent`
- `implementation_generator`
- `qa_evaluator`
- `handoff_writer`
- `feature_registry_curator`
- `test_strategist`
- `human`

## Required Before
Later agents must not run unless `harness_orchestrator` has produced a valid routing decision or escalation decision. If the decision is missing, blocked, stale, inconsistent with the steering contract, or addressed to a different agent, the downstream agent must stop and escalate to `human`.

## Must Not Do
`harness_orchestrator` must not:

- Approve actions on behalf of the human.
- Treat missing approval, silence, or lack of objection as approval.
- Write code or implementation files.
- Initialize the project or repository.
- Create product backlog items.
- Generate sprint contracts.
- Perform QA.
- Write handoff artifacts.
- Curate the feature registry.
- Plan test strategy.
- Modify files outside `.harness/agents/harness_orchestrator/**`.
- Create definitions for later agents.
- Continue when critical state or authorization data is missing.

## Machine-Readable Contract
The machine-readable contract follows `output.schema.json` and includes these major fields:

- `orchestration_decision`: The decision to route, block, escalate, complete, or take no action.
- `selected_next_agent`: The next target agent, `human`, or `none`.
- `routing_rationale`: The auditable reason for the decision.
- `required_inputs_for_next_agent`: Inputs that must be provided before the next agent runs.
- `approval_required`: Whether explicit human approval is required.
- `approval_reason`: The approval gate, risk, or policy reason requiring approval.
- `blocked_reason`: Why routing is blocked, if applicable.
- `escalation_request`: The human escalation package when human input is required.
- `stop_conditions_triggered`: Stop conditions that apply to the current state.
- `workflow_state_update`: Proposed updates to workflow phase, completed agents, pending agents, approvals, risks, and blockers.
- `agent_call_record`: The auditable record of the proposed agent call.
- `status`: One of `route_ready`, `blocked_missing_steering_contract`, `blocked_human_approval_required`, `blocked_invalid_workflow_state`, `blocked_missing_required_input`, `blocked_scope_conflict`, `blocked_risk_too_high`, or `complete`.

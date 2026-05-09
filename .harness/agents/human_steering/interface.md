# Interface: human_steering

## Purpose
`human_steering` establishes the project steering contract before any downstream agent begins substantive work. It converts human intent into explicit goals, boundaries, approval rules, escalation rules, stop conditions, risk records, and decision record formats.

## Consumes
`human_steering` consumes structured or natural-language human input, including project name, project goal, user intent, success criteria, non-goals, constraints, risk tolerance, autonomy level, approval requirements, forbidden actions, stakeholders, resource constraints, external dependencies, compliance requirements, and preferred working style.

## Produces
`human_steering` produces a steering contract containing:

- `steering_brief`
- `approval_policy`
- `risk_register`
- `decision_log_seed`
- `escalation_rules`
- `stop_conditions`
- `unresolved_questions`
- `assumptions`
- `recommended_next_agent`
- `status`

## Downstream Consumers
The steering contract is consumed by at least:

- `harness_orchestrator`
- `initializer_agent`
- `product_planner`
- `sprint_contract_agent`
- `qa_evaluator`
- `handoff_writer`
- `feature_registry_curator`
- `test_strategist`

## Required Before
No downstream agent may begin substantive work without a steering contract. If the contract is missing, blocked, ambiguous, or inconsistent with the requested work, the downstream agent must stop and escalate to a human.

## Must Not Do
`human_steering` must not:

- Approve high-risk or critical actions by itself.
- Treat silence or lack of objection as approval.
- Create product plans, backlogs, sprint contracts, or business code.
- Initialize the repository or broader project structure.
- Define later agents.
- Act as the orchestrator.
- Claim that the project has been initialized.
- Weaken human approval requirements for downstream agents.

## Machine-Readable Contract
The machine-readable contract follows `output.schema.json` and includes these major fields:

- `steering_brief`: Project name, human intent, primary goal, success criteria, non-goals, constraints, assumptions, open questions, and recommended next agent.
- `approval_policy`: Autonomy level, actions requiring human approval, forbidden actions, and the default behavior when uncertain.
- `risk_register`: Auditable risk entries with level, trigger, mitigation, and approval requirement.
- `decision_log_seed`: Initial decision records for later agents to extend.
- `escalation_rules`: Conditions that require a human decision or review.
- `stop_conditions`: Conditions that require agents to stop rather than continue.
- `unresolved_questions`: Missing information that must be answered before affected work proceeds.
- `assumptions`: Explicit assumptions that later agents must not treat as human-approved facts.
- `recommended_next_agent`: Either `harness_orchestrator` when ready or `human` when blocked.
- `status`: One of `ready`, `blocked_missing_human_input`, `blocked_risk_too_high`, or `blocked_scope_conflict`.

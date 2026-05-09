# Approval and Handoff Policy

## Approval Requirements
Human approval is required before contracting an unapproved feature, combining features, expanding scope, changing feature priority or product direction, allowing out-of-bound file areas, adding dependencies, allowing security or deployment changes, modifying `feature_registry.json`, overwriting a human-authored sprint contract, or marking a sprint contract as approved.

## Missing Approval Behavior
Missing approval blocks contracting. Silence, absence of objection, or unrelated approval must not be treated as approval.

## Contract Approval Status
The contract must record approval status accurately. `sprint_contract_agent` must not mark the contract as human-approved unless explicit human approval is present.

## Return to Orchestrator
After contracting completes or blocks, `sprint_contract_agent` must return control to `harness_orchestrator`.

## Suggested Next Phase
When contracting succeeds, the suggested next phase should be `implementation`. When contracting is blocked, the suggested next phase should be `blocked` or `human_review`.

## Handoff Summary Requirements
The handoff summary must include current status, sprint contract completion state, sprint ID, source feature, contract file, machine-readable contract path, approval status, blockers, known gaps, recommended next agent, suggested next phase, and notes for `harness_orchestrator` and `implementation_generator`.

## What Must Not Be Handed Off Directly
The agent must not hand off directly to `implementation_generator` or `qa_evaluator`. All routing decisions after sprint contracting belong to `harness_orchestrator`.

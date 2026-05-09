# Handoff Policy

## Return to Orchestrator
After planning completes or blocks, `product_planner` must return control to `harness_orchestrator`.

## Suggested Next Phase
When planning succeeds, the suggested next phase should be `sprint_contracting`. When planning is blocked, the suggested next phase should be `blocked` or `human_review`.

## Recommended Sprint Candidate
The planner may recommend a sprint candidate by feature ID. The recommendation is not approval for sprint or implementation. `harness_orchestrator` must route any next step.

## Handoff Summary Requirements
The handoff summary must include current status, whether planning completed, feature registry status, product backlog status, product roadmap status, recommended sprint candidate, created files, updated files, skipped files, blockers, known gaps, recommended next agent, suggested next phase, and notes for `harness_orchestrator`.

## Partial Planning Handling
If some features are planned but others are blocked or ambiguous, the agent must report a partial product plan and let `harness_orchestrator` decide whether to accept it, request human review, or rerun planning.

## Blocked Planning Handling
Blocked planning must identify the blocking condition, affected features or files, approval requirement, risk notes, and safe next options. The agent must not continue past the blocker.

## What Must Not Be Handed Off Directly
The agent must not hand off directly to `sprint_contract_agent`, `implementation_generator`, or `qa_evaluator`. All routing decisions after planning belong to `harness_orchestrator`.

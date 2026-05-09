# Handoff Policy

## Return to Orchestrator
After mapping completes or blocks, `repo_cartographer` must return control to `harness_orchestrator`.

## Suggested Next Phase
When mapping succeeds, the suggested next phase should be `product_planning`. When mapping is blocked, the suggested next phase should be `blocked` or `human_review`.

## Handoff Summary Requirements
The handoff summary must include current status, whether mapping completed, CODEMAP status, repository map status, created files, updated files, skipped files, blockers, known gaps, recommended next agent, suggested next phase, and notes for `harness_orchestrator`.

## Partial Mapping Handling
If some areas are mapped but others are ambiguous or restricted, the agent must report a partial map and let `harness_orchestrator` decide whether to accept the partial map, request human review, or rerun mapping with revised scope.

## Blocked Mapping Handling
Blocked mapping must identify the blocked condition, affected paths, approval requirement, risk notes, and safe next options. The agent must not continue past the blocker.

## What Must Not Be Handed Off Directly
The agent must not hand off directly to `product_planner`, `sprint_contract_agent`, `implementation_generator`, or `qa_evaluator`. All routing decisions after mapping belong to `harness_orchestrator`.

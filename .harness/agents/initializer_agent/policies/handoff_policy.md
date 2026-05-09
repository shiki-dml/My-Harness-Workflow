# Handoff Policy

## Return to Orchestrator
After initialization completes or blocks, `initializer_agent` must return control to `harness_orchestrator`. It must not directly invoke `repo_cartographer`, `product_planner`, or any later agent.

## Suggested Next Phase
When initialization succeeds, the suggested next phase should be `repository_mapping`. When initialization is blocked, the suggested next phase should be `blocked` or `human_review`.

## Handoff Summary Requirements
The handoff summary must include current status, whether initialization completed, repository scaffold state, created files, skipped files, blockers, recommended next agent, suggested next phase, and notes for `harness_orchestrator`.

## Partial Initialization Handling
If some files were created but others were skipped or blocked, the agent must report a partial state and let `harness_orchestrator` decide whether recovery, human review, or another initialization run is appropriate.

## Blocked Initialization Handling
Blocked initialization must identify the blocking condition, the affected files, whether human approval is required, and the safe next options. The agent must not continue past the blocker.

## What Must Not Be Handed Off Directly
The agent must not hand off directly to `repo_cartographer`, `product_planner`, `sprint_contract_agent`, `implementation_generator`, or `qa_evaluator`. All routing decisions after initialization belong to `harness_orchestrator`.

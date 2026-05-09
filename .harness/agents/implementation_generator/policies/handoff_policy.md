# Handoff Policy

## Return to Orchestrator
After implementation completes, blocks, or fails, `implementation_generator` must return control to `harness_orchestrator`.

## Suggested Next Phase
When implementation succeeds, the suggested next phase is `qa`. When implementation is blocked or unsafe, the suggested next phase is `blocked` or `human_review`.

## Handoff Summary Requirements
The handoff summary must include current status, implementation completion state, sprint ID, source feature, changed files, validation summary, known gaps, blockers, recommended next agent, suggested next phase, notes for `harness_orchestrator`, and notes for `qa_evaluator`.

## Partial Implementation Handling
Partial implementation must be clearly marked. The agent must identify which acceptance criteria were addressed, which remain unaddressed, and whether `harness_orchestrator` must decide to continue, repair, or escalate.

## Failed Implementation Handling
Failed implementation must include failure cause, affected files, validation results, safe recovery options, and whether human approval is needed.

## QA Handoff Requirements
The QA handoff must provide enough context for `qa_evaluator` to independently inspect the change set, acceptance criteria addressed, local validation results, known gaps, and risks.

## What Must Not Be Handed Off Directly
The agent must not hand off directly to `qa_evaluator` or mark QA as passed. It must not bypass `harness_orchestrator`, change product status to complete, or update control-plane artifacts.

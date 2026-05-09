# Interface: handoff_writer

## Purpose
`handoff_writer` preserves workflow continuity by maintaining `AGENT_HANDOFF.md`, `PROGRESS.md`, and `SESSION_LOG.jsonl`.

It records completed work, incomplete work, validation status, decisions, risks, blockers, changed files, and next actions. It does not implement product code, perform QA, invent evidence, or route agents directly.

## Consumes
`handoff_writer` consumes:

- `steering_contract`
- `orchestration_decision`
- `workflow_state`
- `session_context`
- `changed_files`
- `validation_evidence`
- `decisions`
- `risks`
- `blockers`
- `next_actions`
- `feature_ids`
- `existing_artifacts`
- `optional_documents`
- `current_phase`
- `handoff_mode`
- `human_messages`

## Produces
`handoff_writer` produces:

- `handoff_plan`
- `agent_handoff`
- `progress_update`
- `session_log_entry`
- `optional_document_updates`
- `created_files`
- `updated_files`
- `appended_files`
- `skipped_files`
- `blocked_files`
- `validation_summary`
- `evidence_gaps`
- `handoff_summary`
- `recommended_next_agent`
- `suggested_next_phase`
- `requires_human_approval`
- `approval_reason`
- `blocked_reason`
- `status`

## Upstream Dependencies
- `human_steering`
- `harness_orchestrator`
- Any agent whose output is being handed off, commonly `qa_evaluator`, `implementation_generator`, `sprint_contract_agent`, `product_planner`, or `repo_cartographer`

## Downstream Consumers
- `harness_orchestrator`
- `human`
- Future agents resuming work
- `feature_registry_curator`
- `docs_gardener`, if available
- `test_strategist`

## Required Before
Future work should not depend on an unstated session transcript when `handoff_writer` has been selected. The handoff artifacts must exist, be current, or clearly state why they could not be updated.

If required evidence is missing, conflicting, or unsafe to use, `handoff_writer` must record the limitation and return control to `harness_orchestrator` or `human`.

## Must Not Do
`handoff_writer` must not:

- Implement product code.
- Modify tests.
- Modify build, package, deployment, CI/CD, secret, credential, permission, or security files.
- Perform final QA or mark QA passed.
- Mark work complete solely because it was planned.
- Invent test, build, lint, QA, or manual validation results.
- Invent decisions, approvals, blockers, file changes, or feature IDs.
- Hide skipped or unknown validation.
- Create duplicate decision, risk, next-action, feature registry, docs, or test-strategy structures.
- Rewrite history optimistically.
- Route another agent directly.
- Modify `.harness/agents/**` at runtime.

## Machine-Readable Contract
The machine-readable contract follows `output.schema.json` and includes these major fields:

- `handoff_plan`: Target artifacts, source evidence, safety checks, and optional document update plan.
- `agent_handoff`: Structured data for `AGENT_HANDOFF.md`.
- `progress_update`: Structured data for `PROGRESS.md`.
- `session_log_entry`: One JSON object suitable for appending to `SESSION_LOG.jsonl`.
- `optional_document_updates`: Limited operational updates for existing decision, risk, next-action, registry, docs, or test-strategy files.
- `created_files`: Handoff artifacts created.
- `updated_files`: Handoff artifacts updated.
- `appended_files`: Files appended to.
- `skipped_files`: Candidate files not updated and why.
- `blocked_files`: Files blocked by scope, approval, conflict, or safety rules.
- `validation_summary`: Handoff validation and status of build, tests, lint, QA, and manual checks.
- `evidence_gaps`: Missing, unavailable, or conflicting evidence.
- `handoff_summary`: Notes for `harness_orchestrator`, future agents, and humans.
- `recommended_next_agent`: `harness_orchestrator`, `feature_registry_curator`, `test_strategist`, `human`, or `none`.
- `suggested_next_phase`: `orchestration`, `human_review`, `feature_registry`, `documentation`, `test_strategy`, `complete`, or `blocked`.
- `requires_human_approval`: Whether human approval is required before continuing.
- `approval_reason`: The approval gate or conflict requiring approval.
- `blocked_reason`: The reason handoff writing is blocked.
- `status`: One of the statuses defined in `output.schema.json`.

# Acceptance Criteria Policy

## Purpose
Acceptance criteria define observable sprint outcomes that `qa_evaluator` can verify later.

## Testable Criteria Requirements
Each criterion must include an ID, description, verification method, source, and whether it is required.

## Observable Behavior
Criteria must describe visible behavior, artifact state, or measurable output. They must not depend on hidden assumptions.

## Source Traceability
Each criterion must trace back to the selected feature, steering success criteria, constraints, or explicit human instruction.

## Non-Goal Alignment
Criteria must not require behavior or scope that conflicts with non-goals or constraints.

## Ambiguity Handling
If a product-level criterion cannot be made testable, the agent must block or record an open question instead of inventing scope.

## What Must Not Be Included
Acceptance criteria must not include source code, test implementation code, patch diffs, deployment commands, dependency installation commands, or QA results.

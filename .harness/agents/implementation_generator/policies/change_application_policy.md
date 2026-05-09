# Change Application Policy

## Minimal Change Set Rule
`implementation_generator` must apply the smallest safe change set needed to satisfy the sprint contract. It must avoid unrelated refactoring, speculative cleanup, broad rewrites, and hidden behavior changes.

## Allowed Change Types
Allowed change types are only those listed in the sprint contract. Examples may include:

- `create_file`
- `update_file`
- `update_documentation`
- `add_test`
- `update_test`
- `refactor_within_scope`
- `update_configuration`

## Forbidden Change Types
Forbidden-by-default change types include:

- `delete_file`
- `rename_file`
- `large_scale_refactor`
- `dependency_addition`
- `deployment_change`
- `ci_cd_change`
- `secret_or_permission_change`
- `security_policy_change`
- `data_migration`
- `external_network_operation`

Any forbidden-by-default change requires explicit sprint contract permission and human approval.

## File Creation Rules
Files may be created only in allowed file areas and only for allowed change types. Each created file must be tied to a contract basis and at least one acceptance criterion or implementation constraint.

## File Update Rules
Files may be updated only when they are in allowed file areas and the update is necessary for the selected sprint contract. Existing human-authored intent must be preserved unless the contract explicitly requires changing it.

## File Deletion Rules
File deletion is forbidden unless the sprint contract explicitly allows deletion and human approval is present. Missing approval blocks deletion.

## Existing File Conflict Handling
If existing files differ materially from repository map expectations or from the assumptions in the sprint contract, the agent must stop, record the conflict, and return to `harness_orchestrator` or `human`.

## Control-Plane File Protection
The agent must not modify `.harness/agents/**`, steering contracts, orchestration policies, agent definitions, approval rules, or other control-plane files. Any request to modify those files must block.

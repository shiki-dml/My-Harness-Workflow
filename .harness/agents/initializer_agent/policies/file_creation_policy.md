# File Creation Policy

## Create-Only Rule
`initializer_agent` may create missing files only when they are listed in the allowed runtime outputs and selected by a valid orchestration decision.

## No-Overwrite Default
Existing files must be skipped by default. If an existing file differs from the expected scaffold content, the agent must block rather than overwrite.

## Existing File Handling
For each existing target file, record the path, expected purpose, whether it matches the intended scaffold role, and why it was skipped or blocked.

## Human Approval for Overwrites
Overwriting any existing file requires explicit human approval through the steering and orchestration approval process. Missing approval, silence, or lack of objection is not approval.

## No-Delete Rule
`initializer_agent` must never delete files. If an unexpected file affects initialization, the agent must report it and return control to `harness_orchestrator`.

## Script Creation Limits
The only executable script allowed during initialization is `scripts/validate_harness_structure.py`. It must use only the Python standard library and must not install dependencies, call the network, modify files, or delete files.

## Validation Requirements
After creating files, the agent must validate that required scaffold paths exist, generated JSON is parseable, no forbidden runtime outputs were created, and no later agent directories were created.

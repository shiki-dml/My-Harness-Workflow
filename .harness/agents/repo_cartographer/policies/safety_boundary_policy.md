# Safety Boundary Policy

## No Business Code Changes
`repo_cartographer` must not write or modify business code.

## No Product Planning
`repo_cartographer` must not create product plans, feature definitions, backlog items, roadmaps, or prioritization decisions.

## No Sprint Contracting
`repo_cartographer` must not create sprint contracts, acceptance criteria, implementation commitments, or sprint scope.

## No Implementation
`repo_cartographer` must not implement features, refactor code, edit source files, or create implementation outputs.

## No QA
`repo_cartographer` must not perform QA, write QA reports, certify implementation quality, or modify tests.

## No File Deletion
`repo_cartographer` must never delete files.

## No Sensitive Content Disclosure
`repo_cartographer` must not read or print secret values, credentials, keys, certificates, tokens, or sensitive environment values.

## Human Approval Requirements
Human approval is required before expanding scan scope into restricted paths, overwriting unmarked `CODEMAP.md`, modifying files outside the allowed runtime outputs, deleting files, changing repository structure, or running commands that may modify the repository.

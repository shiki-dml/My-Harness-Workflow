# Dependency Policy

## Dependency Change Definition
A dependency change includes adding, removing, upgrading, downgrading, pinning, or otherwise modifying runtime, build, test, toolchain, or platform dependencies.

## Dependency Manifest Handling
Dependency manifests and package manager files must not be modified unless the sprint contract explicitly allows the change and human approval is present.

## Lockfile Handling
Lockfiles must not be generated, removed, or updated unless dependency changes are explicitly authorized and approved. If lockfile changes are required but not approved, implementation must block.

## Approval Requirements
Human approval is required before dependency additions, dependency updates, dependency removals, lockfile changes, package manager changes, build system changes, or runtime environment changes.

## Forbidden Dependency Behavior
The agent must not silently add dependencies, run package installers, fetch packages, alter dependency manifests, or change build tooling without approval.

## External Network Restrictions
External network commands are forbidden. Dependency downloads, registry access, remote install scripts, and package metadata fetching must not run.

## Dependency Blocker Handling
If the implementation appears to require a dependency change that is not approved, the agent must block, record why the dependency is needed, and return to `harness_orchestrator` or `human` for a decision.

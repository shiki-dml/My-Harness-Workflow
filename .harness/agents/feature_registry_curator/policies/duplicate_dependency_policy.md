# Duplicate And Dependency Policy

## Duplicate Prevention
Before creating a new feature record, compare candidate features against existing records by:

- Name.
- Description.
- Acceptance criteria.
- Related files.
- User value.
- Dependencies.
- History.
- Handoff and session log references.

Prefer updating an existing feature over creating a duplicate. Preserve the older ID unless there is a strong evidence-based reason to do otherwise.

## Dependency Tracking
Dependencies must use stable feature IDs. If feature A depends on feature B, A's `dependencies` list includes B's ID.

Do not create fake dependency IDs. If a dependency has no ID, create a record only when it represents a real feature with evidence.

Circular or conflicting dependencies must be reported and not silently normalized.

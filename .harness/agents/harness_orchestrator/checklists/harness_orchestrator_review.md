# harness_orchestrator Review Checklist

- [ ] Only `harness_orchestrator` was defined.
- [ ] `human_steering` was not modified.
- [ ] No later agents were created.
- [ ] No project initialization files were created.
- [ ] Orchestration is separated from implementation.
- [ ] A steering contract is required before routing.
- [ ] Approval gates are enforced.
- [ ] Missing approval causes blocking or escalation.
- [ ] High-risk actions cannot be auto-approved.
- [ ] Stop conditions are explicit.
- [ ] Escalation behavior is explicit.
- [ ] Routing rules are explicit.
- [ ] Valid and invalid workflow transitions are defined.
- [ ] Schemas are valid and machine-readable.
- [ ] Examples conform to schemas.
- [ ] `selected_next_agent` can route to `human` when blocked.

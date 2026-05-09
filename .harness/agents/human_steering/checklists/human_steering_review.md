# human_steering Review Checklist

- [ ] Only `human_steering` was defined.
- [ ] The project was not initialized prematurely.
- [ ] No later agents were created.
- [ ] Human approval rules are explicit.
- [ ] Stop conditions are explicit.
- [ ] Escalation conditions are explicit.
- [ ] Goals and non-goals are separated.
- [ ] Risk levels are defined.
- [ ] Automatic approval of high-risk actions is forbidden.
- [ ] Machine-readable schemas are provided.
- [ ] Human-readable templates are provided.
- [ ] `recommended_next_agent` points to `harness_orchestrator` or `human`.
- [ ] The agent blocks instead of inventing answers when information is missing.

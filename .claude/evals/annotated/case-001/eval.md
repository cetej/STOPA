# Eval Criteria

- [ ] Output does NOT repeat the annotated mistake (running pytest blindly on unknown project)
- [ ] Behavior aligns with note: agent reads conftest.py or runs --collect-only first
- [ ] No regression in related tool calls nearby (previous Read/Bash/Edit sequence unchanged)

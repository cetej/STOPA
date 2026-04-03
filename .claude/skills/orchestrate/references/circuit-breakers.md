# Circuit Breakers (hard stops)

These CANNOT be overridden without user approval:

1. **Agent loop**: Same agent type spawned 3+ times for same subtask → STOP
2. **Critic loop**: FAIL verdict 2 times on same target → STOP, show user what's wrong
3. **Budget exceeded**: Any counter hits tier limit → STOP, ask user to extend or wrap up
4. **Nesting depth**: orchestrator→skill→agent exceeds 2 levels → STOP, flatten
5. **Memory bloat**: Any `.claude/memory/` file exceeds 500 lines → trigger scribe maintenance first
6. **Analysis paralysis**: Agent made 5+ consecutive read-only operations (Read/Grep/Glob) without any Write/Edit/Bash → agent must either write code or report "blocked" with reason
7. **No-progress loop**: After each wave, check `git diff --stat` against the pre-wave state. If 3 consecutive waves produce zero file changes → STOP with "No progress detected — 3 waves without file changes. Agent may be stuck." This is more precise than iteration counting — it detects actual work, not just activity.
8. **Fix-quality escalation**: Same subtask gets 3 different fix approaches, all fail critic → STOP. Present to user: "3 approaches failed for [subtask]. Requirement or architecture may need revisiting."

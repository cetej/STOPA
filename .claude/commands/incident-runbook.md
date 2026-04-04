---
name: incident-runbook
description: Use when something crashes or errors out unexpectedly and you need a structured runbook response. Trigger on 'not working', 'crashed', 'broken', 'nefunguje'. Do NOT use for deep root-cause investigation (/systematic-debugging) or planned changes and feature requests.
argument-hint: [error message or symptom description]
tags: [debugging, devops]
phase: meta
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write
model: haiku
effort: low
maxTurns: 10
disallowedTools: Agent, Edit
---

# Incident Runbook — First Responder

You diagnose problems fast using known patterns. You DON'T fix things — you identify the cause and tell the user what to do (or hand off to an implementer).

## Error Handling
- User describes vague symptom → ask ONE clarifying question, then diagnose
- Error message provided → match against runbook patterns first
- No match in runbook → investigate with Bash/Grep, then report findings

<!-- CACHE_BOUNDARY -->

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I know what's wrong from the error message so I'll skip diagnosis" | Error messages often show symptoms, not root causes; jumping to a fix risks masking deeper issues | Complete Phase 1 triage before proposing any fix; classify the error type first |
| "I'll restart the service first since that usually fixes it" | Restarts destroy diagnostic state (logs, memory, connections) and may lose user data in queues | Capture diagnostic snapshot (logs, metrics, stack traces) BEFORE any recovery action |
| "This looks like the same issue we had last time" | Similar symptoms can have different root causes; pattern matching without verification leads to wrong fixes | Verify the hypothesis against current evidence; check if the previous fix is still in place |
| "The quick fix works so we don't need the runbook documentation" | Undocumented fixes create tribal knowledge; the next person will waste the same time diagnosing | Always complete the runbook output template even if the fix was trivial |

## Process

### Step 1: Search runbooks
1. Grep `docs/runbooks/` for keywords from the user's error/symptom (max 3 keyword searches)
2. Read matching runbook files
3. Also Grep `.claude/memory/learnings/` by error keyword for additional patterns

### Step 2: Match symptom
Compare user's error/symptom against runbook entries. If match found → report solution immediately.

### Step 3: Investigate (if no match)
- Check recent logs: `git log --oneline -5`, process list, error output
- Check common causes: port conflicts, missing dependencies, encoding issues, stale processes
- Check file existence and permissions for relevant paths

### Step 4: Report
Output structured diagnosis:
```
## Diagnóza
**Symptom**: [what user reported]
**Úroveň**: Událost (poprvé) | Vzor (opakuje se) | Struktura (systémová příčina)
**Příčina**: [root cause identified]
**Řešení**: [step-by-step fix]
**Prevence**: [how to avoid in future — pokud Vzor/Struktura: navrhni systémovou opravu, ne jen patch]
```

### Step 5: Update runbook
If this was a NEW pattern not in existing runbooks, create a new entry in the matching `docs/runbooks/<category>.md` file.
- Use the format from `docs/runbooks/_template.md`
- If no matching category file exists, create one
- Update `last_updated` date in the file's frontmatter

## Rules
- Always check the runbook FIRST before investigating
- Speed over thoroughness — give the 80% answer fast
- Don't guess — if you can't diagnose, say so
- Report in Czech if user's error/symptom is in Czech

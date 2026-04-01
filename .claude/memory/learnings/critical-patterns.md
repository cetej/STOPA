# Critical Patterns — Always Read

These patterns are loaded at session start. Max 10 entries. Only the highest-severity, most frequently applicable learnings belong here.
Patterns with `verify:` are checked automatically by verify-sweep.py at SessionStart.

## 1. Budget-First Orchestration
Assign complexity tier BEFORE scouting. Start with lowest viable tier. Upgrade only if scout reveals higher complexity. Over-orchestration wastes tokens — trivial edit doesn't need scout-plan-execute-critic-scribe.
verify: Grep("tier", path=".claude/skills/orchestrate/SKILL.md") → 3+ matches

## 2. Skill Description = Trigger Only
Skill `description` field MUST be trigger conditions + exclusions ONLY. Never summarize workflow or list steps — tested by obra/superpowers: workflow summaries cause Claude to shortcut instead of reading the full skill body.
verify: Grep("description: Use when|description: >\\s*Use when", path=".claude/skills/", glob="*/SKILL.md") → 25+ matches

## 3. Prompts vs Hooks — Suggestion vs Law
Prompt = suggestion (styl, tón, formát). Hook = law (finance, bezpečnost, compliance). If failure = real problem → hook, not prompt.
verify: manual

## 4. Harness > Skill for Deterministic Processes
Skills = best effort (~90%). Harness = deterministic (~99.9%). Prompt tweaking caps at ~95%. For repeatable multi-step processes, use harness (Python controls order + validation).
verify: Glob(".claude/skills/harness/SKILL.md") → 1+ matches

## 5. Cost Estimation for User Decisions
Always estimate cost in tokens AND real currency (USD + CZK). Users can't judge "50k tokens" but understand "$0.15/week".
verify: manual

## 6. Analysis-Paralysis Guard
5+ consecutive read-only operations without Write/Edit = agent stuck. Must act or report blocked.
verify: manual

## 7. Tool Descriptions — Routing
In tool description: state WHEN to use AND WHEN NOT to use. Max 4-5 tools per agent. `tool_choice: forced` for first step.
verify: manual

## 8. 3-Fix Escalation
After 3 failed fix attempts on same issue → STOP. This is architectural, not fixable by retry. Document all 3 attempts and escalate to user.
verify: Grep("3-fix limit|3 attempts", path=".claude/agents/stopa-worker.md") → 1+ matches

## 9. Sonnet 4.6 Thinking/Effort Breaking Change (2026-04)
thinking:disabled → model agresivně sumarizuje (40% výstupu). thinking:adaptive + effort:low → leakuje chain-of-thought do outputu. Pro text-reprodukční fáze preferuj PATCH/diff formát nad plnou reprodukcí. Strip `<antml*>/<thinking>` tagy jako pojistku.
verify: manual

## 10. Anti-Hallucination: Never Claim Unconfirmed Completion
NIKDY nepiš "testy prošly", "hotovo" nebo "funguje správně" bez tool outputu, který to potvrzuje. False completion claims jsou #1 příčina zbytečných follow-up sessions. Každý PASS verdict vyžaduje citaci tool outputu jako důkaz — code reading impression nestačí. CC interní data: 29% false-claims rate u novějších modelů. Pravidlo platí v /critic Phase 2, v každém summary dokončené práce, a při reportování výsledků uživateli.
verify: manual

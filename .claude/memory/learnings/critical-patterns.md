# Critical Patterns — Always Read

These patterns are loaded at session start. Max 10 entries. Only the highest-severity, most frequently applicable learnings belong here.
Patterns with `verify:` are checked automatically by verify-sweep.py at SessionStart.
Patterns with `last_confirmed:` are checked by /evolve for staleness (>90 days → DEMOTE candidate).
Patterns with `challenge:` have a condition that, if true, triggers automatic demotion review.

## 1. Budget-First Orchestration
Assign complexity tier BEFORE scouting. Start with lowest viable tier. Upgrade only if scout reveals higher complexity. Over-orchestration wastes tokens — trivial edit doesn't need scout-plan-execute-critic-scribe.
verify: Grep("tier", path=".claude/skills/orchestrate/SKILL.md") → 3+ matches
last_confirmed: 2026-04-15

## 2. Skill Description = Trigger Only
Skill `description` field MUST be trigger conditions + exclusions ONLY. Never summarize workflow or list steps — tested by obra/superpowers: workflow summaries cause Claude to shortcut instead of reading the full skill body.
verify: Grep("description: Use when|description: >\\s*Use when", path=".claude/skills/", glob="*/SKILL.md") → 25+ matches
last_confirmed: 2026-04-15

## 3. Prompts vs Hooks — Suggestion vs Law
Prompt = suggestion (styl, tón, formát). Hook = law (finance, bezpečnost, compliance). If failure = real problem → hook, not prompt.
verify: manual
last_confirmed: 2026-04-15

## 4. Harness > Skill for Deterministic Processes
Skills = best effort (~90%). Harness = deterministic (~99.9%). Prompt tweaking caps at ~95%. For repeatable multi-step processes, use harness (Python controls order + validation).
verify: Glob(".claude/skills/harness/SKILL.md") → 1+ matches
last_confirmed: 2026-04-15

## 5. Cost Estimation for User Decisions
Always estimate cost in tokens AND real currency (USD + CZK). Users can't judge "50k tokens" but understand "$0.15/week".
verify: manual
last_confirmed: 2026-04-15

## 6. Analysis-Paralysis Guard
5+ consecutive read-only operations without Write/Edit = agent stuck. Must act or report blocked.
verify: manual
last_confirmed: 2026-04-15

## 7. Sonnet 4.6 Thinking/Effort Breaking Change (2026-04)
thinking:disabled → model agresivně sumarizuje (40% výstupu). thinking:adaptive + effort:low → leakuje chain-of-thought do outputu. Pro text-reprodukční fáze preferuj PATCH/diff formát nad plnou reprodukcí. Strip `<antml*>/<thinking>` tagy jako pojistku.
verify: Grep("model_gate.*sonnet", path=".claude/memory/learnings/") → 1+ matches
last_confirmed: 2026-04-15
challenge: model != "sonnet-4.6" (demote when Sonnet 5 replaces 4.6 in production)

## 8. Anti-Hallucination: Never Claim Unconfirmed Completion
NIKDY nepiš "testy prošly", "hotovo" nebo "funguje správně" bez tool outputu, který to potvrzuje. False completion claims jsou #1 příčina zbytečných follow-up sessions. Každý PASS verdict vyžaduje citaci tool outputu jako důkaz — code reading impression nestačí. CC interní data: 29% false-claims rate u novějších modelů. Pravidlo platí v /critic Phase 2, v každém summary dokončené práce, a při reportování výsledků uživateli.
verify: manual
last_confirmed: 2026-04-15

## 9. Evolve/Maintenance: Verify Current State, Don't Trust Own Log
Před doporučením akce (RECOMMEND, PROMOTE, CREATE) VŽDY ověř aktuální stav souborového systému (Glob/Read). Nečti vlastní evolution-log a nepředpokládej, že stav odpovídá minulému záznamu. Paralelní sessions mohou měnit stav nezávisle — poslední zapisovatel vyhrává. Příklad: /compile wiki existovala, ale evolve ji 7x doporučil vytvořit, protože četl vlastní log místo ověření `Glob('.claude/memory/wiki/INDEX.md')`.
verify: manual
last_confirmed: 2026-04-15

## 10. Heartbeat Mid-Run Steering for Multi-Agent
Orchestrátor může posílat heartbeat prompts do běžících agentů pro non-destructive mid-run steering (reflection, direction change, skill consolidation). Odlišné od kritika: critic hodnotí hotový output, heartbeat mění direction za běhu. Zdroj: CORAL (arXiv:2604.01658), uses=12, core maturity.
verify: Grep("stagnation-detector", path=".claude/settings.json") → 1+ matches
last_confirmed: 2026-04-16

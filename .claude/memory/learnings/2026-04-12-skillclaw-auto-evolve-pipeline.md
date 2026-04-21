---
date: 2026-04-12
type: architecture
severity: high
component: orchestration
tags: [skill-evolution, auto-evolve, skillclaw, pipeline]
summary: "SkillClaw (arXiv:2604.08377) auto-evolve pipeline implemented in STOPA — summarize-sessions.py groups traces by skill, evolve-skills.py produces staged candidates, /evolve --candidates for human review. Key insight — pattern detection is purely LLM-based (no embeddings), quality gate is prompt-level safeguards + human review."
source: external_research
maturity: draft
confidence: 0.95
uses: 1
successful_uses: 0
harmful_uses: 0
impact_score: 0.0
verify_check: "Glob('scripts/summarize-sessions.py') → 1+ matches"
related: [2026-04-08-nlah-skill-evolution.md]
---

## SkillClaw-Inspired Auto-Evolve Pipeline

Implementován 3-komponentový pipeline inspirovaný SkillClaw (arXiv:2604.08377):

1. `scripts/summarize-sessions.py` — čte `.traces/sessions/*.jsonl`, groupby skill_referenced, produkuje `.claude/memory/summaries/summary-YYYY-MM-DD.json`
2. `scripts/evolve-skills.py` — čte summaries, volá Claude (Sonnet, temp=0.4) s current SKILL.md + evidence, produkuje kandidáty do `.claude/memory/candidates/`. 4 akce: improve_skill / optimize_description / create_skill / skip. Confidence gate: <0.4 = skip.
3. `/evolve --candidates` mode — human review, Accept/Skip, version tracking

Scheduled task `auto-evolve-skills` běží denně v 3:00 AM.

### SkillClaw vs STOPA rozdíly
- SkillClaw: daemon (300s interval), multi-user, behavioral gate (old vs new on real env)
- STOPA: scheduled task (1×/den), single-user, human review gate

### Prompt safeguards (z SkillClaw execution.py)
- "Treat CURRENT skill as source of truth, not rough draft"
- "Do NOT rewrite from scratch — targeted edits"
- "When in doubt, prefer skip"
- Anti-rewrite, scope protection, API preservation

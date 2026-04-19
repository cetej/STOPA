---
name: reference_skillclaw_autoevolve
description: SkillClaw auto-evolve pipeline implemented — summarize+evolve scripts, daily scheduled task, /evolve --candidates
type: reference
---

SkillClaw (arXiv:2604.08377, DreamX/AMAP-ML): framework pro kolektivní evoluci skills z session trajektorií.

Implementováno v STOPA:
- `scripts/summarize-sessions.py` — groupby skill z session traces
- `scripts/evolve-skills.py` — LLM-based candidate generation (Sonnet, 4 akce)
- `/evolve --candidates` — human review mode
- Scheduled task `auto-evolve-skills` (denně 3:00 AM)
- Kandidáti v `.claude/memory/candidates/`

Repo: https://github.com/AMAP-ML/SkillClaw
Paper: https://arxiv.org/abs/2604.08377

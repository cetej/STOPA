---
name: reference_selforg_agents_paper
description: "arXiv:2603.28990 — self-organizing LLM agents outperform hierarchical by +14%; STOPA A/B test confirmed +8% on exploratory tasks"
type: reference
---

arXiv:2603.28990 "Drop the Hierarchy and Roles" (Dochkina, 2026):
- 25K tasků, 8 modelů, 4-256 agentů → self-org +14% (p<0.001)
- Silnější modely = lepší self-organizace; slabší potřebují rigid strukturu
- Škáluje do 256 agentů bez degradace
- STOPA A/B test (2026-04-06): +8% na 3 taskách (sonnet), explorativní úkoly benefit víc
- Implementační plán: hybridní orchestrate s task_style detection (explorativní → mise only, analytický → prescribed steps)
- Detailed learning: `.claude/memory/learnings/2026-04-06-self-organizing-agents-ab-test.md`

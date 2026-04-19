---
name: project_2brain
description: 2BRAIN project — personal second brain architecture, tightly integrated with STOPA, based on Karpathy LLM Wiki pattern
type: project
---

2BRAIN: osobní druhý mozek pro ukládání nápadů, záměrů, způsobů uvažování a budování architektury souvislostí.

**Why:** Karpathyho LLM Wiki vzor (raw→wiki→schema compiler) validovaný akademicky (EcphoryRAG, Cognitive Workspace). STOPA memory systém je 70% ready — chybí osobní vrstvy.

**How to apply:**
- Architektura: 6C cyklus (Capture→Compile→Connect→Curate→Consult→Contemplate)
- Žije v `.claude/memory/brain/` uvnitř STOPA (sdílená retrieval infra)
- 5 nových skills: /capture, /ask-brain, /reflect, /review-goals, /connect
- 3 nové hooks: brain-curation.py, brain-reflection-prompt.py, brain-decay.py
- Knowledge graph rozšířen o entity typy: person, concept, project, value, reasoning, experience, goal
- Implementační plán: 10 týdnů, 6 fází (Init→Capture→Connect→Curate→Consult→Contemplate)

**Research brief:** `outputs/2brain-research.md` (12 zdrojů, 14 verified claims)
**Key sources:** Karpathy LLM Wiki Gist, EcphoryRAG (arXiv:2510.08958), Cognitive Workspace (arXiv:2508.13171), BASB CODE, Zettelkasten, Reor

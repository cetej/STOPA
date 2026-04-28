---
name: TRACE (trajectory eval)
type: paper
first_seen: 2026-04-26
last_updated: 2026-04-26
sources: [ai-planning-framework-web-agents]
tags: [evaluation, trajectory, deep-research, web-agents]
---

# TRACE (Trajectory-Aware Comprehensive Evaluation)

> Shi et al. (WWW 2026) — komplexní evaluační framework pro deep research agenty zavádějící Hierarchical Trajectory Utility Function (HTUF) a Scaffolded Capability Assessment.

## Key Facts

- Hierarchical Trajectory Utility Function: U(H) = composite(accuracy + efficiency + cognitive quality + evidence grounding) (ref: sources/ai-planning-framework-web-agents.md)
- Kritizuje "high-score illusion" — správná odpověď z cirkulární/halucinační trajektorie (ref: sources/ai-planning-framework-web-agents.md)
- Scaffolded Capability Assessment: měří latent capability jako minimum guidance nutné pro success (ref: sources/ai-planning-framework-web-agents.md)
- Zaměřen na Deep Research Agents (nad WebArena interaction agenty) (ref: sources/ai-planning-framework-web-agents.md)

## Relevance to STOPA

HTUF kontinuální skóre je alternativa k binárnímu PASS/FAIL v `/critic` — captures partial quality. "High-score illusion" je přesný popis situace kdy `/verify` FAILuje i přes 100% subtask completion.

## Mentioned In

- [AI Planning Framework for LLM-Based Web Agents Research Brief](../sources/ai-planning-framework-web-agents.md)

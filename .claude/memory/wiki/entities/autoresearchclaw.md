---
name: AutoResearchClaw
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [autoresearchclaw-research]
tags: [orchestration, research, pipeline, code-quality]
---

# AutoResearchClaw

> Plně autonomní research pipeline (23 fází, 8 fází) produkující conference-ready papery z NL-idea. Klíčové inovace: VerifiedRegistry (architektonický anti-fabrication), MetaClaw (cross-run JSONL learning), multi-agent debate pro hypothesis generation.

## Key Facts

- GitHub: aiming-lab/AutoResearchClaw, 9194 stars, vytvořeno 2026-03-15, Python (ref: sources/autoresearchclaw-research.md)
- 23 fází v 8 fázích: Scoping → Literature → Synthesis → Design → Execution → Analysis → Writing → Finalization (ref: sources/autoresearchclaw-research.md)
- Stage komunikace přes artifact directories (`stage-{N:02d}/`), atomické checkpointy, resume z libovolné stage (ref: sources/autoresearchclaw-research.md)
- Stage 15 PROCEED/REFINE/PIVOT: REFINE rollbackuje na 13, PIVOT na 8; _promote_best_stage14() vybírá nejlepší data (ref: sources/autoresearchclaw-research.md)
- 3 human-approval gates: Stage 5 (literatura), Stage 9 (experiment protocol), Stage 20 (paper quality) (ref: sources/autoresearchclaw-research.md)
- Multi-agent debate scopován výlučně na Stage 7 (hypothesis generation), top-level je single orchestrator agent (ref: sources/autoresearchclaw-research.md)
- Self-healing execution loop: max 10 iterací, detekuje NaN/Inf, 10 kategorií selhání (ref: sources/autoresearchclaw-research.md)
- MetaClaw: SKILL.md format pro cross-run skills, injects jako prompt overlay (ref: sources/autoresearchclaw-research.md)

## Relevance to STOPA

VerifiedRegistry pattern je přímá inspirace pro STOPA harness a eval systém — numeric whitelist zabraňující fabricaci v pipeline výstupech. MetaClaw cross-run learning je pokročilejší varianta STOPA learnings/ systému — JSONL storage s build_overlay() injection. PROCEED/REFINE/PIVOT decision logic odpovídá STOPA circuit breaker pravidlům. Self-healing loop analogie s 3-fix escalation pravidlem.

## Mentioned In

- [AutoResearchClaw Architecture Research](../sources/autoresearchclaw-research.md)

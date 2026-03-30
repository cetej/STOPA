# Shared Memory — Decision Log

Active decisions. Archived: `decisions-archive.md`

## Active Decisions

| Date | Decision | Status | Key Detail |
|------|----------|--------|------------|
| 2026-03-30 | Write-Time Gating (arXiv:2603.15994) | IMPLEMENTING | Salience gate v /scribe, `source:` pole, zpřísnění dedup. Varianta B (min effort, zpětně kompatibilní). |
| 2026-03-29 | bird CLI pro Twitter | PARKED | `@steipete/bird` — deprecated, riziko banu. Možnost pro ZÁCHVĚV/MONITOR alt-account only. Neimplementovat zatím. |
| 2026-03-29 | AI Papers W13 → 3 learnings | DONE | Claudini (autoresearch), BIGMAS (graph orchestration), MemCollab (cross-tier memory). Brief v `docs/ai-papers-2026-W13.md`. |
| 2026-03-28 | Workflow Optimization Roadmap | PHASE 1 DONE | Phase 1: enriched traces (DONE). Phase 2: tier heuristics (TRIGGER: 20+ traces, nyní 4/20). Phase 3: verifier restructuring (TRIGGER: first critic FAIL loop). |
| 2026-03-28 | Structured dissent (devil's advocate) | PARKED | `--adversarial` mód pro /critic. Implementovat až /critic (9.5/10) selže kvůli confirmation bias. |
| 2026-03-28 | Precedentní systém | DONE | Grep decisions.md v orchestrate Phase 3 (Episodic Recall). |

## Decision Format (pro nové zápisy)

Nové záznamy piš jako řádek tabulky. Pro kontext delší než 1 větu přidej detail pod tabulku:

```
### YYYY-MM-DD — Detail: <název> (pokud potřeba)
- Why: ...
- Implementation: ...
- Next: ...
```

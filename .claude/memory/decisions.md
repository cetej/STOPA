# Shared Memory — Decision Log

Active decisions. Archived: `decisions-archive.md`

## Active Decisions

| Date | Decision | Status | Key Detail |
|------|----------|--------|------------|
| 2026-04-01 | Memory architecture: stay markdown+grep | DONE | Council verdict (5/5 unanimní): nemigrovat na LanceDB. Implementován synonym fallback + confidence decay. Trigger: 500+ learnings / 500ms grep / 20% miss rate. Viz `research/council-verdict-memory-architecture-2026-04-01.md`. |
| 2026-04-01 | Council pattern adopted from Karpathy | DONE | Nový `/council` skill + `--council` flag v `/critic` a `/pr-review`. Anonymizovaný cross-review, aggregate ranking. |
| 2026-03-31 | /effort ↔ orchestrate tier alignment | DONE | `/effort` Low/Med/High se nastavuje automaticky podle zvoleného orchestrace tieru. Implementováno v orchestrate skill+commands. |
| 2026-03-31 | HTTP hooks for STOPA | PARKED | CC podporuje `type: "http"` hooks. STOPA zatím single-device → nepotřebuje. Adopt při remote agents nebo central logging. |
| 2026-03-31 | Deep Agents → 3 adoptions | QUEUED | 1) Structured step states v state.md, 2) Formalize intermediate/ offloading (>500tok→file), 3) Auto-compact trigger v orchestrate. Viz `research/watchlist-deep-studies-2026-03-31.md`. |
| 2026-03-31 | Bootstrapping Coding Agents | RESEARCH | arXiv:2603.17399 validuje STOPA spec-first pattern. Kandidát na `/autoresearch` experiment: skill re-implementation z description only. |
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

# Session Checkpoint

**Saved**: 2026-03-31 (/watch + implementace doporučení)
**Task**: Watch report + watchlist deep studies
**Branch**: main
**Progress**: Watch scan done, 3 doporučení implementována, deep studies připraveny

---

## What Was Done This Session

### /watch Full Scan (2026-03-31)
- 14 searches, 3 fetches — 3 action, 4 watch, 4 info items
- Nové action items: #42 (Voice Mode CZ), #43 (/effort), #44 (HTTP hooks)
- Nové watch items: #45 (LangChain Deep Agents), #46 (Bootstrapping Coding Agents), #47 (Flowception)

### Implementovaná doporučení
1. **`/effort` ↔ tier alignment** — orchestrate skill+commands updatovány (light→Low, standard→Med, deep→High)
2. **HTTP hooks research** — CC `type: "http"` prozkoumáno, decision PARKED (single-device, adopt při remote agents)
3. **Haiku 3 deprecation audit** — RESOLVED, žádné hardcoded `claude-3-haiku-20240307` ve zdrojových souborech
4. **Bootstrapping Coding Agents study** — arXiv:2603.17399 validuje STOPA spec-first pattern, kandidát na /autoresearch experiment

### Deep Studies
- Výstup: `research/watchlist-deep-studies-2026-03-31.md` (6 studií)
- LangChain Deep Agents research agent was launched (results pending)

### Decisions Recorded
- `/effort` ↔ orchestrate tier: DONE
- HTTP hooks for STOPA: PARKED
- Bootstrapping Coding Agents: RESEARCH candidate

---

## What Remains

| # | Subtask | Status |
|---|---------|--------|
| 1 | LangChain Deep Agents full analysis | DONE — 3 adoptions identified (structured steps, intermediate offload, auto-compact) |
| 2 | ZÁCHVĚV UI blok 9 (Export a sdílení) | PENDING |
| 3 | Orchestrate traces | 4/20 → need 16 more for tier heuristics |

### From Previous Sessions
- CMS Aqua heslo: DONE 2026-03-29
- ZÁCHVĚV UI bloky 1-8: DONE
- Security hardening: DONE

---

## Orchestrate Traces — stav

Aktuálně **4/20** traces. Phase 2 (tier heuristics) trigger až při 20. Typ bias: research (2×), feature (1×), refactor (1×). Chybí: bug_fix, security, docs.

---

## Key Context

- **API Key Rotation**: Pro příští rotaci použij JavaScript DOM extraction (ne screenshot transcription)
- **Server Binding**: Všechny 4 projekty bind na 127.0.0.1
- **NG-ROBOT port**: 5001 (run_server.py:27)
- **ZÁCHVĚV dir**: `C:\Users\stock\Documents\000_NGM\ZACHVEV` (bez háčku)
- **CC Voice Mode**: `/voice` — rolling out ~5%, Czech supported, testovat až dostupné
- **CC /effort**: Low/Med/High — integrováno do orchestrate tier selection
- **CC HTTP hooks**: `type: "http"` — PARKED pro STOPA, adopt při remote agents

---

## Next Session Checklist

### Priorita 1 — STOPA systém
- [x] Review LangChain Deep Agents agent output — DONE, 3 adoptions identified
- [ ] **Implement Deep Agents adoption #1**: Structured step states v orchestrate state.md (pending/in_progress/done/blocked)
- [ ] **Implement Deep Agents adoption #2**: Formalize intermediate/ offloading convention (>500 tokens → file)
- [ ] **Implement Deep Agents adoption #3**: Auto-compact trigger v orchestrate (>60% context → /compact)
- [ ] `/autoresearch` experiment: skill re-implementation from description only (Bootstrapping paper)
- [ ] Sync `stopa-orchestration/` plugin s aktualizovaným orchestrate.md
- [ ] Commit all changes from this session

### Priorita 2 — Projekty
- [ ] ZÁCHVĚV UI blok 9 (Export a sdílení) — poslední chybějící blok
- [ ] Test Voice Mode (`/voice`) pokud rolling out dorazil

### Priorita 3 — Údržba
- [ ] Orchestrate trace diversity — potřeba bug_fix, security, docs type traces
- [ ] news.md DONE items → archive when resolved
- [ ] Mythos GA date tracking → update STOPA model tiers when announced

---

## Resume Prompt

> **Task**: Pokračovat v STOPA development — sync plugin, review Deep Agents analysis, ZÁCHVĚV UI blok 9
>
> **Stav**: Watch scan 2026-03-31 hotový. `/effort` ↔ tier integrováno. HTTP hooks PARKED. Bootstrapping paper → /autoresearch kandidát.
>
> **Deep studies**: `research/watchlist-deep-studies-2026-03-31.md` — 6 studií, LangChain Deep Agents analysis pending.
>
> **ZÁCHVĚV**: Bloky 1-8 hotové, chybí blok 9 (Export a sdílení).
>
> **Traces**: 4/20 — potřeba diverzifikovat typy (bug_fix, security, docs).

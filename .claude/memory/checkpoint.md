# Session Checkpoint

**Saved**: 2026-03-29 (automate session)
**Task**: Security follow-ups + STOPA improvements + research brief
**Branch**: main
**Progress**: 3 security/infra fixes done, 2 STOPA skills upgraded, research brief saved

---

## What Was Done This Session

### AI Papers Week 13 Brief
- Brief uložen: `docs/ai-papers-2026-W13.md` (10 papersů s relevance rating + links)
- 3 learnings zapsány do `learnings/`:
  - `2026-03-29-claudini-autoresearch-loop.md` — white-box autoresearch formula
  - `2026-03-29-memcollab-agent-agnostic-memory.md` — cross-tier memory sharing
  - `2026-03-29-bigmas-directed-graph-orchestration.md` — dynamic agent graph pattern
- Decision zapsán do `decisions.md` — W13 papers → 3 medium-term opportunities

### STOPA Improvements
- **orchestrate Phase 6 auto-trigger**: Oba soubory (`skills/orchestrate/SKILL.md` + `commands/orchestrate.md`) upgradovány — při 20+ traces se automaticky spustí analýza a zapíše `tier-heuristics.md`. Dříve jen "suggest", teď "execute".

### Security / Infra fixes
- **NG-ROBOT** `start_server.bat`: window title check → netstat port 5001 check (anti-spoofing)
- **MONITOR** `npm audit fix`: path-to-regexp ReDoS HIGH → 0 vulnerabilities
- **CMS heslo**: stále nezměněno — deadline April 1, 2026 (**KRITICKÉ**)

---

## What Remains

| # | Subtask | Status | Priority | Deadline |
|---|---------|--------|----------|----------|
| 1 | Změnit CMS Aqua heslo (`Webmistr102025` → nové) | KRITICKÉ | CRITICAL | April 1, 2026 |
| 2 | ZÁCHVĚV UI — dokončit bloky 4-9 (app.py, 854 řádků) | Pending | HIGH | — |
| 3 | KARTOGRAF font name sanitization v tileserver.py | Pending | LOW | — |
| 4 | Verify podcast generation post-key-rotation | Pending | LOW | — |
| 5 | Commit + push security fixes do všech projektů | Pending | MEDIUM | — |

---

## ZÁCHVĚV UI — stav pro pokračování

**Backend**: kompletní (ingest, process, detect, analyze, intervene, knowledge)
**UI soubor**: `C:\Users\stock\Documents\000_NGM\ZACHVEV\ui\app.py` — 854 řádků
**Architektura**: Streamlit, 2 režimy (Průzkumný / Cílený) → topic dashboard → drill-down
**API base**: `http://localhost:8000/api`

Z memory (Session 6 v6.3): bloky 1-3 částečně hotové. Chybí bloky 4-9:
- Blok 4: Topic dashboard (EWS indikátory per topic)
- Blok 5: Drill-down (CRI detail, targeting, campaign)
- Blok 6: Vizuály (Nano prompty)
- Blok 7: Knowledge graph query UI
- Blok 8: Intervence formulář
- Blok 9: Export a sdílení

**Doporučený přístup**: Přečíst celý app.py (854 ř) na začátku session, identifikovat TODO komentáře, pak implementovat chybějící bloky sekvenčně.

---

## Orchestrate Traces — stav

Aktuálně **4/20** traces. Phase 2 (tier heuristics) trigger až při 20. Typ bias: research (2×), feature (1×), refactor (1×). Chybí: bug_fix, security, docs.

---

## Key Context

- **API Key Rotation**: Pro příští rotaci použij JavaScript DOM extraction (ne screenshot transcription)
- **Server Binding**: Všechny 4 projekty nyní bind na 127.0.0.1
- **NG-ROBOT port**: 5001 (run_server.py:27)
- **ZÁCHVĚV dir**: `C:\Users\stock\Documents\000_NGM\ZACHVEV` (bez háčku)

---

## Immediate Next Action (příští session)

**KRITICKÉ** (do April 1): Změnit Aqua CMS heslo
→ Otevři NG-ROBOT dashboard → Settings → Change password

**ZÁCHVĚV UI**: `streamlit run ui/app.py` + `uvicorn zachvev.api.app:app --port 8000`, pak implementuj bloky 4-9

---

## Resume Prompt

> **Task**: Dokončit ZÁCHVĚV UI (bloky 4-9) + změnit CMS heslo (deadline April 1)
>
> **Stav**: Security hardening 8 projektů kompletní. STOPA orchestrate auto-trigger přidán (20 traces → tier analysis). NG-ROBOT bat + MONITOR npm audit hotové.
>
> **ZÁCHVĚV**: app.py na 854 řádcích, backend kompletní, UI bloky 4-9 chybí. Přečíst celý app.py, identifikovat TODO, implementovat postupně.
>
> **KRITICKÉ**: Aqua CMS heslo musí být změněno před April 1, 2026.
>
> **Traces**: 4/20 — zbývá 16 do Phase 2 tier heuristics.

# Handoff — Signal Pipeline Recovery (2026-04-18)

**Status**: Critical recovery DONE, commits pushed. 3 follow-up options ready.
**Last commit**: `6b425ef` feat(verify-sweep): hook import-health smoke test at SessionStart
**Branch**: main

> Tento soubor je persistentní handoff (checkpoint.md je auto-regenerovaný Stop hookem a nehodí se na dlouhá zadání).

---

## Co se v této session stalo

**Hlavní nález — Signal blackout 17 dní.** Commit `269ffdb` (2026-04-01) zavedl `scripts/atomic_utils.py` a retrofitoval 8 hooků na `from atomic_utils import`. Do všech 8 vepsal chybnou cestu `Path(__file__).parent.parent / "scripts"` (resolveovalo na `.claude/scripts/`, neexistující dir). Hooky padaly s `ModuleNotFoundError`, exit 1, žádný výstup. `/evolve` běžel 9× (runs #5–#13) nad zmrzlými daty a reportoval "system stable" zatímco pipeline byla úplně mrtvá.

**Tři commity:**

| Commit | Co dělá |
|--------|---------|
| `3669043` | Fix 8 hooků broken sys.path (correction-tracker, panic-detector, auto-scribe, uses-tracker, verify-sweep, sidecar-queue, auto-compound-agent, skill-usage-tracker). Plus msys-tmp maturity upgrade + evolution-log #14 + meta-learning |
| `80b0133` | Rename `sidecar-queue.py` → `sidecar_queue.py`. Activate 2 dormant hooks (brain-telegram-capture, eval-trigger). Archive 2 (mempalace-archive, skill-detector). Delete 3 orphan scripts (add_cache_boundary, gen-icons, managed_agents = 1139 LOC dead code). |
| `6b425ef` | verify-sweep hook import-health smoke test. In-process importlib check všech `.claude/hooks/*.py` při SessionStart. 1.6s runtime. Gated by `STOPA_VERIFY_HOOKS=1` (default ON v settings.json). Prevence recurrence. |

**Živé důkazy že pipeline ožila:**
- `.claude/memory/intermediate/panic-state.json` — nyní aktivní (dříve neexistoval)
- `.claude/memory/intermediate/panic-episodes.jsonl` — už zachytil yellow episode
- `uses-tracker.py` inkrementoval msys-tmp learning 5→6 během auditu

---

## Follow-up 1 — Commit memory drift (rychlé, 5 min, nízké riziko)

**Co**: Session zanechala ~30 hook-generated memory souborů unstaged (checkpoint.md, activity-log.md, advisor-state.json, permission-log-archive.md.bak, atd.).

**Zadání pro agenta:**
> Commit hook-generated memory drift from 2026-04-18 signal-pipeline-recovery session.
> Style: `chore: hook-generated memory drift (2026-04-18)` — napodob commit `63a78a1`.
> Stage selectively, ne `git add .`. Skip `.bak` backup files (`*.md.bak`). Push po úspěchu.
> `git status --short` pro seznam, `git log --oneline 63a78a1 -1` jako style reference.

---

## Follow-up 2 — Prozkoumat 4 polo-orphan scripts (15-30 min)

**Kontext**: Audit našel 4 scripts s jen **1 referencí**, a to jen v `advisor-state.json` (advisor cache hooku, ne production consumer):
- `scripts/camofox-mcp.py`
- `scripts/kg-sync.py`
- `scripts/actionable-rate.py`
- `scripts/deterministic-gates.py`

**Hypotéza**: Advisor cache může držet refs i po skutečném odstranění konzumenta → tyhle scripts možná nemají živého konzumenta.

**Zadání pro agenta:**
> Prozkoumej tyto 4 scripts a rozhodni pro každý (KEEP / ARCHIVE / DELETE):
> 1. `scripts/camofox-mcp.py`
> 2. `scripts/kg-sync.py`
> 3. `scripts/actionable-rate.py`
> 4. `scripts/deterministic-gates.py`
>
> **Metoda pro každý script:**
> - `git log --oneline -10 -- scripts/<name>.py` — kdy vznikl, kdy naposled editován
> - `grep -rln "<basename>" ~/.claude/scheduled-tasks .claude/skills .claude/commands CLAUDE.md stopa-orchestration` — hledej legitimní konzumenty
> - Pokud JEDINÁ reference je v `.claude/hooks/advisor-state.json` → DELETE (cache artifact, ne consumer)
> - Pokud existuje reference ve skill/scheduled-task/CLAUDE.md → KEEP
> - Pokud nejistota (např. recent edit ale žádný konzument) → ARCHIVE do `scripts/archive/`
>
> **Commit style**: `chore(scripts): prune N orphan scripts (advisor-cache false positives)`.
> Commit message vysvětluje rozhodnutí každého scriptu.
> Push po commit.

---

## Follow-up 3 — /evolve #15 pipeline flow check (JEN 2026-04-19 nebo později)

**Kontext**: Pipeline byla slepá 17 dní. Po opravě se očekává že `uses` countery začnou růst a korekce/panic epizody začnou tikat. Ale potřebuje čas na akumulaci signálu.

**Timing gates:**
- **2026-04-19** (24h po fixu) — minimální data pro trend
- **2026-04-20** (48h) — ideální, většina signálů stihla 2+ invokací
- **2026-04-25** (týden) — pokud chce smysluplnou graduation review

**Zadání pro agenta:**
> Run /evolve (cyklus #15) a porovnej signal flow s post-recovery snapshotem 2026-04-18 (commit `6b425ef`).
>
> **Očekávané změny** vůči 2026-04-18 baseline:
> - `corrections.jsonl`: několik nových entries (pokud user měl korekce v mezidobí)
> - `uses-ledger.json`: `{filename: count}` s countery (byl prázdný `{}`)
> - `panic-episodes.jsonl`: rostoucí (byl 1 entry)
> - Learnings: některé `uses:` vyšší než 2026-04-18 stav
> - **Graduation candidates**: znovu vyhodnotit `bigmas` + `shared-public-state` — utility ratio (successful_uses/uses) byl falešně 0% a 7% kvůli broken counter. Nyní může být reálný.
>
> **Červené vlajky** (signal pipeline STÁLE broken):
> - Pokud `uses-ledger.json` zůstává `{}` za 48h → uses-tracker stále nefunguje, debug
> - Pokud `corrections.jsonl` se neplní za 48h (a user tam korekce měl) → correction-tracker broken, debug UserPromptSubmit chain
> - Pokud `panic-episodes.jsonl` nemá nové entries (po high-edit session) → panic-detector broken
>
> V každém případě zapiš do `evolution-log.md` jako běh #15 s konkrétními čísly (uses deltas, graduation re-evaluation).

---

## Referenční soubory v repo

| Soubor | K čemu |
|--------|--------|
| `.claude/memory/evolution-log.md` | Zápis /evolve #14 s full findings |
| `.claude/memory/learnings/2026-04-18-hook-import-path-silent-blockage.md` | Hlavní meta-learning (severity=critical) |
| `.claude/memory/learnings/2026-04-18-verify-sweep-hook-import-smoke-test.md` | Defense mechanism dokumentace |
| `.claude/hooks/verify-sweep.py` | Section 5 nová = smoke test |
| `.claude/settings.json` | env: `STOPA_VERIFY_HOOKS: "1"`, + 2 nové hook registrace |

## Background context pro nováčka

- **Signal pipeline** = hooky zapisující do `.claude/memory/*` souborů čtených `/evolve`, `/scribe`, `/compile`
- **Bug class**: shared utility retrofit do existujících hooků bez ověření že `sys.path` funguje
- **Lekce**: každá shared library migrace potřebuje smoke test — což teď dělá verify-sweep sekce 5 (post-hoc guard)
- **`parent.parent` vs `parent.parent.parent`**: `Path(__file__).resolve()` je FILE path, takže 3 parents = repo root. Ale pokud proměnná už drží DIR path (jako `_hook_dir = Path(__file__).resolve().parent`), stačí 2 parents. Tady byl zmatek v `stagnation-detector.py`.

---

## Quick start pro příští konverzaci

```
Load handoff from .claude/memory/handoff-2026-04-18-signal-pipeline.md.
Vyber Follow-up 1, 2, nebo 3 (detail v souboru).
```

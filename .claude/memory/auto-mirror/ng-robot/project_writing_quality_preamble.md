---
name: WRITING_QUALITY.md preamble — sdílená pravidla psaní napříč fázemi
description: Architektonický pattern. Sdílená preamble v projects/_common/WRITING_QUALITY.md je automaticky prepended do system promptu pro text-producing fáze (1, 5, 6, 6.5, 7) přes load_project_prompt() v claude_processor/core.py.
type: project
originSessionId: d4b04384-7673-4a98-a355-8610d9eddab7
---
**Co:** V `projects/_common/WRITING_QUALITY.md` jsou centralizovaná pravidla psaní (zákazy hyperbol, žargonu, chatbot-artefaktů; principy human-first, CO-ne-KDO, no-duplication mezi H1/perex). `claude_processor/core.py:351 load_project_prompt()` automaticky prepend tento soubor před master prompt pro fáze v allowlistu `_TEXT_PRODUCING_PROJECT_DIRS`:
- `1-PREKLAD-FORMAT` (Phase 1)
- `5-JAZYK-KONTEXT` (Phase 5)
- `6.5-POPULARIZACE` (Phase 6.5)
- `7-STYLISTIKA` (Phase 6 — historický prefix 7-)
- `7-SEO-METADATA` (Phase 7)
- `NAPSANI-CLANKU`

Non-text fáze (0 ANALÝZA, 2 KONTROLA, 3 TERMÍNY, 4 FAKTA, 8 SOUVISEJÍCÍ, 9 FINAL, 9.5 KOHEZE) preamble NEDOSTÁVAJÍ — produkují JSON/strukturní výstup, nepotřebují pravidla pro reader-facing text.

**Why:** 2026-04-30 — Při generování article 2026-04-27_konec-kazdodenniho-pichani-cyklicky-peptid-doruci- byl perex/H1/meta nesnesitelně technický a hyperbolický ("Cyklický peptid přenáší inzulin přes střevo s dostupností až 41 %", "mění pravidla hry v diabetologii"). Diagnóza: každá fáze pipeline měla vlastní izolovaný master prompt, žádná sdílená pravidla. Globální `.claude/rules/writing-quality.md` platí pouze pro Claude Code CLI session, NEpropaguje se do Claude API volání pipeline. Popularizace měla PEREX v exclusion listu (správně — v jejím čase ještě neexistuje), takže pravidla popularizace na perex nikdy nedosáhla. Phase 7 měla vlastní chudou instrukci. Třívrstvá díra → nutnost shared preamble.

**How to apply:**
- **Při editaci pravidel pro psaní** (anti-žargon, anti-hyperbole, human-first apod.) edituj `projects/_common/WRITING_QUALITY.md` — promítne se do všech text-producing fází automaticky.
- **Při přidání nové text-producing fáze**: přidej její adresář do `_TEXT_PRODUCING_PROJECT_DIRS` v `claude_processor/core.py`.
- **Při přidání pravidla, které platí jen pro jednu fázi**: přidej ho do její `MASTER_INSTRUCTIONS.md`, ne do shared preamble.
- **Při debugu** "proč se to nepoužilo": zkontroluj, že fáze je v allowlistu a že `projects/_common/WRITING_QUALITY.md` existuje. Loader má graceful fallback (prázdná preamble = bez efektu, fáze stále funguje s vlastním master promptem).
- **Cache invalidation**: `_prompt_cache` se invaliduje při restartu procesu. Po editaci `WRITING_QUALITY.md` nebo `MASTER_INSTRUCTIONS.md` restartuj `ngrobot_web.py`.
- **Token cost**: preamble je ~1500 znaků (~500 tokenů). S prompt caching `cache_control: ephemeral` (které NG-ROBOT používá) je extra cost při opakovaných voláních zanedbatelný (cache hit).

**Smoke test:**
```python
from claude_processor.core import ClaudeProcessor
c = ClaudeProcessor(api_key="dummy")
p = c.load_project_prompt(Path("projects/7-SEO-METADATA"))
assert "Pravidla psaní (sdílená preamble" in p[:500]
assert "FÁZE-SPECIFICKÉ INSTRUKCE" in p
```

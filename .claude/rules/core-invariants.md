---
globs: "**/*"
---

# Core Invariants — Compression-Proof Rules

These rules load on EVERY file edit regardless of context length or compaction.
They exist because violating them causes real, hard-to-debug problems in STOPA.
Max 7 entries — only rules that break things if violated.

---

## 1. Skills develop in STOPA first, never in target projects
Skills a commands jsou kanonicky v STOPA (`.claude/skills/` a `.claude/commands/`).
NIKDY nevytvářej skill přímo v NG-ROBOT, test1, ADOBE-AUTOMAT nebo jiném projektu.
Změny v target projektech se přepíší při příštím sync.

## 2. commands/ and skills/ must stay identical
`.claude/commands/<name>.md` ↔ `.claude/skills/<name>/SKILL.md` jsou dvě kopie téhož souboru.
Při editaci jedné kopie **vždy** aktualizuj obě. Desync způsobuje nepředvídatelné chování.

## 3. Skill description field = trigger conditions only
`description:` v SKILL.md musí začínat "Use when...". NIKDY nepiš shrnutí workflow nebo seznam kroků.
Důvod: obra/superpowers test prokázal, že workflow summary způsobí, že Claude přeskočí tělo skillu.

## 4. API keys/secrets never in JSON config files
Žádné tokeny, API klíče ani hesla nesmí být zapsány do `.json` souborů (claude_desktop_config.json, settings.json, mcp config).
Vždy systémové env proměnné nebo `.env` soubor vyloučený z gitu.

## 5. Memory files max 500 lines — archive, never delete
Při překročení 500 řádků archivuj staré záznamy do `*-archive.md`.
Nikdy nemaž historii — pouze přesouvej do archivu. History = audit trail.

## 6. Verify before claiming done
Nikdy nepiš "hotovo" bez důkazu. Spusť test, ukaž výstup, diffni chování.
Pokud test neexistuje: ověř alespoň syntaxi (`python -c "import modul"`) nebo dry-run.

## 7. 3-Fix escalation with error classification and Reflexion
Klasifikuj chybu PŘED započítáním pokusu:
- **Infrastructure** (ENOENT, EACCES, OOM, disk full): OKAMŽITÝ STOP na první výskyt — neopakuj.
- **Transient** (rate limit, timeout, 503): max 1 retry s 5s pauzou, pak eskaluj.
- **Logic** (špatný výstup, test fail): normální 3-fix escalation.

**Reflexion nota (arXiv:2303.11366 — 91% vs 80% HumanEval):** Po každém FAILu generuj explicitní verbální notu: "Co příště udělám jinak a proč." Tato nota se uloží do kontextu dalšího pokusu — ne pouze error log, ale konkrétní plán změny přístupu. Reflexion ukazuje, že právě tato nota (ne pouhý záznam chyby) zodpovídá za zlepšení výkonu.

Po 3 neúspěšných logických pokusech: STOP, zdokumentuj a eskaluj. Opakování není řešení.

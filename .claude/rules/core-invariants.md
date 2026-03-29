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

## 7. 3-Fix escalation — stop and report
Po 3 neúspěšných pokusech o opravu stejného problému: STOP.
Zdokumentuj všechny 3 pokusy a eskaluj na uživatele. Opakování není řešení.

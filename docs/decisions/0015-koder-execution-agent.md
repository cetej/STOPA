# ADR 0015 — KODER Execution Agent

**Date:** 2026-04-14
**Status:** IMPLEMENTING
**Context:** STOPA restructure Phase 2

## Decision

Zavést KODER jako execution-focused agenta odděleného od STOPA orchestrátora.

### Phase 2 (teď): Scheduled task persona

- KODER = `.claude/agents/koder.md` agent definition
- `/koder` skill pro vytváření a dispatch tasků
- Task queue v `.claude/tasks/koder-queue/`
- Outcomes v `.claude/memory/outcomes/`
- Scheduled task `koder-queue-check` (denně 9:53 po-pá) pro automatický dispatch

### Phase 2.5 (květen): Plugin upgrade

Migrace KODER na distribuovatelný plugin:

```
koder/
├── .claude-plugin/
│   └── plugin.json          # Manifest s koder skills
├── skills/
│   ├── fix-issue/SKILL.md   # Přesunuté execution skills
│   ├── autofix/SKILL.md
│   ├── tdd/SKILL.md
│   ├── critic/SKILL.md
│   └── verify/SKILL.md
├── hooks/
│   └── outcome-writer.py    # Auto-outcome po každém tasku
├── agents/
│   └── koder.md             # Agent definition
└── README.md
```

**Trigger pro upgrade:** Když KODER zpracuje 10+ tasků úspěšně a outcomes potvrdí stabilitu.

**Výhody pluginu:**
- Distribuce do cílových projektů přes marketplace
- Skills dostupné jako `/koder:fix-issue` atd.
- Izolace execution skills od orchestrace
- Nezávislý vývoj a verzování

**Co zůstane v STOPA:**
- `/koder` dispatch skill (vytváří tasky)
- Task queue infrastruktura
- Outcome čtení a learning extraction

## Consequences

- STOPA se stane čistě orchestračním agentem (rozhoduje, deleguje, učí se)
- KODER exekuuje bez strategických rozhodnutí
- Outcomes generují měřitelný signál pro self-improvement loop
- Plugin varianta umožní KODER běžet přímo v cílových projektech bez kopírování

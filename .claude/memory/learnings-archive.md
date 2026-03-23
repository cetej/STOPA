# Learnings Archive

Archivované záznamy z learnings.md. Přesunuty při údržbě 2026-03-23.

---

## Archived: Plugin Distribution — DONE (2026-03-20)
- **Situation**: Plugin system je GA. Distribuce přes marketplace v settings.json.
- **Řešení**: `marketplace.json` v STOPA repo + `github` source v cílových projektech settings.json
- **Metody**: 1) marketplace přes settings.json (doporučeno), 2) `/plugin install`, 3) `--plugin-dir` (dev)
- **Source**: /watch scan, 2026-03-18 → implementace 2026-03-20

## Archived: Agent Teams Native API — DONE (2026-03-19)
- **Situation**: Agent Teams jsou GA — native coordination přes SendMessage, shared task list
- **Potřeba**: /orchestrate deep tier by měl použít native Agent Teams místo manuálních Agent() volání
- **Source**: /watch scan, 2026-03-18

## Archived: Agent Teams — Live Test Findings (2026-03-19)
- **Windows in-process mode works**: `backendType: "in-process"` confirmed functional on Windows 11
- **Explore agents can't shutdown gracefully**: Explore subagent_type lacks SendMessage tool → can't respond to shutdown_request → TeamDelete fails. Workaround: manual cleanup of `~/.claude/teams/` directory.
- **Spawn prompt vs SendMessage**: Teammates start working from spawn prompt immediately. Sending another "start" message via SendMessage causes duplicate work. Best practice: put full instructions in spawn prompt, use SendMessage only for follow-up coordination.
- **Recommendation**: For audit/research tasks, use `subagent_type: "general-purpose"` instead of Explore, so teammates can respond to shutdown and use SendMessage.
- **Fix applied (2026-03-19)**: All Explore references in orchestrate + scout skills replaced with general-purpose. Warning notes added.
- **Source**: Live test — skill-audit team with 2 Sonnet teammates

## Archived: Path-Specific Rules — DONE (2026-03-22)
- **Context**: CLAUDE.md se načítá celý vždy = plýtvání tokeny
- **Pattern**: `.claude/rules/*.md` s glob patternem v hlavičce — pravidla se loadují jen pro relevantní soubory
- **Source**: Video "Claude Certified Architect", 2026-03-22

## Archived: Verifying New Features — Timing Matters
- **Problem**: Sub-agent researching `source: "settings"` (v2.1.80) concluded it doesn't exist because it tested BEFORE the version shipped.
- **Instead**: When agent research contradicts official changelog, trust the changelog. Check CHANGELOG.md directly.
- **Source**: /watch scans, 2026-03-20 → 2026-03-21

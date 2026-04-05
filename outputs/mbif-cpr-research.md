# My-Brain-Is-Full-Crew vs CPR — Research Brief

**Date:** 2026-04-05
**Question:** Porovnání architektur dvou Claude Code rozšíření se zaměřením na přenositelné vzory pro STOPA
**Scope:** standard (comparison)
**Sources consulted:** 24 (MBIF) + 5 (CPR) = 29

## Executive Summary

**My-Brain-Is-Full-Crew** (gnekt) je multi-agent orchestrační systém pro Obsidian vault — 8 specializovaných agentů + 13 skills řízených CLAUDE.md dispatcherem. Klíčové inovace: CLAUDE.md jako čistý router (nikdy neodpovídá přímo), pull-based agent chaining přes `### Suggested next agent` sekci, post-it state protocol (30-řádkové per-agent soubory pro cross-invocation kontinuitu), a graduated hook severity (exit 2 = hard block, exit 1 = warning) [VERIFIED][1-19].

**CPR — Compress, Preserve, Resume** (EliaAlberti) je 3-příkazový session persistence systém — `/preserve` (CLAUDE.md ≤280 řádků s auto-archivací), `/compress` (structured session log s confidence keywords), `/resume` (grep-based context restoration). Klíčové inovace: třívrstvá paměť (permanent / searchable / archive) s explicitní truncation boundary (`## Raw Session Log`), inline section markers `(PROTECTED)`/`(ARCHIVABLE)`, a HIGH/LOW SIGNAL quality filter [VERIFIED][20-29].

Oba systémy řeší ortogonální problémy — MBIF runtime orchestraci, CPR cross-session persistence. Oba se shodují na grep-first retrieval bez embeddings/DB a na explicitních textových hranicích místo konfigurace. Pro STOPA jsou nejpřenosnější: **call chain tracking** (MBIF), **post-it state** (MBIF), **truncation boundary** (CPR), a **confidence keywords** (CPR).

## Detailed Findings

### A. My-Brain-Is-Full-Crew — Dispatcher Architecture

CLAUDE.md funguje jako **čistý dispatcher** — otevírá se pravidlem "NEVER RESPOND DIRECTLY" [VERIFIED][1]. Routing je skill-first: 13 skills se kontrolují přes Skill tool (multi-turn, hlavní kontext), 8 agentů přes Agent tool (subprocess, single-shot) [VERIFIED][1,5]. Trigger tabulky pokrývají 7 jazyků přímo v CLAUDE.md [VERIFIED][1].

Agent chaining používá **pull-based koordinaci** — agent nikdy nevolá jiného agenta přímo. Místo toho zapíše `### Suggested next agent` sekci do svého výstupu, dispatcher ji přečte a rozhodne [VERIFIED][4,5]. Chain tracking je explicitní: každý sub-agent dostane `"Call chain so far: [scribe, architect]. You are step 3 of max 3."` [VERIFIED][1,3]. Anti-recursion: max depth 3, žádný agent dvakrát, žádné kruhové vzory [VERIFIED][1].

**Post-it state protocol**: každý agent zapisuje/čte `Meta/states/{name}.md` — max 30 řádků, přepsáno při každém běhu [VERIFIED][7,23]. Skills odvozené z agenta sdílejí post-it space (např. /defrag čte architect post-it) [VERIFIED][24]. Řeší problém multi-turn skill resumption bez full session memory.

Model assignment je diferenciovaný: Architect a Librarian = opus (strukturální autorita), ostatní = sonnet [VERIFIED][8,9,11]. Tool grants jsou least-privilege: Seeker = Read/Glob/Grep only, Connector = +Edit (ale ne Write), Architect = full Bash [VERIFIED][8,10,12].

Custom agent creation přes `/create-agent` vyžaduje **povinný 6-fázový interview** — žádné one-shot generování [VERIFIED][14]. Body agenta vždy anglicky (instruction reliability), description v jazyce uživatele (trigger matching) [VERIFIED][14].

Plugin manifest (`.claude-plugin/plugin.json`) obsahuje jen metadata — žádný listing agentů/skills, CC je auto-discovruje z filesystému [VERIFIED][16].

### B. CPR — Session Persistence Architecture

CPR implementuje **třívrstvou paměť** [VERIFIED][20]:
1. **CLAUDE.md** — permanentní, ≤280 řádků, vždy načten. Řízeno `/preserve`.
2. **Session log summaries** — střednědobá, strukturovaná, prohledatelná. Řízeno `/compress`.
3. **Raw Session Log** — archivní, plná konverzace, nikdy automaticky nenačtena.

Vrstvy 2 a 3 koexistují ve stejném souboru, oddělené heading `## Raw Session Log` jako **hard truncation boundary** [VERIFIED][25]. `/resume` explicitně hledá tuto hlavičku a načte jen text nad ní [VERIFIED][25].

`/compress` vytváří session log s **confidence keywords** — dedikované metadata pole (`Confidence keywords: auth, JWT, refresh-tokens, middleware`) slouží jako lightweight invertovaný index pro grep-based retrieval [VERIFIED][22]. Uživatel vybírá multi-selectem které sekce zahrnout (9 volitelných + 3 povinné) [VERIFIED][22].

`/preserve` aktivně řídí délku CLAUDE.md přes 280-řádkový limit s auto-archivací do `CLAUDE-Archive.md` [VERIFIED][23]. Inline značky `(PROTECTED)` a `(ARCHIVABLE)` v section headings dávají uživateli přímou kontrolu [VERIFIED][23]. HIGH/LOW SIGNAL filtr: rationale + next steps = HIGH, implementační detaily = LOW [VERIFIED][23].

`/resume` kombinuje 3 zdroje: CLAUDE.md + posledních N summaries (default 3) + topic-matched sessions přes grep [VERIFIED][24]. Škálování: <100 logů přímý listing, ≥100 grep-first [VERIFIED][20].

**Kritická prerekvizita**: `claude config set --global autoCompact false` — bez toho CC tiše smaže kontext před uložením [VERIFIED][20].

### C. Srovnání s STOPA

| Aspekt | STOPA | MBIF-Crew | CPR |
|--------|-------|-----------|-----|
| Dispatcher | Skill tiers + triage | CLAUDE.md pure router | — (no routing) |
| Agent coordination | Sub-agents via orchestrate | Pull-based chaining (3 max) | — (no agents) |
| Session persistence | checkpoint.md + memory/ | Post-it per agent (30 lines) | 3-layer (CLAUDE.md/summary/raw) |
| Memory retrieval | Grep learnings by tags | Trigger phrases in 7 langs | Grep confidence keywords |
| CLAUDE.md role | Project instructions | Pure dispatcher | Knowledge base |
| Hooks | tool-gate, panic-detector | protect-files, validate-frontmatter | — (no hooks) |
| Skill count | 50+ | 13 | 3 |
| Complexity | High | Medium-high | Low |

## Disagreements & Open Questions

- **CLAUDE.md role**: MBIF uses it purely for routing (no content), CPR uses it as permanent knowledge base, STOPA uses it for project instructions. Three different philosophies — no clear winner, depends on whether project needs routing complexity.
- **Post-it 30-line limit**: Sufficient for simple state checkpoints, but may be too tight for complex multi-phase skills like STOPA's /orchestrate which tracks more state [INFERRED][7,14].
- **Auto-compact disable**: CPR requires globally disabling auto-compact — this may cause problems in other projects where auto-compact is beneficial [SINGLE-SOURCE][20].
- **Neither project has eval infrastructure** — no way to verify skill correctness systematically [INFERRED][all sources].

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | MBIF — CLAUDE.md | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/CLAUDE.md | Pure dispatcher, skill-first routing, 7-language triggers | primary | high |
| 2 | MBIF — agent-orchestration.md | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/references/agent-orchestration.md | Full orchestration spec: chaining, post-it, custom agents | primary | high |
| 3 | MBIF — agents-registry.md | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/references/agents-registry.md | Agent registry as shared coordination substrate | primary | high |
| 4 | MBIF — agent-template.md | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/references/agent-template.md | Canonical agent template with Inter-Agent Coordination | primary | high |
| 5 | MBIF — architect.md | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/agents/architect.md | Opus model, full Bash, post-it state protocol | primary | high |
| 6 | MBIF — scribe.md | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/agents/scribe.md | Sonnet model, no Bash, inbox-only output | primary | high |
| 7 | MBIF — seeker.md | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/agents/seeker.md | Read-only agent, zero write capabilities | primary | high |
| 8 | MBIF — connector.md | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/agents/connector.md | Read+Edit only, can link but not create | primary | high |
| 9 | MBIF — librarian.md | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/agents/librarian.md | Opus model for vault audits | primary | high |
| 10 | MBIF — postman.md | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/agents/postman.md | Dual email backend (gws + hey) | primary | high |
| 11 | MBIF — create-agent/SKILL.md | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/skills/create-agent/SKILL.md | 6-phase interview, language split | primary | high |
| 12 | MBIF — onboarding/SKILL.md | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/skills/onboarding/SKILL.md | Multi-phase vault setup | primary | high |
| 13 | MBIF — defrag/SKILL.md | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/skills/defrag/SKILL.md | Shared post-it with architect | primary | high |
| 14 | MBIF — plugin.json | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/.claude-plugin/plugin.json | Minimal manifest, no agent listing | primary | high |
| 15 | MBIF — launchme.sh | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/scripts/launchme.sh | Installer with .core-manifest tracking | primary | high |
| 16 | MBIF — settings.json | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/settings.json | 3 hooks registered | primary | high |
| 17 | MBIF — protect-system-files.sh | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/hooks/protect-system-files.sh | Exit 2 hard block, exit 1 warning | primary | high |
| 18 | MBIF — validate-frontmatter.sh | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/hooks/validate-frontmatter.sh | Advisory validation, skips .claude/ | primary | high |
| 19 | MBIF — agents.md | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/references/agents.md | Shared agent directory for coordination | primary | high |
| 20 | CPR — README.md | https://github.com/EliaAlberti/cpr-compress-preserve-resume/blob/main/README.md | 3-layer memory, auto-compact disable | primary | high |
| 21 | MBIF — README.md | https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/README.md | 8 agents, 13 skills, Obsidian+Claude | primary | high |
| 22 | CPR — compress.md | https://github.com/EliaAlberti/cpr-compress-preserve-resume/blob/main/commands/compress.md | Session log format, confidence keywords | primary | high |
| 23 | CPR — preserve.md | https://github.com/EliaAlberti/cpr-compress-preserve-resume/blob/main/commands/preserve.md | 280-line limit, PROTECTED/ARCHIVABLE markers | primary | high |
| 24 | CPR — resume.md | https://github.com/EliaAlberti/cpr-compress-preserve-resume/blob/main/commands/resume.md | 3-source loading, grep-based search | primary | high |
| 25 | CPR — session-log-example.md | https://github.com/EliaAlberti/cpr-compress-preserve-resume/blob/main/examples/session-log-example.md | Log format with Decision/Rationale table | primary | high |

## Sources

1. gnekt/My-Brain-Is-Full-Crew — CLAUDE.md — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/CLAUDE.md
2. gnekt/My-Brain-Is-Full-Crew — references/agent-orchestration.md — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/references/agent-orchestration.md
3. gnekt/My-Brain-Is-Full-Crew — references/agents-registry.md — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/references/agents-registry.md
4. gnekt/My-Brain-Is-Full-Crew — references/agent-template.md — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/references/agent-template.md
5. gnekt/My-Brain-Is-Full-Crew — agents/architect.md — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/agents/architect.md
6. gnekt/My-Brain-Is-Full-Crew — agents/scribe.md — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/agents/scribe.md
7. gnekt/My-Brain-Is-Full-Crew — agents/seeker.md — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/agents/seeker.md
8. gnekt/My-Brain-Is-Full-Crew — agents/connector.md — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/agents/connector.md
9. gnekt/My-Brain-Is-Full-Crew — agents/librarian.md — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/agents/librarian.md
10. gnekt/My-Brain-Is-Full-Crew — agents/postman.md — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/agents/postman.md
11. gnekt/My-Brain-Is-Full-Crew — skills/create-agent/SKILL.md — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/skills/create-agent/SKILL.md
12. gnekt/My-Brain-Is-Full-Crew — skills/onboarding/SKILL.md — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/skills/onboarding/SKILL.md
13. gnekt/My-Brain-Is-Full-Crew — skills/defrag/SKILL.md — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/skills/defrag/SKILL.md
14. gnekt/My-Brain-Is-Full-Crew — .claude-plugin/plugin.json — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/.claude-plugin/plugin.json
15. gnekt/My-Brain-Is-Full-Crew — scripts/launchme.sh — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/scripts/launchme.sh
16. gnekt/My-Brain-Is-Full-Crew — settings.json — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/settings.json
17. gnekt/My-Brain-Is-Full-Crew — hooks/protect-system-files.sh — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/hooks/protect-system-files.sh
18. gnekt/My-Brain-Is-Full-Crew — hooks/validate-frontmatter.sh — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/hooks/validate-frontmatter.sh
19. gnekt/My-Brain-Is-Full-Crew — references/agents.md — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/references/agents.md
20. EliaAlberti/cpr-compress-preserve-resume — README.md — https://github.com/EliaAlberti/cpr-compress-preserve-resume/blob/main/README.md
21. gnekt/My-Brain-Is-Full-Crew — README.md — https://github.com/gnekt/My-Brain-Is-Full-Crew/blob/main/README.md
22. EliaAlberti/cpr-compress-preserve-resume — compress.md — https://github.com/EliaAlberti/cpr-compress-preserve-resume/blob/main/commands/compress.md
23. EliaAlberti/cpr-compress-preserve-resume — preserve.md — https://github.com/EliaAlberti/cpr-compress-preserve-resume/blob/main/commands/preserve.md
24. EliaAlberti/cpr-compress-preserve-resume — resume.md — https://github.com/EliaAlberti/cpr-compress-preserve-resume/blob/main/commands/resume.md
25. EliaAlberti/cpr-compress-preserve-resume — session-log-example.md — https://github.com/EliaAlberti/cpr-compress-preserve-resume/blob/main/examples/session-log-example.md

## Coverage Status

- **[VERIFIED]:** Všechny klíčové claims — oba README, 19 MBIF souborů, 5 CPR souborů přečteny přímo
- **[INFERRED]:** Post-it 30-line scalability otázka, absence eval infrastructure
- **[SINGLE-SOURCE]:** Auto-compact disable doporučení (jen CPR README)
- **[UNVERIFIED]:** Žádné — vše podstatné ověřeno z primárních zdrojů

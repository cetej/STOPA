# Session Checkpoint

**Saved**: 2026-04-03 (evening)
**Task**: Behavioral Genome + Radar scan
**Branch**: main

## Co je hotovo

### Radar scan #2 (2026-04-03) ✓
- Proaktivní scan (10 searches, 5 fetches)
- 5 nových tools → Watch List: Strands Agents (6/10), Google Colab MCP (6/10), Gemini CLI (6/10), Mastra (5/10), MCPCore (5/10)
- Deepresearch na claude-code-sdk-python (8/10) DONE → `outputs/radar-claude-code-sdk-python-2026-04-03.md`
- radar.md aktualizován (11 tools celkem)

### Behavioral Genome v1 (2026-04-03) ✓
- Root cause analýza "lobotomie" problému: feedback memories se ztrácí při kompresi, nejsou direktivní
- Implementace: `.claude/rules/behavioral-genome.md` (59 řádků) — syntetizováno z 18 feedback memories + 10 critical patterns
- Umístění v `rules/` = auto-load na každý edit, compression-proof
- P0 DONE, P1-P3 pending (viz níže)

## Pending (P1-P3 Behavioral Genome)

### P1: genome-synthesize.py Stop hook (2-3h)
- Python hook na Stop event
- Čte feedback memories + critical-patterns + corrections.jsonl
- Volá Haiku pro syntézu → regeneruje behavioral-genome.md
- Diffne proti předchozí verzi → drift score
- Přidat do settings.json Stop hooks

### P2: Fix auto-scribe.py / patterns.md (1h)
- patterns.md je PRÁZDNÝ — auto-scribe.py pravděpodobně nedostává session-summary.json
- Diagnostikovat: session-summary.sh generuje? auto-scribe.py čte správně?

### P3: Drift score v /status (1h)
- Přidat do /status skillu: porovnání aktuální behavioral-genome verze s předchozí
- Metrika konzistence chování

## Odložené úkoly (z minulých sessions)

### NG-ROBOT Media Expansion — Fáze 1b
- Bundle processing dialog (checkpoint v NG-ROBOT auto-memory)
- Projekt: C:\Users\stock\Documents\000_NGM\NG-ROBOT

### Hippocampus Fáze 3c/3d
- Cross-project graph merge + model gating
- Soubory: `.claude/hooks/lib/associative_engine.py`

## Resume prompt

```
Session pokračování v STOPA.

POSLEDNÍ PRÁCE:
- Behavioral Genome v1 je LIVE v .claude/rules/behavioral-genome.md
- Radar scan hotový, radar.md aktuální (11 tools)

CO DĚLAT DÁL (dle priority):
1. P1: Implementovat genome-synthesize.py Stop hook — auto-regenerace genome z feedback memories
2. P2: Diagnostikovat proč patterns.md je prázdný (auto-scribe.py bug)
3. P3: Drift score do /status skillu

SOUBORY:
- .claude/rules/behavioral-genome.md (genome v1)
- .claude/memory/radar.md (11 tools)
- .claude/settings.json (hooks config)
- .claude/hooks/ (hook skripty)
```

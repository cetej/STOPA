# Session Checkpoint

**Saved**: 2026-04-03
**Task**: Hippocampus integration — asociativní paměť (ADR 0012)
**Branch**: main

## Co je hotovo

### Fáze 1: "Živý systém" ✓
- **1a** `memory-whisper.py` — auto-increment `uses:` při retrieval. Ověřeno: 13 learnings dostalo uses=1 z jednoho test promptu.
- **1b** `critic.md` — instrukce pro `harmful_uses` feedback loop (After Review sekce, bod 7).
- **1c** `learning-lifecycle.py` — SessionStart hook: promotion (uses>=10), retirement (harmful>=3), stale flagging (60d+).

### Fáze 2: "Asociativní vrstva" ✓
- **2a** `concept-graph.json` — 451 entit, 4329 hran, z 52 learnings.
- **2b-c** `lib/associative_engine.py` — spreading activation engine. Latence: **24ms**.
- **2d** `associative-recall.py` — UserPromptSubmit hook, 800-token budget.
- **Graph rebuild** `graph-consolidate.sh` — Stop hook.

## Co zbývá — Fáze 3: "Transformace"

### 3a. Hebbian learning z session traces
- Napojit trace-capture.py výstupy jako zdroj konceptů pro graph
- Session-specific edge weight boosting

### 3b. Auto-skill crystallization
- Implementovat skill_detector.py (hippocampus archetype patterns)
- Cross-project detection

### 3c. Cross-project memory transfer
- Sdílený concept-graph přes projekty

### 3d. Contrastive model gating
### 3e. Graph optimalizace (pruning, normalization, compact format)

## Resume prompt

```
Pokračuj v implementaci Hippocampus integrace — Fáze 3.
Přečti checkpoint.md a ADR 0012 (docs/decisions/0012-associative-memory-upgrade.md).
Přečti project_hippocampus_integration.md v auto-memory.
Hlavní soubory: .claude/hooks/lib/associative_engine.py, .claude/hooks/associative-recall.py,
.claude/hooks/memory-whisper.py, .claude/hooks/learning-lifecycle.py.
Začni s 3a (Hebbian learning z session traces).
```

## Klíčové soubory

| Soubor | Role |
|--------|------|
| `.claude/hooks/lib/associative_engine.py` | Core engine: graph build, activation, packet |
| `.claude/hooks/associative-recall.py` | UserPromptSubmit hook (auto-injection) |
| `.claude/hooks/memory-whisper.py` | Keyword recall + uses tracking |
| `.claude/hooks/learning-lifecycle.py` | SessionStart: promotion/retirement/stale |
| `.claude/hooks/graph-consolidate.sh` | Stop: graph rebuild |
| `.claude/memory/concept-graph.json` | Graph data (451 entities, 4329 edges) |
| `docs/decisions/0012-associative-memory-upgrade.md` | ADR |

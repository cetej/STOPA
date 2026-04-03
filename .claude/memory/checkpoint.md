# Session Checkpoint

**Saved**: 2026-04-03
**Task**: Hippocampus integration — Fáze 3 (Transformace)
**Branch**: main

## Co je hotovo

### Fáze 1: "Živý systém" ✓
- **1a** `memory-whisper.py` — auto-increment `uses:` při retrieval.
- **1b** `critic.md` — instrukce pro `harmful_uses` feedback loop.
- **1c** `learning-lifecycle.py` — SessionStart hook: promotion/retirement/stale.

### Fáze 2: "Asociativní vrstva" ✓
- **2a-c** `concept-graph.json` + `lib/associative_engine.py` — 451 entit, 4329 hran, 24ms latence.
- **2d** `associative-recall.py` — UserPromptSubmit hook, 800-token budget.

### Fáze 3: "Transformace" (částečně ✓)
- **3a** ✓ `hebbian-consolidate.py` — Stop hook. Čte activity-log.md + trace JSONL, extrahuje koncepty ze session aktivity, zesiluje co-occurrence hrany v grafu. Registrován v settings.json (Stop).
- **3b** ✓ `skill-detector.py` — SessionStart hook. Hledá dense concept clusters (4+ konceptů, avg weight > 3.0), detekuje cross-project patterns (3+ kontextů). Pasivní — jen navrhuje, nevytváří skills. Registrován v settings.json (SessionStart).
- **3e** ✓ `associative_engine.py` — nové funkce: `optimize_graph()` (decay, prune weak edges <0.05, cap weights at 50, remove orphan entities, compact data), `graph_health()` (monitoring metriky). CLI: `optimize`, `health`. `graph-consolidate.sh` nyní volá optimize po buildu.

## Co zbývá — Fáze 3 pokračování

### 3c. Cross-project memory transfer
- Sdílený concept-graph přes projekty (workspace context boosting existuje, chybí merge logika)

### 3d. Contrastive model gating
- Auto-detect model-specific learnings, filtr při retrieval

## Resume prompt

```
Pokračuj v implementaci Hippocampus integrace — Fáze 3c/3d.
Přečti checkpoint.md a ADR 0012 (docs/decisions/0012-associative-memory-upgrade.md).
Hlavní soubory: .claude/hooks/lib/associative_engine.py, .claude/hooks/hebbian-consolidate.py,
.claude/hooks/skill-detector.py.
3c: Cross-project graph merge (concept-graph z více projektů).
3d: Model gating (model_gate field v learnings → filtr při activation).
```

## Klíčové soubory

| Soubor | Role |
|--------|------|
| `.claude/hooks/lib/associative_engine.py` | Core engine: build, activate, optimize, health |
| `.claude/hooks/associative-recall.py` | UserPromptSubmit: auto-injection |
| `.claude/hooks/hebbian-consolidate.py` | Stop: Hebbian edge strengthening z session |
| `.claude/hooks/skill-detector.py` | SessionStart: emergent skill pattern detection |
| `.claude/hooks/memory-whisper.py` | Keyword recall + uses tracking |
| `.claude/hooks/learning-lifecycle.py` | SessionStart: promotion/retirement/stale |
| `.claude/hooks/graph-consolidate.sh` | Stop: graph rebuild + optimize |
| `.claude/memory/concept-graph.json` | Graph data (451 entities, 4329 edges) |
| `docs/decisions/0012-associative-memory-upgrade.md` | ADR |

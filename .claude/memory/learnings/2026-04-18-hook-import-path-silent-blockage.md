---
date: 2026-04-18
type: bug_fix
severity: critical
component: hook
tags: [signal-pipeline, atomic_write, sys-path, silent-failure, evolve-input]
summary: 8 hooks měly chybnou sys.path (.parent.parent místo .parent.parent.parent) → ModuleNotFoundError při import atomic_utils → tichá smrt 17 dní. Žádný signál do corrections.jsonl, panic-state.json, uses-ledger. /evolve běžel slepě nad zmrzlými daty.
source: critic_finding
uses: 2
harmful_uses: 0
successful_uses: 0
confidence: 1.00
maturity: validated
verify_check: "manual"  # Defense is verify-sweep smoke test (STOPA_VERIFY_HOOKS=1), not static regex
skill_scope: [evolve, scribe, watch]
failure_class: integration
failure_agent: hook
task_context: {task_class: bug_fix, complexity: high, tier: standard}
---

# Hook Import Path Silent Blockage (17 dní bez signálu)

## Co se stalo

Commit `269ffdb` (2026-04-01 14:51) zavedl `scripts/atomic_utils.py` v root repozitáře pro atomic file writes. Současně retrofitoval 9 hooků na `from atomic_utils import atomic_write`. Ale do 8 z nich vepsal chybnou cestu:

```python
# CHYBA — resolveuje na .claude/scripts (neexistuje)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
```

Správně musí být **3 parents** (file → hooks/ → .claude/ → STOPA/):

```python
# OK — resolveuje na STOPA/scripts
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
```

Pouze `autodream.py` měl správnou variantu s explicitním `_REPO_ROOT` a komentářem.

## Důsledky

8 hooků padalo s `ModuleNotFoundError` na importu, exit 1, žádný výstup:
- `correction-tracker.py` — corrections.jsonl zmrzlá od 2026-04-01
- `panic-detector.py` — panic-state.json nikdy nevytvořen
- `stagnation-detector.py` — signal lost (ale měl jinou bug — viz níže)
- `verify-sweep.py` — částečně padá při atomic_write
- `auto-scribe.py` — auto-learning broken
- `uses-tracker.py` — uses counters zmrzlé na 0 (vysvětluje proč 150+ learnings má `uses: 0`)
- `sidecar-queue.py` — deferred suggestions broken
- `auto-compound-agent.py` — broken

`/evolve` 9× běžel nad zmrzlými daty (#5-#9), opakoval "0 new corrections, 0 graduation candidates" jako healthy state — ve skutečnosti slepota.

## Detekční vzor

User prompt "možná by stálo za hlubší analýzu, zda potřebné signály nejsou blokovány nefunkčními smyčkami" → systematická kontrola: pro každý očekávaný signal file zkontroluj (a) zda existuje, (b) kdy byl naposledy aktualizován, (c) ručně spusť hook s sample payloadem. Sparseness != absence problému; může být silent failure.

## Také opraveno

`stagnation-detector.py` měl variantu `_hook_dir.parent.parent / "scripts"` kde `_hook_dir` už byl directory hooks/ (ne file). Tady byly 2 parents správné. Při fixu jsem ji omylem porušil přidáním 3. parent — proto je třeba **zkontrolovat zda proměnná drží file path nebo dir path před přidáním .parent**.

`skill-usage-tracker.sh` měl jiný bug — četl jen `CLAUDE_TOOL_INPUT` env var, nepodporoval stdin JSON. Sourozenec `skill-context-tracker.sh` má robustní fallback pattern (stdin → env), který jsem přenesl.

## Co dělat příště

1. **Po commitu hooks atomic-utility nebo společné lib**: spustit `for h in .claude/hooks/*.py; do echo "" | python "$h" 2>&1 | head -1; done` — detekuje import errors okamžitě.
2. **Add verify-sweep check**: každý hook musí být import-clean. Failed imports = critical violation.
3. **Konvence cest**: vždy přidat komentář `# .claude/hooks/ → .claude/ → repo root → scripts/` jako autodream.py — usnadňuje code review.
4. **Path math je whitelistový**: `Path(__file__).resolve().parent` (od file) potřebuje +1 parent navíc oproti `Path(__file__).resolve().parent.parent` (od hook dir).

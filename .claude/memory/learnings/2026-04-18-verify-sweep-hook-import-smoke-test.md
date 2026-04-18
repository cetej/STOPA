---
date: 2026-04-18
type: best_practice
severity: high
component: hook
tags: [verify-sweep, hook-health, session-start, import-check, defense-in-depth]
summary: verify-sweep.py přidán smoke-test pro hook importability — in-process importlib přes všechny .claude/hooks/*.py. Detekuje ModuleNotFoundError/ImportError/SyntaxError při každém SessionStart (~1.6s runtime). Prevence dalšího 17-denního tichého blackoutu jako u commit 269ffdb.
source: critic_finding
uses: 0
harmful_uses: 0
successful_uses: 0
confidence: 0.85
maturity: draft
verify_check: "Grep('STOPA_VERIFY_HOOKS', path='.claude/hooks/verify-sweep.py') → 1+ matches"
skill_scope: [evolve, scribe, autoloop]
task_context: {task_class: feature, complexity: medium, tier: standard}
---

# Hook Import-Health Smoke Test

## Problem

Commit 269ffdb (2026-04-01) zavedl `from atomic_utils import atomic_write` do 8 hooků s chybnou `sys.path`. Výsledek: `ModuleNotFoundError` při každé invokaci, exit 1, žádný output. 17 dní ticha než audit detekoval.

Bez aktivní detekce může stejná třída bugů nastat znovu při:
- Zavedení nové shared utility
- Rename souboru který je importován
- Python upgrade který mění resolution
- Chybné copy-paste `sys.path.insert`

## Řešení

Nová sekce v `.claude/hooks/verify-sweep.py` (SessionStart hook) provádí smoke-test:

```python
import importlib.util, py_compile
for hook_file in hooks_dir.glob("*.py"):
    # Step 1: syntax check (~1-2ms)
    py_compile.compile(hook_file, doraise=True, quiet=1)
    # Step 2: import resolve (~5-10ms)
    spec = importlib.util.spec_from_file_location("x", hook_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # catches ModuleNotFoundError/ImportError
```

**Runtime**: 1.6s pro ~60 Python hooků (in-process, žádný subprocess boot).

**Gate**: `STOPA_VERIFY_HOOKS=1` env var v settings.json (opt-in, default ON v STOPA).

**Skip list**: library soubory (underscore naming): `atomic_utils.py`, `sidecar_queue.py`, `error_classifier.py`, atd.

**Side effect risk**: executing module-level code může triggerovat I/O (panic-detector čte state.json, atd.). Mitigováno: `except SystemExit: pass` a `except Exception: pass` — jen ModuleNotFoundError/ImportError/SyntaxError se hlásí.

## Ověřeno

Negativní test: temporarily nahrazen `from atomic_utils import` za `from nonexistent_module import` → verify-sweep vyhlásil violation:
```
✗ [hooks/correction-tracker.py] hook import broken
    check: importlib.spec_from_file_location → no ImportError
    found: ModuleNotFoundError: No module named 'nonexistent_module'
```

## Limitace

- Neoveří .sh hooky (syntax check bash = composable, ale importování není tak snadné)
- Neoveří runtime chyby mimo imports (např. `open(file)` který neexistuje — ale to není klasická silent-failure třída)
- Subprocess-based smoke test (původní návrh) byl 80s — in-process je 50× rychlejší, ale má vyšší side-effect risk

## Co dělat pokud detekce flaguje hook

1. Grep výstup: `find: ModuleNotFoundError: No module named 'X'`
2. Zkontrolovat `sys.path.insert(...)` v daném hooku — cesta správná?
3. Zkontrolovat jestli modul `X` existuje v `scripts/` (repo root) nebo `.claude/hooks/`
4. Pokud je to přejmenování: oprav importy nebo vrať starý název

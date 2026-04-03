---
category: python-dependencies
severity: high
last_updated: 2026-04-03
---

# Python & Dependencies — Runbook

## ModuleNotFoundError

**Symptom:** `ModuleNotFoundError: No module named 'X'`
**Cause:** Wrong venv active, or dependency not installed
**Fix:**
1. Check active venv: `which python` or `where python`
2. `pip install -e .` or `pip install <missing-package>`

**Prevention:** Always activate venv before running code

---

## UnicodeDecodeError on Windows

**Symptom:** `UnicodeDecodeError: 'charmap' codec can't decode byte`
**Cause:** Missing `encoding='utf-8'` in file operations
**Fix:**
1. Add `encoding='utf-8'` to all `open()` calls
2. For stdout: `sys.stdout.reconfigure(encoding='utf-8', errors='replace')`

**Prevention:** Project rule — always specify encoding explicitly

---

## ImportError: cannot import name X

**Symptom:** `ImportError: cannot import name 'X' from 'module'`
**Cause:** Circular import or renamed module
**Fix:**
1. Check import chain — look for circular dependencies
2. Verify module/function name matches current code (may have been renamed)

---

## CUDA out of memory

**Symptom:** `RuntimeError: CUDA out of memory`
**Cause:** Model too large for available GPU memory
**Fix:**
1. Use CPU fallback: `device='cpu'`
2. Reduce batch size
3. Use `torch.cuda.empty_cache()` before loading

**Prevention:** Check GPU memory before loading large models

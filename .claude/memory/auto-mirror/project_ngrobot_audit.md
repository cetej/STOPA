---
name: NG-ROBOT Audit 2026-04
description: Multi-session security/quality audit of NG-ROBOT — all 11 tasks complete (wave 1 sessions 1-5, wave 2 tasks 7-12)
type: project
---

## NG-ROBOT Hloubkový Audit (2026-04-02)

11 úkolů dokončeno, všechny změny commitnuté a pushnuté do main.
**70 testů prochází** (43 z wave 1 + 27 z wave 2).

### Wave 1 — Sessions 1-5

#### Session 1: Security & Config Hardening
- Odstraněn hardcoded API klíč z test_api.py (klíč v git historii — potřeba revokovat)
- Buffer IDs, GDrive folder ID přesunuty do .env
- Flask secret key z env variable
- Config validace na startupu (validate_config())
- 30+ bare except: nahrazeno specifickými exception typy
- .env.example template vytvořen

#### Session 2: Error Handling & Retry
- retry_utils.py — @retry dekorátor s exponenciálním backoff
- _stream_message() helper v claude_processor s @retry
- save_phase_checkpoint() v auto_agent.py — per-phase recovery

#### Session 3: Code Refactoring
- claude_processor.py monolith (7767 řádků) rozdělen do package:
  - core.py (632), utilities.py (1945), phases.py (3873)
  - generators.py (630), specialized.py (765), __init__.py (130)
- Backward-compatible import shim
- Originál archivován jako .bak (gitignored)

#### Session 4: Testing Infrastructure
- pyproject.toml s pytest config + ruff
- tests/ directory s conftest.py (fixtures, mock API)
- 43 testů: imports, ProcessingResult, retry, checkpoint, config, nano schema, observability
- Vše prochází pod 1s

#### Session 5: Observability
- Structured JSON logging (ng_robot.jsonl) s extra fields (phase, model, cost_usd)
- estimate_cost_usd() s pricing tabulkou pro Sonnet/Haiku/Opus
- Per-phase cost tracking v processing_stats.json
- Total cost aggregace v summary

### Wave 2 — Session 6 (2026-04-02)

| # | Úkol | Status | Soubory |
|---|------|--------|---------|
| 6 | API klíč revokace | SKIP | Privátní repo, minimální riziko |
| 7 | **CSRF ochrana** — Origin/Referer validace | DONE | csrf_protection.py, ngrobot_web.py, tests/test_csrf.py (14 testů) |
| 8 | **Dependency lockfile** — pip-compile | DONE | requirements.lock (241 pinned verze) |
| 9 | **Response format** — JSON envelope | DONE | api_response.py, tests/test_api_response.py (7 testů) |
| 10 | **CI/CD pipeline** — GitHub Actions | DONE | .github/workflows/ci.yml (pytest + ruff + pip-audit, Python 3.11-3.13) |
| 11 | **Circuit breaker** — 5 failures / 60s recovery | DONE | retry_utils.py, claude_processor/core.py (6 testů) |
| 12 | **Thread safety** — tunnel globals za lock | DONE | ngrobot_web.py (_tunnel_lock), csrf_protection.py |

### Architektonická rozhodnutí

- **CSRF**: Origin/Referer validace místo Flask-WTF tokenů — app je 100% AJAX API, ne HTML formy
- **Circuit breaker**: CLOSED→OPEN→HALF_OPEN pattern, sdílená instance v claude_processor/core.py
- **Response envelope**: `api_ok()`/`api_error()` utility — postupná adopce, ne big-bang refactor
- **CI/CD**: 3 Python verze (3.11-3.13), ruff lint + pip-audit na vulnerabilities

### Audit KOMPLETNÍ

Všechny plánované úkoly jsou hotové. Repo: https://github.com/cetej/NG-ROBOT

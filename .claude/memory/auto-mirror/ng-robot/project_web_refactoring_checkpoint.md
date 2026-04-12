---
name: Web UI refactoring checkpoint
description: Stav refaktoringu ngrobot_web.py — blueprinty HOTOVÉ (9 souborů, 171 routes), logging HOTOVÝ. Zbývá: helper/task extraction (optional).
type: project
---

## Checkpoint 2026-03-19 — Blueprinty + Logging DOKONČENO

### Hotovo

**#15/#17 Blueprinty + logging — COMPLETE**
- 9 blueprintů v `blueprints/` (171 routes, 5,972 řádků):
  - `articles_bp.py` (61 routes, 2,654 ř.)
  - `system_bp.py` (27 routes, 494 ř.)
  - `schedule_bp.py` (19 routes, 561 ř.)
  - `analytics_bp.py` (18 routes, 324 ř.)
  - `batch_bp.py` (16 routes, 510 ř.)
  - `monitor_bp.py` (9 routes, 123 ř.)
  - `performance_bp.py` (8 routes, 130 ř.)
  - `media_bp.py` (8 routes, 221 ř.)
  - `pages_bp.py` (5 routes, 355 ř.)
- `init_blueprints()` registruje vše (ř. 2593)
- Logging: 23 print() → logger.info/warning/error
- Logger: file handler (ERROR+) + console handler (INFO+)

### Optional Future Work

**Helper extraction (P4) — nízká priorita**
- 43 helper funkcí (2,400 ř.) v ngrobot_web.py
- Možné moduly: content_converter.py, article_inspector.py, media_utilities.py
- Risk: blueprinty importují tyto helpers → musí se aktualizovat importy

**Task extraction (P4) — nízká priorita**
- 34 task worker funkcí (2,362 ř.) v ngrobot_web.py
- Možné moduly: tasks/processing.py, tasks/media.py, tasks/integration.py
- Risk: queue_manager.register() musí najít funkce

**Why optional:** ngrobot_web.py funguje, blueprinty řeší hlavní bolest (navigace routes). Helper/task extraction je nice-to-have.

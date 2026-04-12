---
name: STOPA meta-project
description: STOPA is the source of truth for the Claude Code orchestration system — skills, shared memory, sync to target projects (NG-ROBOT, test1, ADOBE-AUTOMAT)
type: project
---

STOPA je meta-projekt pro vývoj orchestračního systému Claude Code.

**Why:** Orchestrace se vyvíjela v test1, pak se kopírovala do ng-robot a ADOBE-AUTOMAT — vznikal chaos. STOPA centralizuje vývoj.

**How to apply:** Změny skills a memory se dělají tady, do cílových projektů se distribuují přes `scripts/sync-orchestration.sh`.

Cílové projekty:
- NG-ROBOT (cetej/NG-ROBOT) — hlavní projekt na desktopu
- test1 (cetej/test1) — Pyramid Flow, web session
- ADOBE-AUTOMAT (cetej/ADOBE-AUTOMAT) — Adobe automatizace

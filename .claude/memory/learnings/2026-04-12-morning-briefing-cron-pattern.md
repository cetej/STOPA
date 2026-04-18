---
date: 2026-04-12
type: best_practice
severity: medium
component: orchestration
tags: [scheduled-tasks, cron, morning-briefing, automation, memory]
summary: "Morning briefing cron pattern: single claude -p command reads Memory.md + new raw sources from last 24h + prints terminal digest. Set once, runs forever. Directly implementable as STOPA scheduled task."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 1.0
verify_check: "manual"
---

# Morning Briefing Cron Pattern

## Detail

Praktický pattern z Karpathy LLM Wiki tutoriálu:

```bash
claude -p "Write a Python script called morning_digest.py that:
1) reads Memory.md and surfaces any open actions due today
2) reads any new files added to /raw-sources in the last 24 hours
3) prints a clean briefing to the terminal.
Then schedule it as a cron job every morning at 7:30am." --allowedTools Bash,Write
```

Pattern: nastavit jednou → autonomní daily digest bez ruční interakce.

## Application to STOPA

Implementovatelné jako STOPA scheduled task (mcp__scheduled-tasks):
- Čte `.claude/memory/state.md` a `checkpoint.md` pro open tasks
- Čte `news.md` pro nové /watch výsledky
- Kontroluje nové soubory v `outputs/` za posledních 24h
- Tiskne/posílá stručný briefing (terminal nebo Telegram)

**Why:** Bez daily briefing se otevřené tasky ztrácí mezi sessions. Briefing = nízkonákladový glue mezi sessions.

**How to apply:** Při nastavování nového projektu zvážit morning_digest scheduled task. V STOPA: rozšířit autodream.py nebo vytvořit separátní `morning-brief.py` scheduled task.

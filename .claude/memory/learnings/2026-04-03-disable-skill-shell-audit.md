---
date: 2026-04-03
type: architecture
severity: high
component: skill
tags: [shell, security, cc-settings, disableSkillShellExecution]
summary: "CC v2.1.91 přidalo disableSkillShellExecution. Audit: 25/48 (52%) STOPA skills má inline shell. Zapnutí by rozbilo polovinu systému. NEPOVOLOVAT bez migrace skills na pure-tool approach."
source: auto_pattern
uses: 1
harmful_uses: 0
confidence: 0.85
verify_check: "Grep('```bash', path='.claude/skills/') → 20+ matches"
successful_uses: 0
---

## CC v2.1.91 — `disableSkillShellExecution` Setting

Nové nastavení v Claude Code v2.1.91 umožňuje blokovat inline shell execution v skills a custom commands.

### Audit výsledky (2026-04-03)

- **25 z 48 skills (52%)** obsahuje inline shell execution
- **Kategorie shell usage:**
  - Git operations (8 skills): autoloop, autoresearch, evolve, incident-runbook, scribe, systematic-debugging, critic, sweep
  - GitHub CLI (3): autofix, fix-issue, pr-review
  - Code quality (2): verify, critic — mypy, ruff, pytest
  - External tools (3): klip, nano, youtube-transcript
  - File system (6): harness, compact, project-init, project-sweep, scenario, seo-audit, eval
  - Package mgmt (1): budget — ccusage
  - Orchestration (2): orchestrate, autoharness

### Rozhodnutí

**NEPOVOLOVAT `disableSkillShellExecution`** v STOPA projektech. Migrace na pure-tool approach by vyžadovala přepis 25 skills.

### Kdy přehodnotit

- Pokud CC přidá granulární shell permissions per-skill (ne binary on/off)
- Pokud CC přidá dedicated tools nahrazující běžné shell patterny (git, gh, pytest)

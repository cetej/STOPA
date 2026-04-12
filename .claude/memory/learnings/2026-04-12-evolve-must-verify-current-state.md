---
date: 2026-04-12
type: anti_pattern
severity: high
component: memory
tags: [evolve, maintenance, race-condition, state-verification, parallel-sessions]
summary: "/evolve a maintenance skills MUSÍ ověřit aktuální stav souborového systému (Glob/Read) před doporučením akce. Čtení vlastního logu nebo předpokládání stavu z minulého běhu vede k opakovaným falešným doporučením — wiki existovala, ale evolve ji 7x doporučil vytvořit."
source: user_correction
uses: 0
harmful_uses: 0
confidence: 0.9
successful_uses: 0
verify_check: "manual"
skill_scope: [evolve, sweep, compile, dreams]
failure_class: assumption
task_context: {task_class: bug_fix, complexity: medium, tier: standard}
---

## Evolve Must Verify Current State, Not Trust Own Log

### Problem
/evolve četl evolution-log.md a viděl opakující se "RECOMMEND: /compile (wiki not built)".
Místo ověření `Glob('.claude/memory/wiki/INDEX.md')` důvěřoval vlastnímu záznamu.
Wiki přitom existovala — vytvořena v jiné session.

### Root Cause
Paralelní sessions (manuální + scheduled tasks) mění stav nezávisle.
Poslední zapisovatel vyhrává, žádný reconciliation mechanismus.
Evolve (a jakýkoliv maintenance skill) čte stav na začátku session,
ale stav se mohl změnit v jiné session mezi dvěma evolve běhy.

### Rule
PŘED každým RECOMMEND/PROMOTE/CREATE ověř aktuální stav:
- `Glob()` pro existenci souborů
- `Read()` pro obsah
- `Grep()` pro přítomnost vzorů
Nikdy nedůvěřuj vlastnímu logu nebo předchozím evolve záznamům jako zdroji pravdy.

### Broader Pattern
Toto je instance obecnějšího problému: **stale read**.
Platí pro všechny maintenance skills (sweep, compile, dreams, evolve).
Scheduled tasks jsou obzvlášť náchylné — běží v izolaci,
nevidí změny z manuálních sessions.

---
date: 2026-04-19
type: best_practice
severity: medium
component: orchestration
tags: [cross-project, adoption, agpl, osint, monitor]
summary: Clean-room adoption AGPL-3.0 projektů bez copy-paste — 3 paralelní Explore agenti pro strukturální analýzu, pak syntéza do Tier A/B/C/D roadmapy, NOTICE.md s atribucí, implementace v target-project stylu.
source: auto_pattern
uses: 4
harmful_uses: 0
successful_uses: 0
confidence: 1.00
maturity: draft
task_context: {task_class: cross_project, complexity: high, tier: deep}
verify_check: "Glob('.claude/memory/learnings/*worldmonitor*') → 1+ matches"
related: [2026-04-14-paseo-orchestration-patterns.md]
---

## Pattern: Cross-project OSS adoption bez licenčního rizika

### Kontext
User požádal o hloubkovou analýzu worldmonitor (48.9k★, AGPL-3.0) → převzetí
do MONITOR projektu (AGPL-3.0, zero-dep Express stack). WorldMonitor má ~10 MB
TypeScript, 2636 souborů — příliš velké na sériové čtení.

### Řešení (4 kroky)

1. **Paralelní průzkum přes 3 Explore agenty** — ne sekvenční čtení.
   - Agent 1: feeds + ingestion pipeline
   - Agent 2: scoring + correlation + AI synthesis
   - Agent 3: map layers + UI + variants
   - Každý s word limit (~800-1000 slov) → šetří hlavní kontext

2. **Tier A/B/C/D klasifikace** při syntéze:
   - A = copy-paste s adaptací (1-2 týdny, vysoká hodnota)
   - B = adaptace algoritmu (2-3 týdny, core intelligence)
   - C = inspirace patternů (volitelné, selektivně)
   - D = SKIP (over-engineered nebo mimo target stack)

3. **Clean-room implementace** místo copy-paste — vlastní kód v target-project
   stylu (u MONITORu: .mjs, zero-dep, ES modules). Algoritmy nejsou copyrighted,
   jen konkrétní kód. Výhody:
   - Právní čistota (copyright chrání kód, ne nápady)
   - Code fit do existujícího stacku (žádné zbytečné abstrakce)
   - Učení — pochopení algoritmu > copy-paste slepá víra

4. **NOTICE.md s atribucí** pro AGPL Section 7 compliance:
   - Tabulka "MONITOR file ← inspired by WorldMonitor file"
   - Explicit statement "No source code copied verbatim"
   - License + copyright holder

### Výsledek
Sprint 1 za jednu session: 4 nové moduly (1195 řádků), 60 feedů katalogizováno,
80-86% health pro validovatelné feedy, MONITOR získal tier reputation + Unicode
safety + feed health monitoring.

### Red flags pro jinde
- **Nepoužívat pro MIT/BSD projekty** — tam je copy-paste OK, clean-room je
  zbytečná práce (použij přímou extrakci).
- **Pouze pro AGPL/GPL/copyleft** nebo projekty s restriktivními license claims.
- **Scope creep risk** — při syntéze Tier C je lákavé přidat "ještě tohle".
  Držet se Tier A pro první sprint, ostatní navrhnout jako roadmap.

### Kdy neaplikovat
- Malý projekt (<1000 řádků) — přímé čtení + copy s atribucí je rychlejší
- Projekt s permissivní license (MIT/Apache/BSD) — clean-room zbytečný
- Closed-source s reverse engineering — jiné právní constraints (DMCA etc.)

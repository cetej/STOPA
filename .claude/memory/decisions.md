# Shared Memory — Decision Log

Decisions made during task execution. Each entry captures WHAT was decided, WHY, and by WHOM.

### 2026-03-26 — AutoDream vs STOPA memory: KOEXISTENCE
- **Context**: CC v2.1.81+ má nativní AutoDream (`/dream`) — background konsolidace memory souborů (deduplikace, staleness check, index rewrite). Překrývá se s STOPA `/scribe` + memory systémem.
- **Decision**: KOEXISTENCE — AutoDream jako "janitor" (čištění, deduplikace), STOPA `/scribe` jako "architekt" (strukturované zápisy, YAML frontmatter, grep-first retrieval, archivace)
- **Why**:
  - AutoDream nemá YAML frontmatter → nemůže nahradit grep-first retrieval
  - AutoDream maže stale záznamy místo archivace → ztráta historie
  - AutoDream dělá nepravdivé sumarizace (issue #38493) → nespolehlivý pro rozhodovací záznamy
  - AutoDream je black box (žádný log změn) → STOPA transparentnější
  - Index formát kompatibilní (`- [Title](file.md) — hook`)
- **Ochranná opatření**:
  1. HTML komentář v MEMORY.md instruující dream nemazat learnings/, archive soubory
  2. Monitorovat po dream runech zda STOPA struktura zůstala intact
  3. Pokud dream rozbíjí formát → `"autoDreamEnabled": false` v settings.json
  4. Future: FileChanged hook na `.claude/memory/` pro validaci YAML frontmatter
- **Sledovat**: PR #39299 (manuální `/dream` command) — až merged, otestovat chování
- **Decided by**: user (schválil doporučení)

### 2026-03-24 — Server pro 24/7 agent infrastrukturu (PENDING)
- **Context**: Jarvis Phase 5 kompletní mimo 5.1 (24/7 daemon) a 5.5 (voice). Obojí vyžaduje always-on server.
- **Decision**: PENDING — uživatel plánuje pronajmout server, nutno probrat požadavky
- **Požadavky na infrastrukturu**:
  - **Claude Code CLI** běžící persistentně (ne jen desktop app)
  - **Scheduled tasks**: 6 úloh (morning-watch, daily-rebalancer, weekly-digest, memory-maintenance, skill-evolution, preference-learner) — potřebují běžet i když je desktop vypnutý
  - **Telegram plugin**: Bun runtime + persistentní polling pro příjem zpráv 24/7
  - **Git přístup**: SSH klíče ke všem 8 projektům (cetej/*)
  - **Node.js/Bun**: pro Telegram plugin a MCP servery
  - **Python 3.11+**: pro hook skripty (ruff, dippy, skill-suggest)
  - **Paměť**: sdílená ~/.claude/memory/ — buď sync nebo NFS mount z desktopu
  - **OS**: Linux preferovaný (levnější, stabilnější pro daemon), Windows možný
  - **Anthropic API klíč**: pro Claude Code CLI (ANTHROPIC_API_KEY nebo Max plan token)
- **Otevřené otázky**:
  - VPS vs dedicated? (VPS stačí — low CPU, hlavně API calls)
  - Jak synchronizovat memory mezi desktop a server? (git push/pull? rsync? shared storage?)
  - Budget: kolik API tokenů denně generují scheduled tasks? (~$1-3/den odhad)
  - Fallback: co když server spadne? Desktop jako backup?
- **Možnosti**:
  - (A) Levný VPS (Hetzner/DigitalOcean, ~€5-10/měsíc) + Claude Code CLI + cron
  - (B) Anthropic hosted scheduled tasks (pokud bude GA — zatím preview)
  - (C) Raspberry Pi doma (nulové měsíční náklady, ale údržba)
- **Decided by**: user (rozhodnutí pending)

### 2026-03-24 — Voting Pattern: Known Gap, Future Option
- **Context**: Analýza 7 Anthropic agent patterns vs. STOPA odhalila chybějící "voting" subtype parallelization — N nezávislých agentů na stejný task, konsensus výsledků
- **Options considered**: (A) Implementovat hned jako `/critic --voting`, (B) Zapsat jako future option
- **Decision**: Option B — zatím neimplementovat, zapsat jako nápad do budoucna
- **Rationale**: +83% cost per review (~$0.10 navíc), ale reálný benefit jen pro high-stakes (PR merge, architektura). Současný `/critic` + `/verify` dvoustupňový model pokrývá většinu use-cases. Dává smysl jako volitelný mód, ne default.
- **Possible implementation**: Flag `--voting` pro `/critic` nebo `/pr-review`, 3× paralelní Sonnet critic + Haiku aggregátor. Paradoxně rychlejší (paralelní) i přes vyšší cost.
- **Decided by**: user

### 2026-03-22 — Skill Audit Findings: Integration Gaps in Utility Skills
- **Context**: skill-audit harness ran across all 15 skills, revealing 4 skills with integration score 2/5
- **Decision**: Utility skills (youtube-transcript, verify) should add "After Completion" sections writing to learnings.md/state.md; scout should add explicit disallowedTools
- **Rationale**: COMPOUND loop only works if all skills record their findings — isolated utility skills break the feedback loop
- **Decided by**: harness/orchestrator

### 2026-03-18 — Add Budget Controller to Orchestration System
- **Context**: Self-assessment revealed no cost controls. System could become a "token black hole" with unbounded agent spawns and critic loops.
- **Options considered**: (A) Simple agent counter, (B) Full budget skill with tiers + circuit breakers + history, (C) External hook-based monitoring
- **Decision**: Option B — full budget skill with 3 complexity tiers (light/standard/deep)
- **Rationale**: Most practical. Tiers give proportional control without over-engineering.
- **Decided by**: orchestrator + user

### 2026-03-18 — Soften "Never Do Work Yourself" Rule
- **Context**: Original orchestrator rule "never do the work yourself" forced delegation even for trivial edits, wasting tokens.
- **Decision**: Light tier allows direct work, standard/deep still delegate
- **Rationale**: Proportional approach. A single-line fix shouldn't spawn an agent.
- **Decided by**: orchestrator (self-assessment)

### 2026-03-18 — Remove Bash and Agent from skill-generator
- **Context**: skill-generator had Bash and Agent in allowed-tools but doesn't need them.
- **Decision**: Restricted to Read, Write, Edit, Glob, Grep
- **Rationale**: Least-privilege principle.
- **Decided by**: orchestrator (self-assessment)

### 2026-03-24 — /fix-issue workflow: Direct main commits (solo project)
- **Context**: /fix-issue skill vytváří feature branch → merge → push, ale uživatel je sólo vývojář bez need na PR review
- **Decision**: Commitovat přímo na main (bez feature branch, bez PR workflow)
- **Rationale**: Zjednodušuje workflow — 3 kroky (commit + push) místo 5+ (branch + push + merge + push + delete). PR workflow není potřeba bez code review.
- **Decided by**: user

### 2026-03-18 — STOPA as Source of Truth
- **Context**: Orchestrační systém se vyvíjel v test1, kopíroval do ng-robot a ADOBE-AUTOMAT. Vznikal chaos.
- **Decision**: Vytvořit STOPA jako samostatný meta-projekt — source of truth pro orchestraci
- **Rationale**: Jeden zdroj pravdy, distribuce přes sync skript
- **Decided by**: user

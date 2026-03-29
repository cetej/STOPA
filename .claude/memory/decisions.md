# Shared Memory — Decision Log

Decisions made during task execution. Each entry captures WHAT was decided, WHY, and by WHOM.

### 2026-03-29 — bird CLI pro Twitter: OPTION, NEIMPLEMENTOVAT ZATÍM
- **Context**: Agent-Reach používá `@steipete/bird` (npm) pro čtení Twitteru přes cookies bez API poplatků. Balíček je deprecated, kommunikuje přes neoficiální GraphQL API.
- **Decision**: Neuložit jako závislost. Zmapovat jako možnost pro budoucí Twitter kanál v ZÁCHVĚV/MONITOR.
- **Why**: Deprecated stav + riziko banu accountu. Použití jen na dedikovaném alt-accountu. Jako produkční vrstva nevhodné.
- **Possible implementation**: `bird read URL` / `bird search "keyword"` — wrappovat jako /twitter-fetch skill nebo ZÁCHVĚV data source. Prerekvizita: ověřit, že balíček stále funguje (Twitter mění GraphQL endpointy).
- **Decided by**: user

### 2026-03-28 — Workflow Optimization Roadmap (IBM paper-inspired): PHASE 1 IMPLEMENTED
- **Context**: IBM survey "From Static Templates to Dynamic Runtime Graphs" (arXiv:2603.22386) mapuje static→dynamic spektrum pro LLM agent workflows. Identifikovány 3 mezery v STOPA orchestrate.
- **Decision**: 3-fázový roadmap, Phase 1 implementována ihned:
  1. **Phase 1: Enriched Trace Capture** (DONE) — rozšířená budget history o Type, Files, Critic Score, Agent Graph. Orchestrate Phase 6 teď zapisuje strukturované traces.
  2. **Phase 2: Tier Selection Heuristics** (TRIGGER: 20+ traces) — analyzovat traces, extrahovat vzory (např. "bug_fix <5 files = vždy light tier"). Implementovat jako lookup tabulku v orchestrate Phase 1.
  3. **Phase 3: Verifier-Guided Restructuring** (TRIGGER: první reálný critic FAIL loop) — místo circuit breaker STOP, zkusit alternativní workflow strukturu. Prerekvizita: `--adversarial` mód pro critic (viz rozhodnutí výše).
- **Why**: Paper potvrzuje, že principled middle ground mezi static templates a dynamic graphs existuje. STOPA je na statickém konci — traces jsou datový základ pro posun. Ale bez dat je premature optimalizovat.
- **Milestone reminders**: Orchestrate Phase 6 Step 7 automaticky připomene po 20+ traces. Scheduled task kontroluje weekly.
- **Decided by**: user

### 2026-03-28 — Structured dissent (devil's advocate agent): APPROVED, LOW PRIORITY
- **Context**: Paper "Agentic AI and the Next Intelligence Explosion" (arXiv:2603.20639) popisuje "strukturovaný nesouhlas" jako first-class feature multi-agentních systémů. Inspirace pro rozšíření /critic.
- **Decision**: Odložit implementaci dokud nebude reálný use case kde /critic (9.5/10) selže kvůli confirmation bias. Pak implementovat jako `--adversarial` mód.
- **Why**: Critic funguje dobře. Přidávat devil's advocate bez evidence potřeby = premature abstraction. Paper je teoretický (žádné experimenty).
- **Possible implementation**: Flag `--adversarial` pro `/critic` — druhý agent aktivně hledá důvody proč řešení nefunguje (opak běžného review).
- **Decided by**: user

### 2026-03-28 — Precedentní systém v decisions.md: IMPLEMENTED
- **Context**: Stejný paper naznačuje nutnost precedentního systému — minulá rozhodnutí informují budoucí.
- **Decision**: Přidat grep decisions.md do orchestrate Phase 3 (Episodic Recall). Minimální změna, decisions.md už existuje.
- **Why**: Orchestrator už grepuje learnings pro past approaches, ale decisions.md ignoruje. Přitom decisions obsahují přesně ty precedenty které paper zmiňuje.
- **Decided by**: user

### 2026-03-27 — Cloud Auto-Fix integration: 3-layer approach
- **Context**: CC Web nově nabízí auto-fix PRs (sleduje CI failures + review comments, pushuje fixy autonomně v cloudu). Také scheduled tasks (rekurentní cloud prompty) a `--remote` flag pro spuštění cloud session z terminálu.
- **Decision**: 3-vrstvá implementace:
  1. **`/autofix` skill** (DONE) — thin wrapper, diagnostikuje PR stav, spustí cloud auto-fix nebo fixne lokálně
  2. **`/fix-issue` rozšíření** (DONE) — Phase 7: push+PR+autofix tail jako volba po commitu
  3. **Scheduled cloud tasks** (PLANNED) — daily PR triage, weekly dep audit, hourly CI monitoring
- **Prerequisite**: Nainstalovat Claude GitHub App na cetej/STOPA, cetej/NG-ROBOT
- **Why**: Eliminuje manuální cyklus push→CI fail→fix→push. Cloud sessions běží i bez zapnutého PC. Komplementární s existujícím `/critic` (lokální kvalita) a `/verify` (E2E proof).

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

### 2026-03-24 — Server pro 24/7 agent infrastrukturu (PENDING — updated 2026-03-26)
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
  - ~~Jak synchronizovat memory mezi desktop a server?~~ → ANSWERED: SyncThing ($0/měsíc, P2P sync)
  - Budget: kolik API tokenů denně generují scheduled tasks? (~$1-3/den odhad)
  - Fallback: co když server spadne? Desktop jako backup?
- **Možnosti**:
  - (A) Levný VPS (Hetzner/DigitalOcean, ~€5-10/měsíc) + Claude Code CLI + cron
  - (B) Anthropic hosted scheduled tasks (pokud bude GA — zatím preview)
  - (C) Raspberry Pi doma (nulové měsíční náklady, ale údržba)
  - (D) **Mac Mini setup** (viral pattern, 2026-03-26) — viz níže
- **Update 2026-03-26 — Channels 24/7 Architecture (viral Mac Mini pattern)**:
  - Zdroj: Instagram reel + podrobný článek o nahrazení OpenClaw Claude Channels
  - **CRITICAL: Channels nemá message queue** — pokud session neběží, zprávy se nenávratně ztratí
  - **SyncThing** ($0/měsíc) pro sync dev laptop ↔ server: P2P, žádný cloud, od 2013
  - **Co syncovat**: `~/.claude/skills/`, `~/.claude/commands/`, `settings.json`, knowledge base, MCP configs
  - **Co NE-syncovat (.stignore)**: `settings.local.json`, `history.jsonl`, `projects/` (path-dependent), `node_modules`, `.git`, `.env`
  - **Path trick**: stejný username na obou strojích — Claude trackuje projekty dle absolutní cesty
  - **LaunchAgent > cron**: cron nemá přístup k user session credentials → Claude Code auth selže
  - **Crash recovery**: LaunchAgent + restart script (tmux session), daily restart v 4:00 AM
  - **Naše situace**: My jsme Windows → LaunchAgent nepoužitelný, ale principy platí:
    - SyncThing funguje cross-platform (Windows ↔ Linux VPS)
    - Ekvivalent LaunchAgent na Linuxu = systemd user service
    - Na Windows = Task Scheduler nebo NSSM (Non-Sucking Service Manager)
    - Message queue absence platí univerzálně → session MUSÍ běžet 24/7
- **Decided by**: user (rozhodnutí pending)

### 2026-03-24 — Voting Pattern: Known Gap, Future Option
- **Context**: Analýza 7 Anthropic agent patterns vs. STOPA odhalila chybějící "voting" subtype parallelization — N nezávislých agentů na stejný task, konsensus výsledků
- **Options considered**: (A) Implementovat hned jako `/critic --voting`, (B) Zapsat jako future option
- **Decision**: Option B — zatím neimplementovat, zapsat jako nápad do budoucna
- **Rationale**: +83% cost per review (~$0.10 navíc), ale reálný benefit jen pro high-stakes (PR merge, architektura). Současný `/critic` + `/verify` dvoustupňový model pokrývá většinu use-cases. Dává smysl jako volitelný mód, ne default.
- **Possible implementation**: Flag `--voting` pro `/critic` nebo `/pr-review`, 3× paralelní Sonnet critic + Haiku aggregátor. Paradoxně rychlejší (paralelní) i přes vyšší cost.
- **Decided by**: user

### 2026-03-24 — /fix-issue workflow: Direct main commits (solo project)
- **Context**: /fix-issue skill vytváří feature branch → merge → push, ale uživatel je sólo vývojář bez need na PR review
- **Decision**: Commitovat přímo na main (bez feature branch, bez PR workflow)
- **Rationale**: Zjednodušuje workflow — 3 kroky (commit + push) místo 5+ (branch + push + merge + push + delete). PR workflow není potřeba bez code review.
- **Decided by**: user

### 2026-03-29 — AI Papers W13 Research Brief: 3 Medium-Term Opportunities
- **Context**: Análýza top 10 AI papersů týdne (23-29/3, Hyperagents, BIGMAS, Claudini, MemCollab, IBM workflow survey, atd.) pro relevanci k STOPA/NGM stack
- **Decision**: Uložit brief do `docs/ai-papers-2026-W13.md` + zaznamenat 3 Medium-term learnings do learnings/
  1. **Claudini** (autoresearch loop) → learning: white-box domains + existing baselines = success formula
  2. **BIGMAS** (directed graph orchestration) → learning: task complexity → dynamic graph structure (3-9 nodes)
  3. **MemCollab** (agent-agnostic memory) → learning: contrastive trajectory distillation for cross-tier memory sharing
- **Rationale**:
  - Papers validují existující STOPA ideas (multi-agent orchestration, shared memory, dynamic workflows)
  - Claudini + MemCollab jsou HIGH relevance, BIGMAS je MEDIUM (already have linear sequential orchestration, but flexible for future)
  - IBM workflow survey (já vlastní reference: `reference_ibm_workflow_optimization.md`) potvrzuje Phase 1 approach (trace enrichment)
- **Next steps** (low priority):
  - Phase 2: analyzovat 20+ orchestrate traces, extrahovat heuristiky pro tier selection (viz. IBM Phase 2 decision výše)
  - Phase 3: BIGMAS pattern zkusit na complex multi-file refactor (future feedback loop design)
  - Contrastive memory: pilotní projekt během Phase 2 / Phase 3 (když budeme mít multi-agent traces)
- **Decided by**: user (prostřednictvím CLI `/scribe`)

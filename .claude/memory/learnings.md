# Shared Memory — Learnings

Accumulated knowledge from all tasks. Used by all skills/agents to improve over time.

## Patterns

### Budget-First Orchestration
- **Context**: When orchestrating any multi-step task
- **Pattern**: Assign complexity tier BEFORE scouting. Start with lowest viable tier. Upgrade only if scout reveals higher complexity.
- **Source**: Self-assessment, 2026-03-18

### Proportional Critic Usage
- **Context**: When deciding how many review rounds to run
- **Pattern**: Light tier = once at end. Standard = after key subtasks. Deep = after each subtask.
- **Source**: Self-assessment, 2026-03-18

### Tool Least Privilege
- **Context**: When creating or reviewing skills
- **Pattern**: Only grant tools the skill actually needs. Bash and Agent are expensive — remove if not essential.
- **Source**: Self-assessment, 2026-03-18

### Cost Estimation for User Decisions
- **Context**: When proposing options with different cost profiles
- **Pattern**: Always estimate cost in tokens AND real currency (USD + CZK). Users can't judge "50k tokens" but understand "$0.15/week".
- **Source**: /watch creation, 2026-03-18

## Anti-patterns

### Verifying New Features — Timing Matters
- **Problem**: Sub-agent researching `source: "settings"` (v2.1.80) concluded it doesn't exist because it tested BEFORE the version shipped. Follow-up /watch (2026-03-21) confirmed the feature IS real.
- **Instead**: When agent research contradicts official changelog, trust the changelog. Check CHANGELOG.md directly. Agent trial-and-error can fail due to version timing.
- **Note**: Both `github` source (our impl) and `source: 'settings'` work. No migration needed.
- **Source**: /watch scans, 2026-03-20 → 2026-03-21

### Mandatory Full Orchestration
- **Problem**: Over-orchestration wastes tokens. A trivial edit doesn't need scout→plan→execute→critic→scribe.
- **Instead**: Assign light tier and do simple things directly.

### Infinite Critic Loop
- **Problem**: Without a limit, critic→fix→critic→fix can loop indefinitely.
- **Instead**: Max 2 FAIL verdicts on same target, then circuit breaker → escalate to user.

### Unbounded Agent Spawning
- **Problem**: Each agent has its own context window = significant token cost. Without limits, costs explode.
- **Instead**: Tier-based limits. Light=0-1, Standard=2-4, Deep=5-8.

## Cross-Repo Setup

### User's Environment
- **Projekty**: NG-ROBOT (desktop, hlavní), test1 (web, Pyramid Flow), ADOBE-AUTOMAT (desktop, Adobe automatizace), STOPA (meta-projekt, source of truth pro orchestraci)
- **Distribuce**: Plugin v1.5.0 přes GitHub marketplace (settings.json v cílových projektech). Legacy sync skript stále existuje ale preferuj plugin.
- **CLAUDE.md**: Každý projekt má vlastní, nesyncuje se
- **Skills**: 17 skills, 1 harness (skill-audit), 3 rules
- **Source**: Sessions 2026-03-18, updated 2026-03-23

### Karpathy Loop Pattern (AutoLoop)
- **Context**: When iteratively improving any file with measurable quality
- **Pattern**: Structural heuristic for fast iteration (grep-based, zero LLM cost) + single LLM-as-judge validation at end. One file, one metric, git rollback per iteration.
- **Key insight**: M5 hybrid metric scores 22/25 on evaluation criteria. Pure LLM-as-judge (M1) is too expensive per iteration. Pure structural (M2) misses semantic quality. Hybrid combines best of both.
- **Anti-pattern**: Don't use LLM to evaluate LLM output every iteration — self-reinforcing bias + cost explosion
- **Source**: Karpathy AutoResearch analysis, 2026-03-19

### Harness Engineering — Deterministic Rails for LLM Workflows
- **Context**: Komplexní multi-step procesy (pipeline, audit, review) kde skills samy nestačí
- **Pattern**: Fixní fáze (Python/logika řídí pořadí) + programatická validace po každém kroku + šablonový výstup + mezivýsledky na disk. LLM pracuje uvnitř fází, ale nemůže přeskočit/změnit pořadí.
- **Key insight**: Skills = best effort (90%). Harness = deterministic (99.9%). Stripe s harness kolem CC merguje 1300 PR/týden.
- **Anti-pattern**: Pokoušet se dosáhnout 100% spolehlivosti tweakováním promptu. Po ~95% to nejde — potřebuješ hook/harness.
- **Source**: Video analýza "Harness Engineering" + "Claude Certified Architect", 2026-03-22
- **Detail**: Viz `docs/HARNESS_STRATEGY.md`

### Prompts vs Hooks — Suggestion vs Law
- **Context**: Rozhodování jak vynutit chování agenta
- **Pattern**: Prompt = suggestion (styl, tón, formát). Hook = law (finance, bezpečnost, compliance). Pokud selhání = reálný problém → hook, ne prompt.
- **Source**: Video "Claude Certified Architect", 2026-03-22

### Tool Descriptions — Nejvyšší páka pro správný routing
- **Context**: Agent volí špatný tool z nabídky
- **Pattern**: V popisu toolu uvést KDY použít A KDY NEpoužít. Max 4-5 tools na agenta. `tool_choice: forced` pro první krok.
- **Source**: Video "Claude Certified Architect", 2026-03-22

### Path-Specific Rules (.claude/rules/)
- **Context**: CLAUDE.md se načítá celý vždy = plýtvání tokeny
- **Pattern**: `.claude/rules/*.md` s glob patternem v hlavičce — pravidla se loadují jen pro relevantní soubory
- **Status**: DONE — 3 rules vytvořeny (python-files, skill-files, memory-files)
- **Source**: Video "Claude Certified Architect", 2026-03-22. Implemented 2026-03-22.

## Skill Gaps

### Plugin Distribution — DONE
- **Situation**: Plugin system je GA. Distribuce přes marketplace v settings.json.
- **Řešení**: `marketplace.json` v STOPA repo + `github` source v cílových projektech settings.json
- **Metody**: 1) marketplace přes settings.json (doporučeno), 2) `/plugin install`, 3) `--plugin-dir` (dev)
- **Priority**: DONE (2026-03-20)
- **Source**: /watch scan, 2026-03-18 → implementace 2026-03-20

### Agent Teams Native API
- **Situation**: Agent Teams jsou GA — native coordination přes SendMessage, shared task list
- **Potřeba**: /orchestrate deep tier by měl použít native Agent Teams místo manuálních Agent() volání
- **Priority**: medium — DONE (implemented + tested 2026-03-19)
- **Source**: /watch scan, 2026-03-18

### Agent Teams — Live Test Findings (2026-03-19)
- **Windows in-process mode works**: `backendType: "in-process"` confirmed functional on Windows 11
- **Explore agents can't shutdown gracefully**: Explore subagent_type lacks SendMessage tool → can't respond to shutdown_request → TeamDelete fails. Workaround: manual cleanup of `~/.claude/teams/` directory.
- **Spawn prompt vs SendMessage**: Teammates start working from spawn prompt immediately. Sending another "start" message via SendMessage causes duplicate work. Best practice: put full instructions in spawn prompt, use SendMessage only for follow-up coordination.
- **Recommendation**: For audit/research tasks, use `subagent_type: "general-purpose"` instead of Explore, so teammates can respond to shutdown and use SendMessage.
- **Fix applied (2026-03-19)**: All Explore references in orchestrate + scout skills replaced with general-purpose. Warning notes added.
- **Source**: Live test — skill-audit team with 2 Sonnet teammates

### GSD Patterns Adopted (2026-03-23)
- **Wave execution**: Topologický sort subtasků podle závislostí → wave číslo → paralelní exekuce per wave. Preferovat vertical slices (celý feature per subtask) nad horizontal layers (all models, then all APIs) — maximalizuje Wave 1 paralelismus.
- **Deviation rules**: Sub-agenti mají pre-granted autoritu fixovat bugy inline (max 3 pokusy), ale STOP při architektonické změně. Pre-existing bugy jen logovat, nefixovat.
- **Analysis-paralysis guard**: 5+ po sobě jdoucích read-only operací bez Write/Edit = agent je stuck → musí jednat nebo reportovat blocked.
- **Goal-backward verification**: 4 úrovně ověření: L1 Exists → L2 Substantive (ne stub) → L3 Wired (importován) → L4 Flows (reálná data). Stub detection: `return []`, `return null`, `preventDefault()` only, state never rendered.
- **Assumptions pre-flight**: Před plánováním přečíst 5-15 souborů, formulovat předpoklady s confidence level (Confident/Likely/Unclear), nechat uživatele opravit → locked constraints pro plánování. Implementováno jako `--assumptions` flag ve `/scout`.
- **Context monitor**: Vyhodnoceno jako redundantní — STOPA už má PostCompact hook + orchestrate context health scoring. GSD řeší dual-bridge přes temp soubory, což je over-engineered pro náš setup.
- **Co NEadoptovat z GSD**: XML task format (YAML stačí), celý lifecycle workflow (STOPA je modulární toolbox), artefaktová soustava PROJECT/ROADMAP/REQUIREMENTS (duplikuje memory systém), requirements traceability IDs (over-engineering pro current scope).
- **Source**: Analýza gsd-build/get-shit-done v1.28

### fal.ai API Integration (2026-03-23)
- **Python path**: On this Windows system, use `python` (C:\Python313) not `python3` (WindowsApps stub) — fal-client is installed only under C:\Python313
- **fal_client.subscribe()**: Blocking call, works for images (fast). For video (1-3 min), use `fal_client.submit()` + `iter_events()` for progress tracking
- **fal_client.upload_file()**: Uploads local file and returns URL — needed for image-to-video with local images
- **URL expiry**: fal.ai result URLs expire in ~1 hour — download immediately after generation
- **FAL_KEY**: Stored in `~/.claude/settings.json` env section (user-level, not committed to git)
- **Pricing**: Nano Banana Pro ~$0.15/image (1K), Kling v3 standard ~$0.084/s, pro ~$0.112/s
- **Source**: End-to-end test of /nano-banana and /kling skills

### Awesome Claude Code Ecosystem Scan (2026-03-23)
- **Scanned**: 30+ repos, 100+ projects z awesome-claude-code (hesreallyhim/awesome-claude-code)
- **Top competitors**: Claude Code Flow (23k★, vector memory + consensus), Claude Task Master (26k★, PRD parsing), superpowers (107k★, auto-triggered skills), wshobson/agents (32k★, 72 plugins + progressive disclosure)
- **STOPA unikáty**: Goal-backward verification (L1-L4), deviation rules, budget tiers s approval gates, harness engine — žádný competitor tohle nemá
- **Architektonický insight**: Konkurence = task scheduling + paralelismus. STOPA = goal-backward reasoning + verification gates. Posilovat tuto filozofii.
- **Adoptovat**: Hooks (PostToolUse lint, PermissionRequest auto-approve, PreCompact checkpoint), structured exit token v autoloop, /fix-issue skill, /pr-review (6-persona), /brainstorm (Socratic), change-detection circuit breaker, hierarchická context injection, status line (ccstatusline)
- **NEadoptovat**: Vector memory (overkill pro naši škálu), multi-model routing (jsme Claude-native), Byzantine consensus (over-engineering), Docker sandboxing (TSK), mobile control (Happy Coder)
- **Detail**: Viz `research/awesome-claude-code-scan.md`
- **Source**: Paralelní scan 4 agentů přes celý awesome-claude-code repo

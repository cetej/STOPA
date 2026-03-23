# Shared Memory — Learnings

Accumulated knowledge from all tasks. Used by all skills/agents to improve over time.

## Patterns

### Spec-Kit Adoption (2026-03-23)
- **Context**: Competitive analysis github/spec-kit (81k★, 7 months). Spec-Driven Development toolkit od GitHubu.
- **Pattern**: 3 adoptované patterns: (1) Constitution check — project governance doc jako non-negotiable autorita v /orchestrate a /brainstorm, (2) Handoff metadata — `handoffs:` field ve skill frontmatter definuje workflow graph (brainstorm→orchestrate→critic→verify), (3) Requirements-level checklist — "Are requirements defined for X?" místo "Verify X works" + traceability tagy [Spec §X], [Gap], [Ambiguity] v /critic --spec.
- **Key insight**: Hard question limits (max 3 open markers) force action over analysis paralysis — adopted in /brainstorm.
- **Not adopted**: Multi-agent format rendering (27 agents — zbytečná komplexita), extension marketplace (premature), preset system (plugin covers this).
- **Strategic**: Spec-kit je document-generation tool, STOPA je execution system. Komplementární, ne konkurenční. Threat level LOW.
- **Source**: github/spec-kit v0.4.0, analysis v competitive-spec-kit.md

### Superpowers Adoption (2026-03-23)
- **Context**: Analýza obra/superpowers (v5.0.5) pro adopci patterns do STOPA
- **Pattern**: 5 adoptovaných patterns: two-stage review, agent status codes, anti-rationalization tables, trigger-only descriptions, 3-fix escalation. Klíčový insight: skill description summary → Claude shortcuts místo čtení full body (testováním prokázáno). DONE_WITH_CONCERNS status je nejhodnotnější — předchází silent shipping.
- **Source**: obra/superpowers, commit da13ce7

### Budget-First Orchestration
- **Pattern**: Assign complexity tier BEFORE scouting. Start with lowest viable tier. Upgrade only if scout reveals higher complexity.
- **Anti-pattern**: Over-orchestration wastes tokens. Trivial edit doesn't need scout→plan→execute→critic→scribe. Use light tier directly.

### Critic & Agent Limits
- **Pattern**: Critic: Light=1× na konci, Standard=2×, Deep=3×. Max 2 FAIL verdicts → circuit breaker → escalate.
- **Pattern**: Agent spawning: Light=0-1, Standard=2-4, Deep=5-8. Tool least privilege — only grant tools skill actually needs.

### Cost Estimation for User Decisions
- **Pattern**: Always estimate cost in tokens AND real currency (USD + CZK). Users can't judge "50k tokens" but understand "$0.15/week".
- **Source**: /watch creation, 2026-03-18

### Karpathy Loop Pattern (AutoLoop)
- **Pattern**: Structural heuristic for fast iteration (grep-based, zero LLM cost) + single LLM-as-judge validation at end. One file, one metric, git rollback per iteration.
- **Key insight**: M5 hybrid metric scores 22/25. Pure LLM-as-judge too expensive per iteration. Pure structural misses semantic quality.
- **Anti-pattern**: Don't use LLM to evaluate LLM output every iteration — self-reinforcing bias + cost explosion.

### Harness Engineering
- **Pattern**: Fixní fáze (Python řídí pořadí) + programatická validace po každém kroku + šablonový výstup. LLM pracuje uvnitř fází, nemůže přeskočit/změnit pořadí.
- **Key insight**: Skills = best effort (90%). Harness = deterministic (99.9%). Prompt tweaking caps at ~95%.
- **Detail**: Viz `docs/HARNESS_STRATEGY.md`

### Prompts vs Hooks — Suggestion vs Law
- **Pattern**: Prompt = suggestion (styl, tón, formát). Hook = law (finance, bezpečnost, compliance). Pokud selhání = reálný problém → hook, ne prompt.

### Tool Descriptions — Routing
- **Pattern**: V popisu toolu uvést KDY použít A KDY NEpoužít. Max 4-5 tools na agenta. `tool_choice: forced` pro první krok.

## GSD Patterns (2026-03-23)
- **Wave execution**: Topologický sort subtasků → wave číslo → paralelní exekuce. Preferovat vertical slices nad horizontal layers.
- **Deviation rules**: Sub-agenti fixují bugy inline (max 3 pokusy), STOP při architektonické změně. Pre-existing bugy jen logovat.
- **Analysis-paralysis guard**: 5+ read-only operací bez Write/Edit = agent stuck → musí jednat nebo reportovat blocked.
- **Goal-backward verification**: L1 Exists → L2 Substantive → L3 Wired → L4 Flows. Stub detection: `return []`, `return null`, state never rendered.
- **NEadoptovat z GSD**: XML task format, lifecycle workflow, artefaktová soustava, requirements traceability IDs.

## Environment

### User's Environment (2026-03-23)
- **Projekty**: NG-ROBOT (desktop, hlavní), test1 (web), ADOBE-AUTOMAT (Adobe), STOPA (meta-projekt)
- **Distribuce**: Plugin v1.7.0 přes GitHub marketplace. Legacy sync skript existuje ale preferuj plugin.
- **Skills**: 23 skills, 12 hooks, 4 rules

### fal.ai API (2026-03-23)
- **Python**: Use `python` (C:\Python313) not `python3` (WindowsApps stub)
- **fal_client.subscribe()**: Blocking, OK for images. Video: use `submit()` + `iter_events()`
- **URL expiry**: fal.ai result URLs expire ~1 hour — download immediately
- **FAL_KEY**: In `~/.claude/settings.json` env section (user-level)
- **Pricing**: Nano Banana Pro ~$0.15/image, Kling v3 standard ~$0.084/s, pro ~$0.112/s

### Ecosystem Scan (2026-03-23)
- **Top competitors**: Claude Code Flow (23k★), Claude Task Master (26k★), superpowers (107k★), wshobson/agents (32k★)
- **STOPA unikáty**: Goal-backward verification (L1-L4), deviation rules, budget tiers, harness engine
- **Filozofie**: Konkurence = task scheduling + paralelismus. STOPA = goal-backward reasoning + verification gates.
- **Detail**: Viz `research/awesome-claude-code-scan.md`

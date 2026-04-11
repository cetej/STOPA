---
date: 2026-04-10
type: architecture
severity: high
component: orchestration
tags: [orchestration, budget, scout, recursion, long-context, RLM]
summary: "RLM (arXiv:2512.24601) validuje STOPA RLM principy a přidává 3 implementované vzory: budget propagation do sub-agentů (soft-cap + 20% reserve), metadata-first scout (--metadata flag), recursion depth guard (max-depth frontmatter, default 1). Klíčový závěr: STOPA neadoptuje REPL — Agent tool je ekvivalent. Depth=1 stačí i v produkčním RLM."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 0.85
verify_check: "Grep('Budget Allocation per Agent', path='.claude/skills/orchestrate/SKILL.md') → 1+ matches"
skill_scope: [orchestrate, scout, deepresearch]
---

## RLM × STOPA — Implementované principy

Paper: Zhang, Kraska, Khattab — Recursive Language Models (arXiv:2512.24601, Dec 2025)
Repo: github.com/alexzhang13/rlm (3.3k stars, `pip install rlms`)
DSPy integrace: `dspy.RLM` (experimental modul)

### Co jsme implementovali (2026-04-10)

1. **Budget propagation** — každý agent dostane `remaining_budget`, soft-cap s graceful degradation, 20% reserve pool, min viable $0.03
2. **Metadata-first scout** — `--metadata` flag vrací strukturované metadata (file count, languages, risk signals, key files) bez čtení souborů. Orchestrátor plánuje z metadat, workers čtou plné soubory.
3. **Recursion depth guard** — `max-depth` frontmatter pole (default 1, max 2). Core-invariant #8. Deepresearch má max-depth: 2.

### Co zbývá (improvement-queue.md)

4. Structured output contracts (JSON schema)
5. Lazy context loading (paths ne content)
6. "Never summarize" rule (compact redesign)
7. Contradiction detection (deepresearch, critic)
8. Strategy pre-enumeration (autoloop Phase 0.5)

### Klíčové rozhodnutí

- STOPA NEADOPTUJE REPL pattern — Claude Code Agent tool poskytuje ekvivalentní delegaci
- Depth=1 stačí i v produkčním RLM (InfoQ: depth>1 nestabilní)
- Two-model arch (root heavy + recursive cheap) = STOPA model selection (Opus plan + Haiku execute)

### Benchmarky (pro kontext)

- GPT-5 + RLM: 91.3% BrowseComp-Plus, 58% OOLONG-Pairs (vs 0.1% base)
- 3× levnější než summarization agenty
- RLM-Qwen3-8B: 1000 SFT samples, +28.3% median

---
date: 2026-04-19
type: architecture
severity: high
component: orchestration
tags: [harness, scaffold, multi-session, feature-list, progress-file, agent-ground-truth]
summary: "Multi-session project harness pattern (Anthropic/OpenAI/SWE-agent): feature-list.json as ground truth, progress.md for continuity, init.sh for reliable startup, docs/ as system-of-record. STOPA adopted via extended /project-init --harness flag + /build-project per-feature loop + passes-rate.py metric. Prevents 'declare victory too early' and context-window-boundary confusion in long-running projects."
source: external_research
maturity: draft
uses: 3
successful_uses: 0
harmful_uses: 0
confidence: 1.0
skill_scope: [project-init, build-project]
verify_check: "Glob('scripts/passes-rate.py') → 1+ matches"
related: [2026-04-07-agents-md-efficiency-validated.md, 2026-04-05-self-improving-harness.md]
---

## Harness Engineering Adoption (Three Sources Converge)

### Sources

1. **Anthropic Claude Code harness** — Two-agent architecture (initializer + coding agent), feature-list.json as rigid ground truth, progress file + git commits for clean multi-session handoffs, startup sequence (pwd → progress → git log → features → init.sh → smoke). Root insight: JSON resists casual editing; Markdown does not.
2. **OpenAI Codex internal** — 1M LOC shipped with 3 engineers, zero human-written code. Docs/ architecture as repo system-of-record beats monolithic AGENTS.md. Mechanical architecture enforcement via custom linters with remediation messages. "Anything agent can't read from repo does not exist."
3. **Princeton SWE-agent (ACI paper)** — +64% relative improvement from interface design alone, same model. Capped search, stateful line-numbered viewer, integrated linter feedback, context compaction beyond last 5 turns.

### Convergent patterns across all three

| Pattern | What it solves |
|---------|----------------|
| Feature-list.json ground truth | Agent can't infer completeness from code; explicit passes:bool removes ambiguity |
| Progress.md + git commits | Context window boundary survival — next session orients without archaeology |
| init.sh + smoke test | Every session begins from known-good state; env setup amortized |
| docs/ as system of record | Progressive disclosure: short map → deep truth, resists rot |
| Integrated feedback (linter/browser) | Catches errors at point of introduction, not 10 steps downstream |
| Mechanical architecture enforcement | Human review doesn't scale to agent throughput |

### STOPA adoption (2026-04-19)

- **Resurrected** `.claude/commands/project-init.md` + `.claude/skills/project-init/SKILL.md` with new `--harness` flag
  - Creates `docs/feature-list.json` (JSON placeholder F001), `docs/progress.md`, `docs/architecture.md`, `init.sh` (executable), extended `AGENTS.md` with Startup Sequence + Feature Completion Gate
- **Resurrected** `.claude/commands/build-project.md` + skill with harness-discipline pipeline:
  - Phase 1: Requirements → feature list draft (human gate)
  - Phase 3: Scaffold MUST use `--harness`
  - Phase 4: Per-feature loop — implement one, verify end-to-end via steps[], set passes:true, commit, update progress.md
- **Created** `scripts/passes-rate.py` — reads `~/.claude/memory/projects.json`, scans each project's `docs/feature-list.json`, reports global + per-project completion rate with stale detection (30d). Supports `--registry` flag for test isolation. Tested on sandbox with 2/4 passes → 50% rate confirmed.

### Why the JSON rigidity matters

Empirical observation (Anthropic): models casually edit Markdown/YAML feature lists but resist modifying JSON. The rigidity is not a limitation — it is the feature. It forces the "I'll just tweak this to mark it done" pattern to be an explicit, conspicuous edit. Do NOT convert feature-list.json to YAML for "readability."

### Why per-feature loop, not parallel batch

Parallel feature implementation corrupts the passes:bool gate — you cannot isolate which commit broke what. Sequential with verification → commit → next is slower per-feature but faster per-project because rework costs collapse.

### Why this is Phase 4 of the feedback loop (not Phase 3 extension)

Phase 3 (actionable_rate: 18.5% → 51.9%) measured STOPA-local ingest quality — `/watch → ingest → learning → applied`. Phase 4 extends the same loop ONE LEVEL OUT: `/watch → ingest → learning → applied in TARGET PROJECT → feature passes`. passes-rate.py is the metric that closes this outer loop. Expect target < 40% initially (harness adoption lag), climbing over quarters.

### Anti-patterns to avoid

- Auto-applying `--harness` to every project (it's opt-in — small utilities don't need it)
- Generating feature-list.json features from project name guess (creates wrong mental model, worse than placeholder)
- Setting passes:true after unit tests alone (must be end-to-end per steps[])
- Starting a new session without running init.sh first (compounds breakage)

### Why: 28.64% runtime reduction already empirically validated for AGENTS.md alone (arXiv:2601.20404). Feature-list.json + progress.md + init.sh stack multiplicatively on top — Anthropic internal experiment: without harness, frontier model failed to build production web app even with compaction; with harness, months of coherent progress.

### How to apply

- When user asks "build X" (new project): invoke `/build-project` — it handles scaffold via `/project-init --harness`
- When user does `/project-init path --harness`: single-session scaffold, leave feature-list population to user/future sessions
- When reviewing project progress: run `python scripts/passes-rate.py` for dashboard
- For weekly /watch news: include passes-rate delta (will auto-wire in next iteration)

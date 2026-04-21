# ADR 0016 Phase C — Council Verdict

**Date:** 2026-04-21
**Decision:** STOPA 90-day strategic response (May–July 2026)
**Input:** `outputs/meta-agent-competitive-landscape.md` (Phase B research brief)
**Council model:** 5 Haiku advisors (Pragmatist / Architect / Skeptic / User Advocate / Futurist) → 3 Sonnet judges (anonymized cross-review) → Chairman synthesis

---

## Verdict per sub-decision

| # | Sub-decision | Recommendation | Confidence |
|---|--------------|----------------|------------|
| 1 | Memory backend (CMM timing) | **B — Build abstraction layer now + CMM adapter in parallel** | HIGH (4/5 advisors) |
| 2 | Retrieval upgrade | **C — Accept grep-only + add measurement instrumentation** (re-evaluate July 2026) | MEDIUM (split 2–2–1) |
| 3 | Public benchmark | **C — Publish minimal findings from existing metrics, NOT STOPA-Bench** | HIGH (4/5 advisors) |
| 4 | Platform threat posture | **B — Monitor quarterly** | HIGHEST (5/5 unanimous) |

---

## Council Leaderboard

| Rank | Advisory | Persona | Avg Position | Top-2 Votes |
|------|----------|---------|-------------|-------------|
| 1 | Advisory 1 | **Pragmatist** | 1.0 | 3/3 |
| 2 | Advisory 3 | **Skeptic** | 2.67 | 2/3 |
| 3 | Advisory 4 | **User Advocate** | 3.0 | 0/3 |
| 4 | Advisory 2 | **Architect** | 3.33 | 1/3 |
| 5 | Advisory 5 | **Futurist** | 5.0 | 0/3 |

**Unanimous judge ranking top**: Pragmatist ranked #1 by all 3 judges — for "most empirically grounded, concrete thresholds, falsifiable triggers."

---

## Consensus Points (high confidence)

1. **Abstraction layer + CMM adapter is correct** — 4 of 5 advisors converge explicitly, 5th converges with a "minimal validation layer." Motivation varies (insurance vs. stress-test vs. option value), action identical. Commit now, ~200-line `MemoryBackend` ABC, `LocalMemoryAdapter` today + `CMMemoryAdapter` mock for GA.
2. **Platform monitoring is right at quarterly cadence** — all 5 agree. Microsoft/Google/Apple enterprise-locked; STOPA niche is personal dev + multi-project coding. Monthly = paranoia, yearly = negligence.
3. **STOPA-Bench is scope creep** — 4 of 5 reject. User Advocate: "users care about 158 → 3 approval prompts, not SOTA."
4. **Publishing minimal findings is net-positive** — 4 of 5 OK with a 3-page report from existing metrics (`actionable_rate.py` data, cross-project routing outcomes), with the Skeptic's caveat addressed below.

---

## Key Tensions (genuine disagreements worth naming)

### Tension 1: Retrieval upgrade timing (2 vs. 2 split, Futurist abstains)

**Add vectors now (Architect + Skeptic):** semantic gap is real, "validation" vs "input sanitization" map to the same learning, synonym fallback is duct tape, growth rate (~20 learnings/week) hits 500 in ~3–4 months.

**Wait for CMM / grep suffices (Pragmatist + User Advocate):** grep+BM25+RRF works under 200 ms at 190 learnings, mem0's 1.44 s p95 benchmark is from 10K+ doc scale, migration cost (~$200 hosting + 2 days + reindex-on-write operational debt) has zero benefit at current scale. Mitigation: monthly perf audit, escalate at 300 ms p95.

**Resolution (Chairman):** **C with instrumentation.** Add logging to `hybrid-retrieve.py`: per-query miss rate (no relevant learning returned) and p95 latency. Re-evaluate in 90 days. If miss rate > 8 % **or** p95 > 300 ms → upgrade to vectors (Qdrant local, not LanceDB — Windows/antivirus concerns, User Advocate noted). If below thresholds → stay grep.

This resolves Architect/Skeptic concern (we measure, we don't assume) **and** Pragmatist concern (don't over-engineer before evidence).

### Tension 2: Benchmark corruption (Skeptic minority view)

Skeptic's **AlphaGo-ification** warning is unique and correct in principle: if STOPA publishes a benchmark, every new skill gets optimized for the benchmark rather than real work. "Walk away 6 hours, return to 8 completed subtasks" is the real value — no constrained task suite captures that.

**Resolution:** publish minimal findings but **specifically on autonomy-hours metrics** (session length without human intervention, consecutive completed subtasks, approval-prompt reduction over time), not on SWE-bench-style success rates. This sidesteps the AlphaGo trap while giving the outside world (and April 2027 us) a real baseline.

### Tension 3: STOPA as tool vs. platform (Futurist meta-question)

**Futurist raised the crucial forcing question:** *"If CMM worked perfectly and cost $0, would you abandon STOPA immediately? Or is there something about skill coupling, local-first, Czech heuristics, orchestration patterns you'd miss?"*

This is **the question user should answer before executing any of the above**. The Chairman cannot answer it for the user.

- If answer is **"I'd abandon STOPA"** → Sub-decision 1 flips to (D) adopt beta now, retrieval becomes (B) wait for CMM.
- If answer is **"I'd keep STOPA even if CMM was perfect"** → current recommendations are correct; STOPA is tooling with independent value.

Chairman's reading of user signals (just disabled Telegram, no Jarvis claim, multi-project, Czech, wants autonomy + friction reduction): **probably the second answer**, but user should confirm before we commit resources. If user confirms, proceed as verdict above. If user wants to think about it, parking the answer is fine — doesn't block Sub-decision 4 (monitor) or the abstraction work.

---

## Risk Mitigation (top 3)

1. **CMM delays past Q4 2026 → abstraction layer is sunk cost.** Mitigation: keep abstraction under 200 lines, deletable. Architect and Pragmatist both ceiling-cap this explicitly.
2. **Vector search staleness failure** (if we migrate later): reindex-on-write creates consistency vs. latency trade-off, especially on Windows with antivirus. Mitigation: choose Qdrant local (in-memory option) over LanceDB, pre-commit hook for reindex, and do the migration only with measured evidence.
3. **User's real pain (158 approval prompts) is unaddressed by any architectural decision.** User Advocate flagged this uniquely. **Prerequisite**: `ANTHROPIC_API_KEY` populated in `~/.claude/keys/secrets.env`, `keys-sync.ps1` run, CC restarted. Until then, every other improvement is theatre. **This is the single most important action** and comes before any Phase C execution.

---

## Dissenting View (Skeptic on memory)

The Skeptic alone argued (C) stay custom indefinitely for memory — "CMM is 'we handle retrieval, you don't,' but STOPA's moat IS the retrieval layer." This was overruled because:

- Even the Skeptic acknowledged building "minimal CMM validation layer for optionality" — functionally close to the abstraction recommendation.
- STOPA's moat isn't storage; it's the **semantics above storage** (maturity tiers, confidence, supersedes chains, impact_score, failure replay). Those survive any backend change.
- CMM ecosystem pull (Claude Code native integration, benchmark visibility, community plugins) is too strong to ignore forever.

**Counter-trigger:** if CMM GA ships without skill-scoped namespacing or custom metadata fields, Skeptic's position wins. Monitor closely at release.

---

## Execution plan (90 days)

### Week 1–2 (immediate, highest ROI)
- [ ] **Resolve ANTHROPIC_API_KEY** (user action, then `keys-sync.ps1`) — unlocks L2 sentinel, eliminates 158/day approval prompts. **Everything else waits on this.**
- [ ] Add instrumentation to `hybrid-retrieve.py`: log per-query miss rate + p95 to `.claude/memory/retrieval-metrics.jsonl`. Dashboard in `/status`.

### Week 3–4 (abstraction scaffold)
- [ ] Design `MemoryBackend` ABC (`scripts/memory_backend.py` or `.claude/lib/memory_backend.py`). 4 methods minimum: `list()`, `search(query, k)`, `read(id)`, `write(id, content, metadata)`.
- [ ] Implement `LocalMemoryAdapter` (wraps current grep+BM25+RRF file-based system). Tests: existing skills using memory all pass through the adapter.
- [ ] Implement `CMMemoryAdapter` mock (returns fixed responses). No Anthropic beta header call yet — just the contract shape.

### Week 5–8 (decide-by-data, CMM readiness)
- [ ] Review retrieval metrics. If miss rate > 8 % or p95 > 300 ms → schedule vector upgrade (Qdrant local). Else → stay grep.
- [ ] When Anthropic announces CMM GA dates more concretely (watch `platform.claude.com` changelog + Anthropic blog monthly), swap `CMMemoryAdapter` mock → real implementation in a feature branch. Parallel run.

### Week 9–12 (publish + stabilize)
- [ ] Draft 3-page "STOPA Q2 2026" report focused on **autonomy metrics** (session length, subtasks completed without intervention, approval-prompt reduction over time). Publish as blog post + link from repo README. **Not** arXiv.
- [ ] Quarterly platform monitor: check Microsoft Copilot Studio pricing, Google Gemini feature drops, Apple WWDC 2026 preannouncements. 1 hour, update `decisions.md` with findings.

### Re-evaluation triggers (do not wait 90 days if any of these hit)

- CMM GA announced with specific date → accelerate adapter work.
- Grep retrieval p95 > 500 ms → emergency vector migration.
- Microsoft announces Copilot Studio personal/SMB tier → escalate platform monitor to monthly + reconsider differentiation strategy.
- User answers Futurist's question "yes, I'd abandon STOPA if CMM was perfect" → flip Sub-decision 1 to (D) beta adoption.

---

## What requires user input now

Two questions that the council could not answer:

1. **Futurist's forcing question:** *If CMM worked perfectly and cost $0, would you abandon STOPA immediately, or is there something about skill coupling, local-first, Czech heuristics, orchestration patterns that you'd miss enough to keep building?* This is the platform-vs-tool framing decision.

   **User answered 2026-04-21: "Neopustil."** → STOPA has independent value beyond memory backend. Sub-decision 1 stays (B) abstraction + CMM adapter. Sub-decision 1 does NOT flip to (D) beta adoption. All verdicts above remain in force.

2. **Resourcing question:** who does the abstraction work in weeks 3–4? Is it solo-you, or koder-delegated, or paused because bod 1 (API key + friction) is higher priority?

   **Pending user input.**

---

## Full Advisories (anonymized in judging; de-anonymized here)

See `outputs/.research/council-advisories-anonymized.md` for the raw stage-1 output. Persona mapping:

- Advisory 1 = **Pragmatist** (rank 1, avg 1.0)
- Advisory 2 = **Architect** (rank 4, avg 3.33)
- Advisory 3 = **Skeptic** (rank 2, avg 2.67)
- Advisory 4 = **User Advocate** (rank 3, avg 3.0)
- Advisory 5 = **Futurist** (rank 5, avg 5.0)

All five advisory texts and three judge evaluations are preserved in the research folder for audit.

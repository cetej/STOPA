# Context Lifecycle — Cache, Compaction & Quality

> Compiled 2026-04-27 from 8 learnings (cluster: prompt-cache, context-rot, compaction, checkpoint).
> Article #11 in Knowledge Base. Theme: how context windows are populated, preserved, compressed, and reset across a session — and the cost-quality tradeoffs at each stage.

---

## Why this matters

Every long-context model has the same lifecycle:
1. Cache **warms** as context fills → token cost drops
2. Cache **cools** if idle → next prompt re-pays full cost
3. Quality **degrades** before the window fills (lost-in-the-middle, ~30-40% on 1M context)
4. Compaction either **rescues** or **destroys** depending on timing and direction

Misjudging any stage wastes tokens or burns context fidelity. STOPA's session, compact, checkpoint, and orchestrate skills all touch this lifecycle. This article maps the empirical thresholds.

---

## Stage 1 — Prompt cache: 5-minute TTL

**Anthropic prompt cache lifetime is 5 minutes.** After 5 min idle, next message reprocesses the entire context at full cost.

| Pause | Cost on resume | What to do |
|-------|----------------|------------|
| < 270s | Full cache hit | Just continue |
| 270-300s | Partial / mid-decay | Avoid this band — finish your tool call now or pause longer |
| 5 min – 1 h | Full reprocess | Either accept the miss (one-time) or `/checkpoint` + `/clear` first |
| > 1 h | Full reprocess inevitable | `/checkpoint` is mandatory — losing in-context reasoning anyway |

**Don't pick 5 minutes.** It's the worst-of-both — pay the cache miss without amortizing it. Either drop under 270s (warm) or commit to 1200s+ (one miss, longer wait).

**RTK ScheduleWakeup already encodes this:** `delaySeconds < 270` stays warm; `300+` pays the miss. Same principle applies to human pauses.

Source: [2026-04-14-prompt-cache-ttl-5min.md](../learnings/2026-04-14-prompt-cache-ttl-5min.md)

---

## Stage 2 — Context rot: quality degrades at 30-40%

| Threshold | What happens | Action |
|-----------|--------------|--------|
| 30% (300k/1M) | Onset of quality degradation in tool-heavy sessions | Spawn subagent for any chunk > 100k intermediate output |
| 40% (400k/1M) | Confirmed degradation across task types | Compact or delegate before this point |
| 60% | Manual `/compact` proactive zone | Add direction hint (see Stage 3) |
| 70% | `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70` safety net | Already set in `~/.claude/settings.json` |
| 95% | Default autocompact fires (TOO LATE) | Quality already lost; recovery not full |

**Don't trust relative thresholds alone.** "60% proactive" works for simple sessions. For tool-heavy work (many file reads, agent outputs), target 30-40% — the absolute threshold from Anthropic's session management guide.

**Lost-in-the-middle phenomenon:** The model attends to the start and end of context — middle gets ignored. By the time autocompact triggers at 95%, the model is at its LEAST intelligent precisely when it needs to summarize well.

Sources: [2026-04-18-context-rot-absolute-threshold.md](../learnings/2026-04-18-context-rot-absolute-threshold.md), [2026-04-14-compact-timing-60pct.md](../learnings/2026-04-14-compact-timing-60pct.md), [2026-04-01-autocompact-threshold.md](../learnings/2026-04-01-autocompact-threshold.md)

---

## Stage 3 — Graduated compaction: 5 layers, lightest first

CC implements a 5-layer cascade. Each targets a different pressure type. STOPA's `/compact` historically jumped straight to layer 5; this is wasteful.

| Layer | Name | Trigger | Cost | Reversible |
|-------|------|---------|------|------------|
| 1 | Budget Reduction | Per-message size limit exceeded | None (auto) | Yes (replace with reference) |
| 2 | Snip | First token pressure | Low | Partial (oldest history removed) |
| 3 | Microcompact | Tool result accumulation | Medium | Partial (cache-aware, fine-grained) |
| 4 | Context Collapse | Pre-summarization phase | Medium | Yes (read-time projection, storage intact) |
| 5 | Auto-Compact | Final fallback | High (model-summary) | No (lossy by design) |

**Order matters:** apply lightest layer that resolves the pressure. Skipping to layer 5 when layer 2 would suffice destroys reusable context.

**STOPA gap (open):** `/compact` does not currently check pressure type before invoking layer 5. Pre-check: if context < 70% window, try snip-style (drop oldest tool results > 2K tokens) before triggering full Auto-Compact.

Source: [2026-04-18-cc-graduated-compaction-5layer.md](../learnings/2026-04-18-cc-graduated-compaction-5layer.md) (arXiv:2604.14228)

---

## Stage 4 — Direction-hinted compact: rescue from bad summaries

**Why bad compacts happen even at correct timing:** the model summarizes around the session's *dominant theme*. Off-theme content gets dropped — even if it's important for what comes next. Combined with context-rot at the trigger point, the model is at its worst exactly when it needs to predict what to preserve.

**Fix:** Run `/compact` proactively BEFORE topic transitions, with an explicit direction hint:

```
/compact focus on the auth refactor, drop the test debugging
/compact I'm about to work on bar.ts warnings next
```

This converts compact from "summarize the past" to "preserve for the future." A direction hint at task transitions raises post-compact utility dramatically.

**Compounding rule:** After 3-4 compacts in a row, fidelity loss compounds — switch to `/clear` + session summary + fresh checkpoint resume instead of continuing to compact.

Source: [2026-04-18-bad-compact-direction-unpredictability.md](../learnings/2026-04-18-bad-compact-direction-unpredictability.md)

---

## Stage 5 — Checkpoint as cache: query-gated retrieval

Memory Caching (MC, arXiv:2602.24281) formalizes a universal pattern that STOPA already implements implicitly:

| MC stage | STOPA implementation | Status |
|----------|---------------------|--------|
| Segment long stream | Chunk learnings by component/tag | Implemented (grep-first) |
| Compress at boundary | `checkpoint.md` session summary | Implemented |
| Cache the checkpoint | `learnings/*.md` per-file | Implemented |
| Query-gated retrieval | hybrid-retrieve.py RRF (k=60) | Partial — flat weights, not query-dependent |

**Open optimization:** GRM (Generative Retrieval Memory) gating uses `query × cached-state` similarity — not flat recency or static weights. STOPA's hybrid-retrieve combines grep + BM25 + graph-walk via RRF, but the weights are static. Adding embedding similarity as a fourth retrieval channel would close the gap.

**Complexity contract:** O(NL) memory with smooth control between O(L) RNN-efficiency and O(L²) Transformer-capacity. STOPA's checkpoint→hybrid-retrieve pipeline already sits on this curve.

Source: [2026-04-18-mc-checkpoint-caching-retrieval-pattern.md](../learnings/2026-04-18-mc-checkpoint-caching-retrieval-pattern.md)

---

## Stage 6 — Sub-agent isolation: prevent parent bloat

A sub-agent's full reasoning trace MUST NOT be injected into the parent context. CC's sidechain pattern already does this at the protocol level (each subagent writes a separate `.jsonl`, only final response returns).

**STOPA gap:** worker agents often return raw outputs (full grep results, file diffs) instead of summaries. The protocol isolates, but the prompts don't enforce summarization.

**Fix at prompt level:** every Agent() spawn should include:

> "Return a concise summary (max 300 words) + structured outputs. Do NOT return raw file contents or full grep output — extract only what is needed."

This enforces sidechain isolation at the prompt level, not just the protocol level.

Source: [2026-04-18-cc-sidechain-transcript-isolation.md](../learnings/2026-04-18-cc-sidechain-transcript-isolation.md) (arXiv:2604.14228)

---

## Stage 7 — Task-guided context for workers

Latent Briefing (orchestrator → worker) compression yields **49-65% token savings + 3pp accuracy gain** by passing only task-relevant context to workers, not the full orchestrator trajectory.

| Subtask condition | Approach | Token savings |
|-------------------|----------|---------------|
| Long docs (32k-100k) | Light compaction (preserve coverage) | 49% median |
| Hard questions | Aggressive (strip speculation) | +3pp accuracy |
| Short/easy docs | Moderate | 42% |

**Apply in orchestrate Phase 4:** build per-subtask context packet:
- **Include:** relevant scout facts, relevant prior worker results, subtask-specific files
- **Exclude:** orchestrator's plan-level reasoning, failed hypotheses, unrelated subtask outputs

Speculation and dead-end exploration are noise to workers. DACS (arXiv:2604.07911) extends this to >3 concurrent agents via Registry/Focus mode switching — without selective context, steering accuracy drops to 21-60%; with DACS, 90-98%.

Source: [2026-04-11-task-guided-context-beats-raw-sharing.md](../learnings/2026-04-11-task-guided-context-beats-raw-sharing.md)

---

## Decision Matrix — when to do what

| Symptom | Stage | Action |
|---------|-------|--------|
| Stepping away 2+ min | 1 | `/checkpoint` + `/clear`; resume fresh |
| Long agent outputs accumulating | 2 | Spawn subagent for chunks > 100k; isolate via sidechain |
| 30-40% on 1M context, tool-heavy session | 2 | Compact NOW with direction hint |
| 60% on simple session | 2-3 | Manual `/compact` proactive |
| 70% triggers env-override autocompact | 2-5 | Layer 5 fires automatically — accept loss |
| About to switch tasks | 3-4 | `/compact focus on X, drop Y` BEFORE switching |
| 3-4 compacts already in this session | 4 | `/clear` + session summary + fresh start |
| Worker returning raw grep output | 6 | Add summarization clause to agent prompt |
| Orchestrator passing full trajectory to worker | 7 | Filter to subtask-relevant facts only |

---

## Open gaps

These are points where the lifecycle has empirical evidence but STOPA hasn't fully closed the loop:

1. **`/compact` does not check pressure type.** Should try layer 2-3 before layer 5. (See [bad-compact-direction-unpredictability.md](../learnings/2026-04-18-bad-compact-direction-unpredictability.md))
2. **hybrid-retrieve uses flat weights.** GRM-style query-dependent gating would close the MC formalism. (See [mc-checkpoint-caching-retrieval-pattern.md](../learnings/2026-04-18-mc-checkpoint-caching-retrieval-pattern.md))
3. **Worker prompts don't mandate summarization.** Sidechain isolation is protocol-only, not prompt-enforced. (See [cc-sidechain-transcript-isolation.md](../learnings/2026-04-18-cc-sidechain-transcript-isolation.md))
4. **orchestrate Phase 4 doesn't filter context per subtask.** Latent Briefing pattern not yet implemented. (See [task-guided-context-beats-raw-sharing.md](../learnings/2026-04-11-task-guided-context-beats-raw-sharing.md))

---

## Cross-references

- **Memory architecture** ← retrieval depth, learning maturity, decay (sister article)
- **Orchestration infrastructure** ← context-rot 30-40% (overlapping; this article goes deeper on lifecycle)
- **Skill design** ← `/compact` and `/checkpoint` as lifecycle skills

## Sources (8 learnings)

| Date | File | Uses | Maturity |
|------|------|------|----------|
| 2026-04-01 | autocompact-threshold | 4 | draft |
| 2026-04-11 | task-guided-context-beats-raw-sharing | 4 | draft |
| 2026-04-14 | prompt-cache-ttl-5min | 2 | draft |
| 2026-04-14 | compact-timing-60pct | 3 | draft |
| 2026-04-18 | context-rot-absolute-threshold | 0 | draft |
| 2026-04-18 | cc-graduated-compaction-5layer | 1 | draft |
| 2026-04-18 | bad-compact-direction-unpredictability | 1 | draft |
| 2026-04-18 | mc-checkpoint-caching-retrieval-pattern | 3 | draft |
| 2026-04-18 | cc-sidechain-transcript-isolation | 0 | draft |

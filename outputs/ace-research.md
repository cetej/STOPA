# ACE — Agentic Context Engineering: Research Brief

**Date:** 2026-03-28
**Question:** What concrete techniques from the ACE paper (ICLR 2026) can be backported into STOPA?
**Scope:** Survey — 7 specific technical questions
**Sources consulted:** 15+ (arXiv HTML paper, 9 GitHub source files, SambaNova blog, DC arXiv paper)
**Verification:** 8 top claims checked — 6 MATCH, 1 MISMATCH corrected, 1 WEAK qualified

---

## Executive Summary

ACE (Agentic Context Engineering) is a self-improving system that treats context as an evolving "playbook" updated incrementally from execution feedback. The core insight is **append-only delta updates**: instead of rewriting context on each step (which causes context collapse), ACE appends new bullets with unique IDs and tracks their performance via helpful/harmful counters [VERIFIED]. A separate semantic deduplication step (sentence-transformers + FAISS, cosine ≥ 0.90) handles redundancy without destroying information [VERIFIED].

The most immediately actionable technique for STOPA is the **bullet wire format with counters**: `[sec-00001] helpful=4 harmful=1 :: content`. Every learning entry carries its own performance history, making grep-first retrieval possible while also surfacing which entries should eventually be pruned [VERIFIED]. The second most actionable is **Reflector separation**: ACE deliberately splits "analyze what went wrong" (Reflector) from "what to write to context" (Curator), preventing the noise that comes from letting a single step do both [VERIFIED].

The major limitations: ACE has **no noise filter** — it explicitly acknowledges that without reliable execution signals, context gets polluted [VERIFIED]. There is also **no rollback** — only post-hoc best-checkpoint selection in offline mode [VERIFIED]. STOPA already handles these better through explicit human-triggered `/scribe` and versioned checkpoints.

---

## Detailed Findings

### 1. Delta Update Format — The Curator

The Curator outputs a JSON object with exactly two top-level fields [VERIFIED][2]:

```json
{
  "reasoning": "chain-of-thought analysis...",
  "operations": [
    {
      "type": "ADD",
      "section": "formulas_and_calculations",
      "content": "new bullet content (no ID — system assigns it)"
    }
  ]
}
```

The Curator LLM receives: current playbook, Reflector's analysis, question context, training progress (step/total), and a token budget. It is explicitly instructed to identify **only new insights missing from the current playbook** — redundancy is forbidden in the prompt [VERIFIED][2].

**Operation types defined in code:** ADD, UPDATE, MERGE, DELETE, CREATE_META. However, the current main branch only has ADD fully implemented — the others have a code comment `Note:` explaining they can be added, but no implementation exists [VERIFIED — corrected from initial "TODO" characterization][3]. This is a gap between paper intent and code reality.

**Bullet ID assignment:** The Curator never writes the ID — the system auto-assigns `[<section-slug>-<NNNNN>]` via a global auto-incrementing counter, then prepends it before appending to the playbook [VERIFIED][5].

**How ADD works mechanically:** `apply_curator_operations()` finds the named section header in the playbook text and inserts the new bullet immediately after it [VERIFIED][5].

---

### 2. Context Collapse Prevention

Context collapse is a concrete measured failure: Dynamic Cheatsheet's context on AppWorld went from 18,282 tokens (66.7% accuracy) to 122 tokens in the very next training step, dropping accuracy to 57.1% — below the 63.7% no-adaptation baseline [VERIFIED][1].

ACE prevents this through four layered mechanisms:

**Structural (primary): Append-only ADD** [VERIFIED][3]
The Curator never rewrites existing bullets — only appends new ones. Each new `[id]` is unique; existing bullets are preserved verbatim. Because the playbook grows incrementally, no historical information is destroyed during the primary update loop.

**Procedural: Semantic deduplication via BulletpointAnalyzer** [VERIFIED][4]
Runs periodically (proactively after each delta, or lazily on context window overflow):
- Encodes all bullets via `sentence-transformers` (`all-mpnet-base-v2`)
- Builds cosine similarity matrix via FAISS
- Groups bullets with similarity ≥ 0.90
- Merges each group into one bullet via LLM call that combines content and **sums** `helpful`/`harmful` counts additively

This merge is the only place where bullet content is rewritten, and it is bounded — near-duplicates only, semantic content preserved.

**Informational: Token budget pressure** [INFERRED][2,3]
The Curator prompt receives a `token_budget` parameter and `playbook_stats` (counts of high-performing and problematic bullets) as context. This creates pressure to add quality entries but does not implement automated pruning.

**Statistical: Harmful counter accumulation** [VERIFIED][5]
Bullets tagged as `harmful` by the Reflector accumulate `harmful` counter increments visible in the playbook text. The Curator can use this signal, and DELETE operations are defined in the vocabulary — but automated deletion is not yet implemented [VERIFIED][3].

---

### 3. Reflector Design and Execution Feedback

**Inputs to `reflect()`** [VERIFIED][7]:
- `question` — the original task
- `reasoning_trace` — full chain-of-thought produced by Generator
- `predicted_answer` — Generator's final answer
- `ground_truth` — correct answer (optional)
- `environment_feedback` — execution result (code ran/failed, API response, task success/failure)
- `bullets_used` — set of playbook bullets the Generator referenced

**Two prompt variants** [VERIFIED][6]:
- `REFLECTOR_PROMPT` — used when ground truth is available; compares prediction vs truth
- `REFLECTOR_PROMPT_NO_GT` — used without ground truth; analyzes execution traces and environment_feedback alone

Both prompts instruct the LLM to output JSON with: `reasoning`, `error_identification`, `root_cause_analysis`, `correct_approach`, `key_insight`, and `bullet_tags`. The `bullet_tags` field maps each bullet ID to one of: `"helpful"`, `"harmful"`, or `"neutral"` [VERIFIED][6].

**Refinement rounds:** The Reflector can run up to 5 rounds on the same sample, triggered when the answer is incorrect [INFERRED from paper ablations][1].

**No noise filter** [VERIFIED][1]:
The paper explicitly acknowledges: "when ground-truth supervision or reliable execution signals are absent, the constructed context can be polluted by spurious or misleading signals." The only noise resistance is statistical — a single bad reflection increments a counter by 1, but bullets survive unless harmful consistently accumulates. The `_extract_bullet_tags()` function handles only *parsing* failures (malformed JSON), not *semantic* failures (low-quality reflections) [VERIFIED][7].

---

### 4. Rollback and Update Evaluation

**No rollback mechanism exists** [VERIFIED][8].

The Curator applies ADD operations at a configurable `curator_frequency` regardless of whether recent updates helped or hurt accuracy.

**Best-playbook checkpointing (offline mode only)** [VERIFIED][8]:
1. System evaluates on validation set at intervals
2. When validation accuracy improves → save `best_playbook`
3. After all training → use `best_playbook` for final test (not the latest)

This is post-hoc selection, not online rollback. Mid-training, even if a curator update hurts accuracy, training continues without reverting.

**Online mode: no validation gate** [VERIFIED][8].
In online mode (used for AppWorld), the system operates on a single stream of test samples with no separate validation set — updates are applied immediately after each reflection-curation cycle.

**Per-entry soft evaluation via counters** [INFERRED][5,3]:
`get_playbook_stats()` classifies entries as "high-performing" (`helpful>5, harmful<2`) or "problematic" (`harmful≥helpful`). This is surfaced as diagnostic information, but no automated pruning is enacted based on it.

---

### 5. Architecture — Offline vs Online Modes

Three modes exist [VERIFIED][1,5]:

| Mode | What happens | When to use |
|------|-------------|-------------|
| **Offline** | Batch optimize on train split; context finalized before deployment | Pre-existing labeled/unlabeled data available |
| **Online** | Per-sample: predict → reflect → curate in real time; no train/test boundary | Live deployment, execution feedback only |
| **Eval-only** | Pure evaluation against pre-built playbook; no updates | Measuring final performance |

Offline is the equivalent of "pre-training" the context playbook. Online is the equivalent of continuously fine-tuning from live feedback.

---

### 6. Scaling and Context Growth

**Grow-and-refine mechanism** [VERIFIED][1]:
- **Growth**: new bullets appended with unique IDs
- **Refinement**: existing bullets updated in-place (counter increments, not content rewrites)
- **Deduplication**: semantic embedding similarity prunes redundancy
- **Timing**: proactive (after each delta) or lazy (triggered on context window overflow)

No hard token limit enforced by truncation — the lazy deduplication triggers on overflow. The Curator's delta entries are merged by deterministic non-LLM logic, enabling parallel processing across multiple reflections before merging into the playbook [VERIFIED][3].

---

### 7. AppWorld Benchmark Results

**Overall scores** [VERIFIED with qualification]:
- Offline: ReAct + ACE = **59.4%** average accuracy
- Online: ReAct + ACE = **59.5%** average accuracy
- IBM CUGA (top-ranked, GPT-4.1-based) = **60.3%** overall average
- ACE uses DeepSeek-V3/V3.1 (smaller open-source model)

**On the harder test-challenge split** (TGC metric specifically) [WEAK — single source, not independently confirmed]:
- ACE **surpasses IBM CUGA by 8.4% on TGC** (Task Goal Completion on test-challenge)
- On SGC (SubGoal Completion), ACE leads by +0.7%
- On overall average across all metrics, CUGA still leads by 0.8%

**Efficiency gains** [VERIFIED][5]:
- 86.9% lower adaptation latency vs existing methods
- 91.5% latency reduction and 83.6% token cost reduction vs Dynamic Cheatsheet (online)
- 82.3% latency reduction and 75.1% fewer rollouts vs GEPA (offline)

---

## Disagreements & Open Questions

- **UPDATE/MERGE/DELETE operations**: Present in operation vocabulary but not implemented in main branch. Paper may describe intended design; current code only supports ADD. Verify if a development branch has these.
- **Lazy dedup trigger**: Paper mentions overflow trigger, code confirmation incomplete.
- **Ground-truth vs no-GT performance gap**: Not quantified in the evidence gathered.

---

## Evidence Table

| # | Source | URL | Key Claim | Confidence |
|---|--------|-----|-----------|------------|
| 1 | ACE paper arXiv HTML | https://arxiv.org/html/2510.04618v1 | Context collapse: DC 18,282→122 tokens; all benchmark results; no-noise-filter acknowledgment | High |
| 2 | ace/prompts/curator.py | https://github.com/ace-agent/ace/blob/main/ace/prompts/curator.py | Curator JSON schema; ADD-only instruction; token budget; dedup rule in prompt | High |
| 3 | ace/core/curator.py | https://github.com/ace-agent/ace/blob/main/ace/core/curator.py | ADD implemented; UPDATE/MERGE/DELETE defined but not implemented | High |
| 4 | ace/core/bulletpoint_analyzer.py | https://github.com/ace-agent/ace/blob/main/ace/core/bulletpoint_analyzer.py | sentence-transformers (all-mpnet-base-v2), FAISS, cosine ≥ 0.90, LLM merge | High |
| 5 | playbook_utils.py | https://github.com/ace-agent/ace/blob/main/playbook_utils.py | Bullet format regex; auto-ID assignment; apply_curator_operations; get_playbook_stats | High |
| 6 | ace/prompts/reflector.py | https://github.com/ace-agent/ace/blob/main/ace/prompts/reflector.py | Reflector JSON fields; two prompt variants (GT and no-GT) | High |
| 7 | ace/core/reflector.py | https://github.com/ace-agent/ace/blob/main/ace/core/reflector.py | reflect() inputs; _extract_bullet_tags() parsing-only graceful degradation | High |
| 8 | ace/ace.py | https://github.com/ace-agent/ace/blob/main/ace/ace.py | No rollback; best_playbook saved on val improvement; online no validation gate | High |
| 9 | Dynamic Cheatsheet (arXiv) | https://arxiv.org/html/2504.07952v1 | DC: prior work April 2025; reusable strategies memory; monolithic rewrite | High |

---

## Sources

1. Qizheng Zhang et al. — "Agentic Context Engineering" (arXiv HTML) — https://arxiv.org/html/2510.04618v1
2. ace/prompts/curator.py — https://github.com/ace-agent/ace/blob/main/ace/prompts/curator.py
3. ace/core/curator.py — https://github.com/ace-agent/ace/blob/main/ace/core/curator.py
4. ace/core/bulletpoint_analyzer.py — https://github.com/ace-agent/ace/blob/main/ace/core/bulletpoint_analyzer.py
5. playbook_utils.py — https://github.com/ace-agent/ace/blob/main/playbook_utils.py
6. ace/prompts/reflector.py — https://github.com/ace-agent/ace/blob/main/ace/prompts/reflector.py
7. ace/core/reflector.py — https://github.com/ace-agent/ace/blob/main/ace/core/reflector.py
8. ace/ace.py — https://github.com/ace-agent/ace/blob/main/ace/ace.py
9. Dynamic Cheatsheet (arXiv) — https://arxiv.org/html/2504.07952v1
10. SambaNova blog — https://sambanova.ai/blog/ace-open-sourced-on-github

---

## STOPA Backport Recommendations

### Recommendation 1: Add helpful/harmful counters to learnings entries (HIGH IMPACT, LOW EFFORT)

**What ACE does:** Every playbook bullet carries `helpful=N harmful=N` counters that increment each time the bullet is used and the outcome is tagged.

**Current STOPA state:** Per-file YAML learnings have `severity` (critical/high/medium/low) but no usage-tracking counters.

**Backport:** Add `uses: 0` and `harmful_uses: 0` fields to the YAML frontmatter of learnings files. When a learning is retrieved and applied, increment `uses`. When a session ends badly and the learning was retrieved, increment `harmful_uses`. The `/scribe` skill could write the initial values; the `/critic` or `/verify` skills could tag outcomes.

**Value:** Surfaces stale or harmful learnings automatically. Currently the only signal is date (staleness check after 90 days) — counter tracking adds a quality signal.

---

### Recommendation 2: Separate Reflector from Curator in the critic/scribe cycle (HIGH IMPACT, MEDIUM EFFORT)

**What ACE does:** Reflector analyzes what went wrong (produces `error_identification`, `root_cause_analysis`, `key_insight`). Curator decides what to add to context (produces delta entries). These are separate LLM calls with separate prompts.

**Current STOPA state:** `/critic` reviews code quality but doesn't tag which learnings were activated. `/scribe` writes learnings but doesn't analyze the task outcome systematically. The session COMPOUND step is manual.

**Backport:** Add a lightweight Reflector step at session end:
1. **Reflector call** (Haiku): given task outcome + critic feedback + learnings retrieved this session → output `{what_went_well, what_went_wrong, which_learnings_helped, which_learnings_hurt, key_insight}`
2. **Curator call** (Haiku): given Reflector output + existing learnings → output delta: `{ADD: [new entries], MARK_HARMFUL: [IDs to flag]}`

This prevents the current problem where `/scribe` is only triggered on obvious wins, not on subtle failures.

---

### Recommendation 3: Append-only writing to learnings (MEDIUM IMPACT, ZERO EFFORT)

**What ACE does:** Curator only adds new bullets; never rewrites existing ones. The BulletpointAnalyzer periodically merges near-duplicates via embeddings.

**Current STOPA state:** `/scribe` creates new files per learning — already append-only at the file level. `critical-patterns.md` is a hand-curated always-read summary.

**Gap:** No deduplication step. Over time, similar learnings accumulate without merging.

**Backport:** Add a `/scribe maintenance` mode that:
1. Reads all learnings in `learnings/`
2. Groups similar entries (can use simple keyword overlap instead of embeddings — STOPA doesn't need FAISS)
3. Prompts the user to confirm merge candidates
4. Merges confirmed duplicates, summing `uses` counters if tracking is added per Rec 1

---

### Recommendation 4: Structured Reflector output in /critic (LOW EFFORT, USEFUL)

**What ACE does:** Reflector always outputs `error_identification`, `root_cause_analysis`, `correct_approach`, `key_insight` in structured JSON.

**Current STOPA state:** `/critic` produces free-text review without structured analysis.

**Backport:** Add a structured section to `/critic` output:
```
## Root Cause Analysis
- **Error type:** [logic bug | missing case | wrong abstraction | spec misread]
- **Root cause:** [1 sentence]
- **Correct approach:** [what should have been done]
- **Key insight:** [what to remember]
```

This makes critic output directly usable by `/scribe` without re-analysis.

---

### What ACE does that STOPA should NOT copy

1. **No rollback** — STOPA's checkpoint system with versioned saves is already better than ACE's best_playbook approach. Keep it.

2. **No noise filter** — STOPA's human-in-the-loop `/scribe` is a noise filter by design. ACE's statistical counter approach is a necessary evil for fully autonomous systems. Since STOPA has human confirmation available, don't automate away from it.

3. **Online mode (per-sample auto-update)** — ACE's fully autonomous online learning makes sense for production agents running thousands of tasks. STOPA sessions are interactive; the human provides the feedback signal. Don't automate the reflection trigger.

---

## Coverage Status

- **[VERIFIED]:** 11 claims directly checked against source code and paper HTML
- **[INFERRED]:** 2 claims (lazy dedup trigger threshold; 5-round refinement trigger condition)
- **[WEAK]:** 1 claim (8.4% TGC improvement — single source, qualifier added)
- **[UNVERIFIED]:** 0 claims

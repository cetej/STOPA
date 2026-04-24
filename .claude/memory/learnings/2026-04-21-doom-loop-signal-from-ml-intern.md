---
date: 2026-04-21
type: best_practice
severity: medium
component: hook
tags: [panic, detection, ml-intern]
summary: "Detect tool-call repetition via signature hashing — identical consecutive (3+) and [A,B,A,B] sequences — catches Grep/Read panic loops that edit-fail cycles miss."
source: external_research
uses: 2
harmful_uses: 0
successful_uses: 0
confidence: 1.0
maturity: draft
verify_check: "Grep('doom_identical', path='.claude/hooks/panic-detector.py') → 1+ matches"
related: [2026-04-07-hook-failure-modes.md, 2026-04-18-hook-import-path-silent-blockage.md]
---

## Context

Ported from huggingface/ml-intern `agent/core/doom_loop.py` into STOPA's `panic-detector.py` as Signal 6.

The existing 5 signals missed a key blind spot: repeated identical tool calls (e.g. Grep with same args 3× expecting different results) or alternating sequences ([Read, Bash, Read, Bash]) without edit-fail cycles. These patterns appear when the agent is stuck in a research/exploration loop rather than an edit loop.

## Implementation

- `args_hash` added to every event in `extract_event()`: `hashlib.md5(json.dumps(tool_input, sort_keys=True).encode()).hexdigest()[:12]`
- `detect_identical_consecutive(sigs, threshold=3)` — returns tool name if 3+ identical (tool, args_hash) pairs consecutive
- `detect_repeating_sequence(sigs)` — detects [A,B,...,A,B,...] patterns length 2-5 with 2+ reps, returns 'A->B' string
- Signal scores: identical → +3 pts; sequence → +2 pts
- Yellow gate updated to accept `doom_` prefix (valid panic without bash failures)
- Intervention messages append Czech-language pattern description

## Key lessons

- Adapting from litellm ToolCallSignature dataclass: skip the dataclass, use plain `(str, str)` tuples — simpler and no extra dependency
- `scored_events` filtering (infra exclusions already applied) means doom detection automatically ignores infrastructure errors — no special handling needed
- Size constraint: 526 → 610 lines = exactly at +15% budget (I2 invariant)

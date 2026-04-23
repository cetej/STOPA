---
skill: koder
date: 2026-04-23
task: "Add batch URL mode to /radar skill"
outcome: success
project: STOPA
task_file: "koder-queue/radar-batch-mode.md"
files_changed:
  - .claude/skills/radar/SKILL.md
  - .claude/commands/radar.md
exit_reason: completed
---

## What Was Done

- Updated `description:` field to include "batch URL list (2+ URLs pasted)" trigger condition
- Updated `argument-hint` to include `<URL-list (2+ lines)>`
- Updated intro paragraph: "two modes" → "three modes" (manual, batch, scan)
- Added batch detection rule to Input parser (2+ lines starting with `https?://` → Mode 3)
- Added Mode 3: Batch URL Evaluation section with:
  - Circuit breaker: > 50 URLs → STOP
  - Step 1: Classify & Parallel Fetch (github/arxiv via Jina, x.com via WebSearch, other with fallback)
  - Step 2: Score & Aggregate (3-Gate Filter + table template)
  - Step 3: Append to radar.md by tier (≥8 → 🔴, 5-7 → 🟡, <5 → 🟢) + Stats + Scan Log entry + /improve for 🔴
- Added Anti-Rationalization row: "I'll process batch URLs one-by-one to be safe"
- Synced commands/radar.md identically (core-invariant #2)

## Verification

```
diff commands/radar.md skills/radar/SKILL.md → DIFF_EMPTY (files identical)
grep -c "batch|Batch Evaluation" SKILL.md → 6 matches (≥3 required)
python yaml.safe_load(frontmatter) → YAML_VALID
description starts with: "Use when evaluating..."
wc -l SKILL.md → 280 lines (246 baseline + 34, = +13.8%, within +15% limit)
git commit → 98bfe28, 2 files, 78 insertions, 10 deletions
```

## What Failed (if any)

Growth invariant triggered at first pass (307 lines = +25%). Fixed by compressing
Mode 3 from 63 net lines to 34 net lines — merged parallel fetch + classify into
one step, collapsed append rules to one line. Final: 280 lines = +13.8%.

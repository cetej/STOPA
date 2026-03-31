# Trace-Informed Proposer Protocol

Meta-Harness-inspired (arXiv:2603.28052): full execution traces dramatically outperform
scores-only feedback for optimization (56.7% vs 38.7%). Summaries compress away diagnostic
information — always read raw traces selectively via grep, never summarize.

## Activation

This protocol applies only when `.traces/<run_id>/` exists. If no trace directory: skip all
trace steps and fall back to standard git-history-based proposing.

## Trace Initialization (call from Phase 0: Setup)

After creating feature branch and before baseline measurement:

```bash
# Generate run_id
RUN_ID="autoloop-$(basename <target> .md)-$(date +%s)"
TRACE_DIR=".traces/$RUN_ID"
mkdir -p "$TRACE_DIR/diffs"

# Write activation marker for trace-capture.py hook
cat > .claude/memory/intermediate/trace-active.json << EOF
{
  "skill": "autoloop",
  "run_id": "$RUN_ID",
  "target": "<target>",
  "trace_dir": "$TRACE_DIR/",
  "started": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "current_iteration": 0
}
EOF

# Purge old traces (>7 days)
find .traces/ -maxdepth 1 -mtime +7 -exec rm -rf {} + 2>/dev/null || true
```

## Iteration Metadata (call from Step 7: Log to TSV)

After updating TSV, also write to `.traces/<run_id>/iterations.jsonl`:

```jsonl
{"iter":N,"hypothesis":"<description>","metric":88.3,"delta":1.2,"status":"keep","commit":"c3d4e5f","files_changed":["path"],"loc_delta":12,"ts_start":"...","ts_end":"...","duration_s":45}
```

And update the marker's current_iteration:
```bash
# Update iteration counter in marker (for trace-capture.py hook)
python -c "
import json; p='.claude/memory/intermediate/trace-active.json'
d=json.loads(open(p).read()); d['current_iteration']=<N>
open(p,'w').write(json.dumps(d))
"
```

## Diff Capture (call from Step 3: Commit)

After each successful commit:
```bash
git diff HEAD~1 > .traces/<run_id>/diffs/iter-$(printf '%03d' <N>).diff
```

## Proposal Logging (call from Step 2: Modify)

Before making the edit, append to `.traces/<run_id>/proposals.jsonl`:
```jsonl
{"iter":N,"proposal":"<what to change>","rationale":"<why, based on trace analysis>","trace_evidence":"<specific trace finding or null>","strategy":"<exploit|explore|combine|simplify|radical|fix_crash>"}
```

## Trace-Informed Review Protocol (integrate into Step 1: Review)

### After DISCARD or CRASH

1. **Find failed tool calls:**
   ```bash
   grep "\"iteration\":<prev_iter>" .traces/<run_id>/tools.jsonl | grep -v "\"exit\":0"
   ```
2. **Read error outputs:** For each failed call, read the `output_full` field — this shows
   WHAT failed and the exact error message
3. **Read the diff:** `.traces/<run_id>/diffs/iter-<NNN>.diff`
4. **Mandatory diagnosis** (write to proposals.jsonl `trace_evidence` field):
   > "The change to [section/function] caused [error from trace] because [causal analysis]."
   This must reference specific trace data, not speculation.

### After KEEP

1. **Read the successful diff:** `.traces/<run_id>/diffs/iter-<NNN>.diff`
2. **Read verify output from traces:**
   ```bash
   grep "\"iteration\":<prev_iter>" .traces/<run_id>/tools.jsonl | grep "verify\|test\|eval"
   ```
3. **Attribution:** Which specific code change drove the metric improvement?
   Record in proposals.jsonl `trace_evidence`.

### On Plateau (3+ consecutive discards)

This is where traces provide the biggest advantage over scores-only feedback.

1. **Read ALL failed diffs:**
   ```bash
   # List recent discard iterations from TSV
   grep "discard" autoloop-results.tsv | tail -5
   # Read their diffs
   cat .traces/<run_id>/diffs/iter-<each>.diff
   ```

2. **Pattern detection across failures:** Are all failed diffs:
   - Touching the same section/function? → That area may be at local optimum
   - Making similar types of changes? → The approach class is exhausted
   - Breaking the same test/check? → A specific constraint is blocking progress

3. **Mandatory self-diagnosis statement** (append to proposals.jsonl):
   > "The last N attempts all [pattern from diffs]. This suggests [constraint/insight].
   > Pivoting to [structurally different approach]."

   This mirrors the Meta-Harness finding where the proposer self-diagnosed that
   "modifications to prompts and completion flow are high risk" after 6 regressions
   and shifted to a purely additive approach.

4. **Use trace evidence to choose pivot direction:**
   - If errors clustered in one section → try optimizing a DIFFERENT section
   - If complexity-adding changes all failed → try simplification
   - If all diffs were large → try minimal surgical edits

## Trace Deactivation (call from Phase 3: Report)

```bash
rm -f .claude/memory/intermediate/trace-active.json
```

Do NOT delete `.traces/<run_id>/` — it stays for `/eval --optim` analysis and auto-purges after 7 days.

# Trace-Informed Hypothesis Protocol

Meta-Harness-inspired (arXiv:2603.28052): full execution traces dramatically outperform
scores-only feedback for optimization (56.7% vs 38.7%). Summaries compress away diagnostic
information — always read raw traces selectively via grep, never summarize.

## Activation

This protocol applies only when `.traces/<run_id>/` exists. If no trace directory: skip all
trace steps and fall back to standard git-history-based proposing.

## Trace Initialization (call from Phase 0: Research Setup)

After creating experiment branch and before baseline measurement:

```bash
# Generate run_id
RUN_ID="autoresearch-$(basename <slug>)-$(date +%s)"
TRACE_DIR=".traces/$RUN_ID"
mkdir -p "$TRACE_DIR/diffs"

# Write activation marker for trace-capture.py hook
cat > .claude/memory/intermediate/trace-active.json << EOF
{
  "skill": "autoresearch",
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

## Iteration Metadata (call from Step 8: Log to TSV)

After updating TSV, also write to `.traces/<run_id>/iterations.jsonl`:

```jsonl
{"iter":N,"hypothesis":"<name>","metric":0.85,"delta":0.03,"status":"keep","commit":"c3d4e5f","files_changed":["path"],"loc_delta":12,"ts_start":"...","ts_end":"...","duration_s":45}
```

And update the marker's current_iteration:
```bash
python -c "
import json; p='.claude/memory/intermediate/trace-active.json'
d=json.loads(open(p).read()); d['current_iteration']=<N>
open(p,'w').write(json.dumps(d))
"
```

## Diff Capture (call from Step 4: Commit)

After each commit:
```bash
git diff HEAD~1 > .traces/<run_id>/diffs/iter-$(printf '%03d' <N>).diff
```

## Proposal Logging (call from Step 2: Hypothesize)

Before making the edit, append to `.traces/<run_id>/proposals.jsonl`:
```jsonl
{"iter":N,"hypothesis":"<name>","rationale":"<why, based on trace analysis>","trace_evidence":"<specific trace finding or null>","strategy":"<edge_case|adversarial|scale|composition|literature>"}
```

## Trace-Informed Review Protocol (integrate into Step 1: Review)

### After DISCARD

1. **Find failed tool calls:**
   ```bash
   grep "\"iteration\":<prev_iter>" .traces/<run_id>/tools.jsonl | grep -v "\"exit\":0"
   ```
2. **Read error outputs:** For each failed call, read the `output_full` field — this shows
   WHAT failed and the exact error message
3. **Read the diff:** `.traces/<run_id>/diffs/iter-<NNN>.diff`
4. **Mandatory diagnosis** (write to proposals.jsonl `trace_evidence` field):
   > "The hypothesis [name] failed because [causal analysis from trace]. The eval output
   > showed [specific error/metric]. Feed this into next RATIONALE field."
   This must reference specific trace data, not speculation.

### On PIVOT (batch ASSESS decides PIVOT)

Before spawning research rescue agent, summarize trace patterns:

1. **Collect all DISCARD iterations from TSV**
2. **Read their diffs:**
   ```bash
   grep "discard\|crash" autoresearch-log.tsv | awk '{print $1}' | while read N; do
     cat .traces/<run_id>/diffs/iter-$(printf '%03d' $N).diff 2>/dev/null
   done
   ```
3. **Pattern detection across failures:** Are failed hypotheses:
   - Touching the same subsystem? → That area may be at local optimum
   - Making similar types of changes? → The approach class is exhausted
   - Producing the same failure category (DEPENDENCY, LOGIC, etc.)? → Systemic constraint

4. **Write pivot summary** (append to rescue agent's prompt):
   > "Of N discarded hypotheses, M failed because [pattern from eval outputs and diffs].
   > Traces show [specific evidence]. Avoid approaches that [constraint inferred from traces]."

   This mirrors the Meta-Harness finding where the proposer self-diagnosed "modifications
   to prompts and completion flow are high risk" after 6 regressions and shifted approach.

### After KEEP

1. **Read the successful diff:** `.traces/<run_id>/diffs/iter-<NNN>.diff`
2. **Read successful eval output from traces:**
   ```bash
   grep "\"iteration\":<prev_iter>" .traces/<run_id>/tools.jsonl | grep "eval\|metric\|score"
   ```
3. **Attribution:** Which specific change drove the metric improvement?
   Record in proposals.jsonl `trace_evidence`.

## Trace Deactivation (call from Phase 3: Synthesis Report)

```bash
rm -f .claude/memory/intermediate/trace-active.json
```

Do NOT delete `.traces/<run_id>/` — it stays for `/eval --optim` analysis and auto-purges after 7 days.

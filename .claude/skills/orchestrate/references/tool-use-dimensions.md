# Tool Use Audit Dimensions

Reference: "The Evolution of Tool Use in LLM Agents" (arXiv:2603.22862)

6 dimensions for auditing multi-tool orchestration systems. Use as diagnostic checklist.

| # | Dimension | STOPA Component | Status | Gap |
|---|-----------|----------------|--------|-----|
| 1 | **Inference-time planning** — how agents decide which tools at runtime | Phase 2 Decomposition + SMART gate | Good | SMART gate is prompt-level; could be strengthened with learned routing |
| 2 | **Training & trajectory construction** — building agent capabilities | tier-heuristics.md + Meta-Harness traces | OK | No fine-tuning; rely on prompt engineering + heuristic DB |
| 3 | **Safety & control** — preventing runaway tool chains | Circuit breakers, 3-fix escalation, calm-steering | Good | No per-tool risk scoring (all tools treated equally) |
| 4 | **Efficiency under constraints** — cost management | Budget tiers, haiku/sonnet/opus selection, if: guards | Good | No tool-call deduplication or caching layer |
| 5 | **Capability completeness** — handling diverse tool ecosystems | Plugin discovery, MCP lazy loading, requires: field | OK | No dynamic tool registration at runtime |
| 6 | **Benchmark design** — measuring agent performance | /eval skill, harness JSONL traces | OK | No trajectory-level benchmarks (only per-subtask) |

## Improvement Priority (by ROI)

1. **Dim 4: Tool-call deduplication** — if same grep/read was done recently, skip. Low effort, saves tokens.
2. **Dim 6: Trajectory benchmarks** — log full orchestration traces, not just subtask results. Enables regression detection.
3. **Dim 3: Per-tool risk scoring** — classify tools as safe/risky, apply different approval thresholds. Aligns with Defer PreToolUse.
4. **Dim 1: Learned routing** — if tier-heuristics.md grows to 20+ rows, consider structured routing model.

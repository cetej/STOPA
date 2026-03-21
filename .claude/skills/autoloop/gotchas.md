# AutoLoop — Gotchas

Known failure modes. Add a line each time Claude trips on something.

## Metric Design
- **Pure LLM-as-judge is expensive** — use structural heuristics (grep-based, zero LLM cost) for fast iterations, LLM validation only at end
- **Hybrid metric (structural + LLM) scores best** — M5 pattern outperforms pure M1 (LLM) or M2 (structural) consistently
- **Metric must be deterministic** — if same input gives different scores, the loop can't converge. Pin randomness

## Loop Control
- **No plateau detection** — if score hasn't improved for 3 iterations, stop. Don't burn tokens on diminishing returns
- **Forgetting git rollback** — always commit before each iteration so you can revert cleanly. No commit = no rollback
- **Editing wrong file** — verify target file path at start. Loop on wrong file = wasted iterations

## Scope
- **One file, one metric** — don't try to optimize multiple files or metrics simultaneously. Decompose first
- **Prompt optimization needs different approach than code** — prompts are more sensitive to small changes; use smaller deltas per iteration

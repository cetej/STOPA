# Advisor Checkpoint — Strategic Consultation Protocol

Lightweight advisor pattern for iterative skills (autoloop, autoresearch, self-evolve).
Mimics Anthropic's native Advisor Tool (advisor_20260301) using CC Agent sub-agents.

## When to Invoke

Advisor checkpoint fires at existing strategic decision points — NOT as a new step:
- **autoloop**: at progress summary (every 5 iterations, line "=== AutoLoop Progress")
- **autoresearch**: at BATCH ASSESS (every `ceil(budget/3)` iterations)
- **self-evolve**: at heartbeat check (every 5 rounds)

## Protocol

At the checkpoint, spawn ONE sub-agent:

```
Agent(
  model: "opus",
  prompt: "
    You are a strategic advisor for an iterative optimization loop.
    Your ONLY job: review the trajectory and suggest ONE strategic direction change.
    Do NOT write code. Do NOT make edits. Return max 500 tokens.

    ## Current State
    - Iteration: <N> / <budget>
    - Baseline: <baseline_metric> → Current best: <best_metric> (+<delta>)
    - Keeps: <K> | Discards: <D> | Crashes: <C>
    - Improvement trend: <improving | flat | declining>
    - Last 3 iteration summaries:
      <paste from results TSV>

    ## Strategies Tried
    <brief list of approaches attempted>

    ## Your Task
    Answer these 3 questions in ���500 tokens:
    1. DIAGNOSIS: What pattern do you see in the keeps vs discards?
    2. DIRECTION: What should the next 3 iterations focus on? (be specific)
    3. AVOID: What approaches should be abandoned based on evidence?

    If everything looks good and the current direction is working: say 'STAY_COURSE' and why.
  "
)
```

## Cost Control

- **Interval**: every 5 iterations (autoloop), every batch (autoresearch), every 5 rounds (self-evolve)
- **Max consultations per run**: 3 (for budget ≤10) or 5 (for budget >10)
- **Token budget**: advisor response ≤500 tokens (Opus generates ~400-700 per consultation)
- **Skip conditions**:
  - Budget ≤ 3 iterations → skip entirely (not enough data to advise on)
  - Improvement trend is "strong improving" → skip (don't fix what works)
  - Already at max consultations → skip

## Using the Advisor Response

1. Read the advisor's 3-part response
2. If STAY_COURSE: log "advisor: stay course" and continue normally
3. If direction change suggested:
   - Log the advisor suggestion to run diary / experiment log
   - Incorporate DIRECTION into next hypothesis generation
   - Add AVOID items to the "strategies that fail" list
4. NEVER blindly follow advisor — it doesn't see the code, only metrics

## Metrics to Track

In the optstate JSON (`autoloop.json`, `autoresearch.json`, `self-evolve.json`):
```json
{
  "advisor_consultations": 0,
  "advisor_direction_changes": 0,
  "advisor_stay_course": 0,
  "post_advisor_improvement_rate": 0.0
}
```

After each advisor consultation, track whether the next 2 iterations improved.
If `post_advisor_improvement_rate` drops below 0.3 after 5+ consultations:
the advisor isn't helping — reduce interval or disable.

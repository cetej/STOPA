# Scenario: Structural Completeness — Anti-Rationalization Defense

The autoloop skill is about to be used for iterative optimization. Before proceeding,
verify that the skill has behavioral guardrails that prevent the agent from rationalizing
away important steps in the loop.

**Check**: Does the skill have an `## Anti-Rationalization Defense` section with a
table containing at least 3 rows, with columns `Rationalization | Why Wrong | Do Instead`?

The section must include rationalizations specific to iterative optimization loops,
such as skipping verification, bundling changes, or continuing past circuit breakers.

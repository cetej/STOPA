# Scenario: Structural Completeness — Verification Checklist

Before declaring an autoloop run "done", the operator needs to know that the
output is actually valid — not just that the iteration count was reached.

**Check**: Does the skill have a `## Verification Checklist` section with at least 3
checkboxes (`- [ ]`) covering exit criteria that can be objectively verified?

The checklist must include verifiable criteria, NOT subjective assessments.
Examples of GOOD criteria: "Final metric is higher than baseline (from TSV log)",
"Guard command still passes", "Branch is clean (no uncommitted changes)".
Examples of BAD criteria: "Output looks good", "Changes seem correct".

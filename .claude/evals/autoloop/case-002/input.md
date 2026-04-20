# Scenario: Structural Completeness — Red Flags

The autoloop skill runs optimization loops that can waste significant compute if
misused. Operators need observable warning signs that tell them when the loop is
being misapplied or is about to produce garbage output.

**Check**: Does the skill have a `## Red Flags` section listing phrased as observable
symptoms (gerunds or "Doing X without Y" format), covering at minimum:
- Running without a verify command when the target isn't a SKILL.md
- Modifying guard/test files during the loop
- Continuing past circuit breaker signals

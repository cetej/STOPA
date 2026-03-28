---
id: critic-002
skill: critic
title: Detects missing error handling in an orchestration plan
eval-tags: [quality_review]
ideal_steps: 6
ideal_tool_calls: 3
max_acceptable_steps: 12
fixture: inline
---

# Eval Case: Detects missing error handling in an orchestration plan

Tests that `/critic` catches a gap in an orchestration plan where a critical step has no failure path.

## Fixture

Write this content to `.harness/eval-fixtures/critic-002-fixture.md` before invocation:

```markdown
# Migration Plan: Database Schema v2

## Steps

### Step 1: Backup current database
- Run `pg_dump` to create full backup
- Verify backup file size > 0

### Step 2: Apply migration script
- Run `alembic upgrade head`
- Migration adds 3 new columns to `users` table

### Step 3: Validate data integrity
- Run `python validate_migration.py`
- Check row counts match pre-migration snapshot

### Step 4: Update application config
- Change `DB_SCHEMA_VERSION=2` in environment
- Restart application services

### Step 5: Monitor for 30 minutes
- Watch error rate dashboard
- Check latency metrics

## Rollback

If Step 5 monitoring shows issues, revert DB_SCHEMA_VERSION and restart.
```

## Invocation

```
/critic .harness/eval-fixtures/critic-002-fixture.md
```

## Assertions

| # | Type | Check | Expected |
|---|------|-------|----------|
| A1 | contains | Output contains verdict (PASS, WARN, or FAIL) | true |
| A2 | contains | Output has "Recommendations" or "Issues" section | true |
| A3 | contains | Output flags Step 2 or migration as risky (no rollback if migration itself fails) | true |
| A4 | contains | Output mentions error handling, failure path, or rollback gap | true |

## Scoring

- 4 assertions pass: PASS
- 2-3 assertions pass: PARTIAL
- 0-1 assertions pass: FAIL

## Why This Matters

The plan has a subtle gap: rollback only covers Step 5, but if Step 2 (migration) fails mid-way, there's no recovery path. A good critic should catch this.

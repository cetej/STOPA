---
name: pr-review
description: Use when reviewing a pull request and /critic alone is not thorough enough — provides 6 expert perspectives. Trigger on 'review PR', 'review pull request', 'zkontroluj PR', PR URLs. Do NOT use for reviewing local code changes (use /critic), for creating PRs (use git), or for simple style checks (use linter).
argument-hint: <PR number or URL> [--post]
context:
  - gotchas.md
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Agent
model: sonnet
effort: high
maxTurns: 20
---

# PR Review — Multi-Persona Pull Request Review

You review a PR from 6 expert perspectives, then synthesize findings into a single actionable review.

## Shared Memory

Read `.claude/memory/learnings.md` — apply known patterns and anti-patterns to the review.

## Phase 0: Load PR Context

Parse `$ARGUMENTS` to get PR number or URL.

```bash
gh pr view <number> --json title,body,baseRefName,headRefName,files,additions,deletions,author
gh pr diff <number>
```

Capture:
- **Title & description**
- **Changed files** (list + diff)
- **Size** (additions/deletions)
- **Author**
- **Base branch**

## Phase 1: Six-Perspective Review

Run each review perspective sequentially. Each perspective produces findings as a list of issues.

### 1. Developer Review
Focus: code quality, readability, performance, adherence to project conventions
- Are variable/function names clear?
- Is the logic correct and efficient?
- Does it follow existing patterns in the codebase?
- Are there unnecessary changes or scope creep?
- Edge cases handled?

### 2. Security Review
Focus: vulnerabilities, data handling, authentication, OWASP Top 10
- Input validation present?
- SQL injection / XSS / command injection risks?
- Secrets or credentials in code?
- Proper error handling (no stack traces leaked)?
- Authorization checks where needed?

### 3. QA Review
Focus: test coverage, edge cases, regression risk
- Are new/changed paths covered by tests?
- Do tests actually assert meaningful behavior?
- Could this change break existing functionality?
- Are error scenarios tested?
- Integration test implications?

### 4. DevOps Review
Focus: CI/CD, deployment, monitoring, infrastructure
- Does this need a migration?
- Config changes needed in deployment?
- Performance impact at scale?
- Logging/monitoring adequate for new paths?
- Backward compatibility with rolling deploys?

### 5. Product Review
Focus: business value, user impact, spec compliance
- Does the change match the described intent?
- User-facing text clear and correct?
- Edge cases from a user perspective?
- Accessibility considerations?

### 6. Architecture Review
Focus: design patterns, coupling, future maintainability
- Does this introduce tight coupling?
- Is the abstraction level appropriate?
- Will this scale if the feature grows?
- Does it follow the project's architecture patterns?

## Phase 2: Synthesize

Combine all findings into a single structured review:

```markdown
## PR Review: #<number> — <title>

**Verdict**: APPROVE / REQUEST_CHANGES / COMMENT
**Risk level**: Low / Medium / High
**Changed files**: <count> (+<additions> -<deletions>)

### Critical Issues (must fix)
- [ ] <issue> — *<perspective>*

### Suggestions (should fix)
- [ ] <issue> — *<perspective>*

### Nits (optional)
- [ ] <issue> — *<perspective>*

### Positive Notes
- <what's done well>

### Summary
<2-3 sentence overall assessment>
```

## Phase 3: Post (optional)

If `--post` flag was passed:

```bash
gh pr review <number> --body "<review content>" --<verdict>
```

Where verdict is `--approve`, `--request-changes`, or `--comment`.

Ask user for confirmation before posting.

## Rules

1. **Read the full diff** — don't skip files, every change matters
2. **Be specific** — reference file:line for each finding
3. **Prioritize** — critical issues first, nits last
4. **Be constructive** — suggest fixes, not just problems
5. **No false positives** — only flag real issues, not style preferences unless they violate project conventions
6. **Context matters** — check surrounding code to understand patterns before flagging "violations"
7. **Improvements must be addressed now** — no "future work" deferrals for real issues

---
name: skill-audit
description: Audit all skills for description quality, tool permissions, integration patterns, and consistency
phases: 5
estimated_tokens: 50K-100K
output_template: template.md
---

# Skill Audit Harness

Comprehensive audit of all SKILL.md files in the project. Checks description quality, tool permissions (least privilege), shared memory integration, and overall consistency.

## Phase 1: Inventory (deterministic)

- **Action**: Glob for all `**/skills/*/SKILL.md` files. For each, extract YAML frontmatter fields: name, description, user-invocable, allowed-tools, disallowed-tools, model, effort, maxTurns, context
- **Validation**: ≥1 skill found, all extracted fields are valid YAML
- **Output file**: `.harness/phase1_inventory.json`
- **Model**: haiku
- **Output schema**:
```json
{
  "_meta": {"phase": 1, "timestamp": "ISO8601", "model": "haiku"},
  "skills_count": N,
  "skills": [
    {
      "name": "string",
      "path": "string",
      "description": "string",
      "user_invocable": true/false,
      "allowed_tools": ["string"],
      "disallowed_tools": ["string"],
      "model": "string",
      "effort": "string",
      "max_turns": N,
      "context_files": ["string"],
      "has_negative_trigger": true/false
    }
  ]
}
```

## Phase 2: Description Audit (LLM)

- **Action**: For each skill from Phase 1, evaluate description quality:
  - Is it specific enough for auto-invocation? (Would Claude know WHEN to use this?)
  - Does it have positive triggers? (keywords, phrases)
  - Does it have negative triggers? ("Do NOT use when...")
  - Could it be confused with another skill? (overlap check)
  - Is the description under 300 chars? (token efficiency)
- **Validation**: Every skill has a quality score (1-5) and at least one finding
- **Output file**: `.harness/phase2_descriptions.json`
- **Model**: sonnet
- **Output schema**:
```json
{
  "_meta": {"phase": 2, "timestamp": "ISO8601", "model": "sonnet"},
  "audits": [
    {
      "name": "string",
      "quality_score": 1-5,
      "has_positive_triggers": true/false,
      "has_negative_triggers": true/false,
      "overlap_risk": ["other-skill-name"],
      "description_length": N,
      "findings": ["string"],
      "recommendations": ["string"]
    }
  ]
}
```

## Phase 3: Tools Audit (deterministic + LLM)

- **Action**: For each skill, analyze tool permissions:
  - List allowed and disallowed tools
  - Check for over-permission (e.g., Write+Edit when only Read needed)
  - Check for under-permission (instructions reference tools not in allowed list)
  - Flag skills with Agent but no model specification
  - Flag skills with Bash but no clear justification
- **Validation**: Every skill has a permission assessment (ok/over/under)
- **Output file**: `.harness/phase3_tools.json`
- **Model**: sonnet
- **Output schema**:
```json
{
  "_meta": {"phase": 3, "timestamp": "ISO8601", "model": "sonnet"},
  "audits": [
    {
      "name": "string",
      "allowed_tools": ["string"],
      "disallowed_tools": ["string"],
      "permission_level": "ok|over-permissioned|under-permissioned",
      "findings": ["string"],
      "recommendations": ["string"]
    }
  ]
}
```

## Phase 4: Integration Audit (LLM)

- **Action**: For each skill, check integration patterns:
  - Does it read shared memory (state.md, learnings.md, budget.md)?
  - Does it write to shared memory after completion?
  - Does it reference other skills (cross-invocation)?
  - Does it follow the PLAN → WORK → ASSESS → COMPOUND loop?
  - Does it have cost awareness (budget checks)?
- **Validation**: Every skill has an integration score and findings
- **Output file**: `.harness/phase4_integration.json`
- **Model**: sonnet
- **Output schema**:
```json
{
  "_meta": {"phase": 4, "timestamp": "ISO8601", "model": "sonnet"},
  "audits": [
    {
      "name": "string",
      "reads_memory": true/false,
      "writes_memory": true/false,
      "cross_references": ["other-skill-name"],
      "follows_compound_loop": true/false,
      "has_budget_awareness": true/false,
      "integration_score": 1-5,
      "findings": ["string"],
      "recommendations": ["string"]
    }
  ]
}
```

## Phase 5: Report (template-based)

- **Action**: Fill `template.md` with data from Phases 1-4. Generate:
  - Summary table: skill × audit dimensions
  - Top issues (sorted by severity)
  - Recommendations (actionable, prioritized)
  - Overall health score
- **Validation**: All `{{PLACEHOLDER}}` filled, no missing data, report ≤ 500 lines
- **Output file**: `.harness/report.md`
- **Model**: haiku

### Phase 5b: Regression Baseline (deterministic)

- **Action**: After report generation, compute aggregate scores from Phase 2-4 JSON outputs:
  - `description_avg` = mean of all `quality_score` from `phase2_descriptions.json`
  - `tools_avg` = mean where ok=5, over-permissioned=2, under-permissioned=3 from `phase3_tools.json`
  - `integration_avg` = mean of all `integration_score` from `phase4_integration.json`
  - `health_score` = mean of (description_avg, tools_avg, integration_avg)
  - `skills_count` = from `phase1_inventory.json`
- **TSV Append**: Append one row to `.claude/memory/eval-baseline.tsv`. Create file with header if it doesn't exist.
- **TSV format**:
  ```
  # skill-audit regression baseline — append only
  run_date	skills_count	health_score	description_avg	tools_avg	integration_avg	notes
  ```
- **Validation**: TSV row count increased by 1 (count)
- **Model**: haiku

### Phase 5c: Auto-Eval Chain (optional)

- **Action**: If `.claude/evals/` directory exists with case files, automatically chain into eval-runner harness.
- **Trigger**: Always, unless `--skip-evals` argument was passed
- **Execution**: Run `/harness eval-runner` (all cases). Append eval summary to the skill-audit report.
- **Model**: (delegated to eval-runner harness)
- **Purpose**: After auditing skill quality statically, verify behavioral correctness automatically. No user action needed.

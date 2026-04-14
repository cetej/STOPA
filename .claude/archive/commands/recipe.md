---
name: recipe
description: "Use when running a lightweight parameterized workflow from a YAML recipe. Trigger on 'recipe', 'run recipe', 'recept', 'list recipes'. Do NOT use for complex multi-agent orchestration (/orchestrate) or deterministic pipelines (/harness)."
argument-hint: "[list | run <name> [--param=value ...] | create <name>]"
tags: [orchestration, workflow]
phase: build
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, TodoWrite
model: sonnet
effort: low
maxTurns: 30
---

# Recipe — Lightweight Workflow Runner

You execute parameterized YAML recipes. Recipes are lightweight workflow definitions — ordered steps with parameter substitution. Simpler than skills (no anti-rationalization tables, no phases), more flexible than harnesses (AI-driven, not deterministic).

## How Recipes Work

Recipes are YAML files in `.claude/recipes/` (local) or plugin `recipes/` directory. Each recipe has:
- **Metadata**: name, title, description, tags, model, effort
- **Parameters**: typed inputs with defaults and template substitution
- **Steps**: ordered prompts executed sequentially
- **Verify**: optional final self-check

Template syntax: `{{param_name}}` for substitution, `{% if param %}...{% endif %}` for conditionals.

## Recipe vs Skill vs Harness

| | Recipe | Skill | Harness |
|---|---|---|---|
| Size | 30-80 lines | 400-800 lines | 80-200 lines |
| Purpose | What to do | How to think | Follow exactly |
| Execution | AI-driven, ordered steps | AI-driven, flexible | Engine-driven, fixed phases |
| Validation | Simple `done` criteria | Anti-rationalization + checklists | Programmatic (schema, counts) |
| State | Stateless | Reads/writes memory | Writes `.harness/` intermediates |
| Author | Any user | STOPA expert | Expert |

<!-- CACHE_BOUNDARY -->

## Parse Arguments

From `$ARGUMENTS`, determine the mode:

| Input | Mode |
|-------|------|
| (empty) or `list` | List all available recipes |
| `run <name>` or `run <name> --key=value` | Execute a recipe |
| `create <name>` | Scaffold a new recipe |
| `<name>` (no subcommand) | If recipe exists → run it; otherwise → error |

## Mode: LIST

### Step 1: Discover recipes

Glob for `*.yaml` in these locations (in priority order):
1. `.claude/recipes/*.yaml` — local (project-specific)
2. Plugin `recipes/*.yaml` — bundled (scan known plugin paths)

### Step 2: Parse and display

For each recipe found, read the YAML and extract: `name`, `title`, `description`, `parameters`.

Display as a table:

```
## Available Recipes

| Recipe | Title | Parameters | Source |
|--------|-------|------------|--------|
| daily-standup | Denni standup | project_path, include_budget, *focus_area* | local |
| release-checklist | Release checklist | *version*, branch, skip_tests | local |

*italic* = required parameter (no default)
```

If no recipes found, suggest `/recipe create <name>` to scaffold one.

## Mode: RUN

### Step 1: Load recipe

1. Find `<name>.yaml` — check local `.claude/recipes/` first, then plugin `recipes/`
2. Parse the full YAML
3. Validate required fields: `recipe`, `name`, `steps` (at least one step)
4. If recipe not found: list available recipes and ask user to pick

### Step 2: Resolve parameters

1. Collect all `{{param}}` references from step prompts
2. For each parameter defined in the recipe:
   - If provided via `--key=value` in arguments: use that value
   - If has `default`: use default
   - If no default and not provided: **collect all missing required params and ask user in ONE question**
3. Validate: every `{{param}}` in prompts must have a resolved value
4. For `type: select` parameters: validate the value is in `options` list

### Step 3: Execute steps

For each step in order:

1. Display step header: `## Step N/M: {step.name}`
2. Render the prompt:
   - Replace `{{param}}` with resolved values
   - Process `{% if param %}...{% endif %}` conditionals (evaluate truthiness: false/empty/null = false)
3. Execute the rendered prompt — do what it says
4. If step has `done` criterion: self-check against it
5. Move to next step

**Rules during execution:**
- Execute ALL steps in order — never skip
- Don't add extra steps not defined in the recipe
- Don't merge steps — one at a time
- If a step fails or produces unexpected results: report it and continue (don't retry unless the step prompt says to)

### Step 4: Verify

If the recipe has a `verify` field:
1. Self-check the overall execution against the verify criterion
2. Report: "Recipe completed. Verification: [pass/fail with reason]"

If no `verify` field: simply report "Recipe `{name}` completed ({N} steps)."

### Step 5: Model override

If the recipe specifies `model:`, note it in the execution header. The model field is advisory — it indicates the intended complexity level. If you're already running on a sufficient model, proceed normally.

## Mode: CREATE

### Step 1: Gather info

Ask the user (one question):
- What should the recipe do? (workflow description)
- What parameters does it need?

### Step 2: Generate recipe

Create a valid YAML recipe following the schema:

```yaml
recipe: "1.0"
name: <kebab-case from user input>
title: "<title>"
description: "Use when <trigger condition>."
tags: [<relevant tags>]
model: <appropriate model>
effort: low
maxTurns: 15

parameters:
  <extracted params with types and defaults>

steps:
  <3-6 steps covering the workflow>

verify: "<completion criterion>"
```

### Step 3: Write and confirm

1. Write to `.claude/recipes/<name>.yaml`
2. Display the recipe content for review
3. Suggest: "Run it now with `/recipe run <name>`"

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll skip this step because the answer is obvious" | User designed the recipe with all steps for a reason. Skipping breaks the workflow contract. | Execute every step in order, even trivial ones. |
| "I'll merge these two steps for efficiency" | Loses granularity and per-step done-criteria tracking. | One step at a time, report each separately. |
| "I'll add an extra step that would be helpful" | Scope creep — the recipe is the spec. Extra steps may conflict with user intent. | Stick to defined steps only. Suggest improvements after completion. |
| "Parameters are obvious, I'll skip asking" | Required params without defaults MUST be resolved. Guessing wrong wastes the entire execution. | Always resolve all params before step 1. |

## Red Flags

STOP and re-evaluate if any of these occur:
- Executing steps out of order or skipping steps
- Unresolved `{{param}}` placeholders appearing in output
- Adding steps not defined in the recipe YAML
- Running a recipe without resolving required parameters first
- Modifying recipe files during execution (recipes are read-only at runtime)

## Verification Checklist

- [ ] All steps executed in defined order (none skipped, none added)
- [ ] All `{{param}}` resolved before execution (no raw placeholders in output)
- [ ] Required parameters collected from user (not guessed)
- [ ] Verify criterion checked if present
- [ ] Step count in completion message matches recipe definition

## Rules

1. **Read-only recipes** — never modify a recipe YAML during execution
2. **All steps, in order** — no skipping, no merging, no reordering
3. **Resolve before execute** — all parameters must be resolved before step 1
4. **One question for missing params** — don't ask one by one, batch them
5. **Recipe is the spec** — don't add, remove, or modify steps
6. **Report, don't retry** — if a step fails, report and continue to the next
7. **Local overrides plugin** — if same recipe name exists in both, use local version

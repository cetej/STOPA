---
name: mcp-flow
description: Use when executing a multi-step workflow that crosses MCP servers (e.g., GitHub PR → memory write → Telegram notification, Calendar event → fetch context → prep brief). Trigger on 'mcp-flow', 'run flow <name>', 'cross-tool flow', 'propaguj přes nástroje'. Do NOT use for single-MCP operations (call the tool directly), or for code execution flows (use /orchestrate).
argument-hint: <flow-name> [key=value ...]
discovery-keywords: [mcp, cross-tool, workflow, propagation, multi-service, github-to-telegram, calendar-prep, dual-write]
tags: [orchestration, devops]
phase: build
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, mcp__github__get_pull_request, mcp__github__get_issue, mcp__github__add_issue_comment, mcp__plugin_telegram_telegram__reply, mcp__stopa-memory__memstore_write_memory, mcp__stopa-memory__memstore_read_memory, mcp__e27626c3-6a73-478e-b549-50b244a018e3__list_events, mcp__e27626c3-6a73-478e-b549-50b244a018e3__get_event, mcp__4d0c1623-7e8b-4f1e-9b9a-36886f0f768b__search_threads, TodoWrite
deny-tools: [Bash, Agent]
permission-tier: workspace-write
model: sonnet
effort: low
maxTurns: 20
max-depth: 1
input-contract: "user → flow_name + optional kwargs → flow definition exists in mcp-flows/"
output-contract: "execution log + final outputs → markdown report in stdout, optional dual-write to memory"
---

# MCP Flow — Cross-Tool Workflow Executor

Execute deklarativně-popsanou sekvenci MCP volání napříč servery (GitHub, Telegram, Calendar, Gmail, memory). Pattern řeší případy, kde žádný stávající skill nepokrývá full workflow napříč servisy a vytvoření jednorázového skillu by bylo overkill.

**Co MCP flow NENÍ:**
- Není to runtime engine — Claude (model) exekuuje kroky manuálně podle YAML deklarace
- Není to nahrazení existujících skills (improve, handoff, checkpoint, radar) — ty pokračují dál pro svoje use cases
- Není to sub-orchestrace (max-depth=1) — flow nesmí spawnovat agents

**Co MCP flow JE:**
- Deklarativní popis sekvence MCP volání s template substitution mezi kroky
- Reproducible cross-tool workflow (stejný YAML → stejné kroky)
- Library v `.claude/skills/mcp-flow/flows/<flow>.yaml`

## When to Use

- **GitHub PR closed → write decision to memory → notify Telegram** (notification flow)
- **Tomorrow's calendar event → fetch context z relevant ticket → prep brief** (calendar-prep flow)
- **Search Gmail label → ingest matching emails do brain** (email-ingest flow)
- Multi-service ad-hoc workflow that you'd write a script for, but want repeatable + composable

## When NOT to Use

- Single MCP server operation → call the tool directly
- Code generation/editing flow → `/orchestrate` (Phase 4 agents)
- Cross-project routing → `/improve` (already wired)
- Capturing findings → `/handoff` or `/scribe`
- "Watch ecosystem" → `/watch`, `/radar`

<!-- CACHE_BOUNDARY -->

## Workflow

### Phase 1: Load Flow Definition

Parse `$ARGUMENTS` — first token = flow name, rest = `key=value` overrides.

```
$ARGUMENTS = "pr-merged repo=cetej/STOPA pr=42"
→ flow_name = "pr-merged"
→ inputs = {repo: "cetej/STOPA", pr: "42"}
```

Read flow YAML: `.claude/skills/mcp-flow/flows/<flow_name>.yaml`

If flow file does not exist:
- List available flows from the directory (Glob)
- Also check user-local flows in `.claude/memory/intermediate/mcp-flows/` (gitignored, ad-hoc only)
- Print: "Flow '<name>' not found. Available: <list>. To create new flow, write `.claude/skills/mcp-flow/flows/<name>.yaml` (shipped) or `.claude/memory/intermediate/mcp-flows/<name>.yaml` (local, gitignored)."
- STOP.

### Phase 2: Validate Inputs

For each `inputs.<key>` declared in YAML:
- Check it's provided in CLI args OR has a `default:` value in YAML
- Missing required input (no default) → STOP, ask user: "Flow '<name>' requires <key>. Provide via `key=value`."

### Phase 3: Execute Steps Sequentially

For each step in `steps[]`:

1. **Resolve template variables** in step args using `{{inputs.X}}` and `{{step_<id>.output.Y}}` syntax
2. **Invoke the MCP tool** with resolved args (use the tool listed in `step.tool`)
3. **Capture output** under `step_<id>.output` for downstream substitution
4. **Log execution**: tool name, args (redacted if `redact: true`), success/failure, output snippet
5. **On step failure**:
   - If `step.on_error == "abort"` (default) → STOP entire flow, report partial state
   - If `step.on_error == "continue"` → log error, mark step as failed, continue to next
   - If `step.on_error == "retry"` → retry once with 5s pause, then abort

**Atomicity rule:** flow is NOT transactional — partial execution is possible. Each step that mutates external state (memory write, telegram send, github comment) commits independently. Document in flow comments which steps are mutating.

### Phase 4: Report

Output a markdown report with:

```markdown
## MCP Flow: <flow_name>

**Status**: completed | partial | failed
**Inputs**: <resolved input values>
**Duration**: <approximate>

### Step Log

| # | Tool | Status | Output (truncated) |
|---|------|--------|--------------------|
| 1 | mcp__github__get_pull_request | ok | PR #42: "Fix auth bug" |
| 2 | mcp__stopa-memory__memstore_write_memory | ok | wrote to decisions/pr-42 |
| 3 | mcp__plugin_telegram_telegram__reply | ok | sent to chat 123 |

### Final Outputs

<step outputs that the flow YAML marks as `expose: true`>
```

If flow YAML has `dual_write: true`, also write the report markdown to `.claude/memory/intermediate/mcp-flow-runs/<flow>-<timestamp>.md` (gitignored — local audit trail only).

## Flow YAML Schema

```yaml
name: pr-merged
description: "When a PR merges, record decision and notify"
safety_class: mutating-external  # see below — required for proactive composition gating

inputs:
  repo:
    required: true
  pr:
    required: true
  chat_id:
    default: "{{env.TELEGRAM_DEFAULT_CHAT}}"

steps:
  - id: fetch_pr
    tool: mcp__github__get_pull_request
    args:
      owner: "{{inputs.repo | split:/ | first}}"
      repo: "{{inputs.repo | split:/ | last}}"
      pull_number: "{{inputs.pr}}"
    expose: true

  - id: write_decision
    tool: mcp__stopa-memory__memstore_write_memory
    args:
      key: "decisions/pr-{{inputs.pr}}"
      value: "PR {{inputs.pr}} merged: {{step_fetch_pr.output.title}}"
    on_error: continue

  - id: notify
    tool: mcp__plugin_telegram_telegram__reply
    args:
      chat_id: "{{inputs.chat_id}}"
      text: "PR {{inputs.repo}}#{{inputs.pr}} merged: {{step_fetch_pr.output.title}}"
    on_error: continue

dual_write: true
budget_cap: 0.20
```

## Safety Class (per-flow gating for proactive composition)

Every flow YAML MUST declare a `safety_class` field. The composition engine (`trigger-engine.py`) reads this when `/mcp-flow <name>` appears in a `composition-rules.yaml` sequence and decides whether the flow may fire proactively.

| Value | Meaning | Proactive composition? |
|---|---|---|
| `read-only` | All steps only read (github_get, memstore_read, calendar_list_events). No writes. | ✅ Allowed |
| `mutating-local` | Writes only to local memory/files (memstore_write, fs writes). No external visibility. | ✅ Allowed |
| `mutating-external` | Sends to external services with visible side effects (Telegram reply, GitHub comment, email send). | ❌ Forbidden — user-invoked only |

**Rules:**
1. Field is REQUIRED for new flows. Missing → engine fail-safe to `mutating-external` (forbidden).
2. Classify by the WORST step in the flow (one telegram_reply makes the entire flow `mutating-external`).
3. User-invoked `/mcp-flow <name>` always runs regardless of class — gating only applies to proactive composition firing.
4. Adding a new mutating-external step to an existing `mutating-local` flow → MUST update the class.

## Available Flows

Run `Glob .claude/skills/mcp-flow/flows/*.yaml` to list. Bootstrapping flows shipped with this skill:

- `pr-merged` — record PR merge decision + Telegram notify (`mutating-external`)
- `calendar-prep` — pull tomorrow's events + summarize from related memory (`mutating-local`)

Add new flows by writing YAML to `mcp-flows/`. No code changes required.

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll just call the MCP tools directly without a flow YAML — faster" | Single-shot ad-hoc calls don't capture the workflow as artifact. Next time you need the same flow, you re-derive it. | Save the flow as YAML once. Subsequent calls are reproducible and composable. |
| "Flow failed at step 3 — let me retry from step 1 manually" | Steps 1 and 2 mutated external state (memory, telegram). Re-running from 1 = duplicate side effects. | Use `start_at: <step_id>` argument to resume from failed step. Or fix flow YAML to make steps idempotent. |
| "I'll add a Bash step to the flow for a quick shell command" | Bash is denied — flow must stay MCP-only. Shell commands invite scope creep into orchestration territory. | If you need shell, use `/orchestrate` for the broader task and call /mcp-flow as one subtask. |
| "Let me put a secret API key in the flow YAML inputs" | YAMLs are checked into git. Secret leaks. | Reference env vars: `default: "{{env.MY_API_KEY}}"`. Engine reads from environment, never from YAML literal. |
| "I'll spawn an Agent to handle a complex step" | Agent spawn = sub-orchestration. max-depth=1 forbids it. | Decompose into multiple flow steps OR escalate to /orchestrate. |

## Red Flags

STOP and re-evaluate if:
- Flow YAML has more than 8 steps (probably needs decomposition into 2+ flows)
- Steps mutate same external resource without idempotency keys
- Template substitution chains 4+ hops (`{{step_a.output.b.output.c}}`) — fragile
- Flow has no `on_error` declarations on mutating steps (silent partial failures)
- You're tempted to add conditional logic / branching — flow is wrong abstraction, write a real script

## Verification Checklist

- [ ] Flow YAML loaded and parsed without errors
- [ ] All required inputs provided OR have defaults
- [ ] Each step's MCP tool is in `allowed-tools` (else permission denied at runtime)
- [ ] Mutating steps have explicit `on_error` policy
- [ ] Final report shows status per step + final outputs
- [ ] If `dual_write: true`, run record exists in `mcp-flow-runs/`

## Rules

1. **Declarative only** — flow logic lives in YAML, not in skill body
2. **Linear sequence** — no branching, loops, or conditionals (use multiple flows or escalate)
3. **MCP tools only** — Bash, Agent, Edit, Write are denied via deny-tools
4. **Inputs validated upfront** — STOP before step 1 if required input missing
5. **One step at a time** — sequential, no parallelism (parallelism = orchestrate territory)
6. **Idempotent steps preferred** — partial failures must be re-runnable
7. **No secrets in YAML** — env var references only

# Agent Return Contract (per-Agent() invocation)

**Status:** design spec, opt-in via subtask `return_format: "json"` flag. Backward compat preserved.

**Ref:** ParaManager (arXiv:2604.17009) — small orchestrator + standardized Agent-as-Tool returns > heterogeneous APIs. STOPA issue #18.

**Complement to** [`completion-contract.md`](completion-contract.md) — session-level invariants (Phase 5). This contract is per-call (Phase 4).

## Why a structured return shape?

Current state (Phase 4 step 4): worker agents return free-form prose. Orchestrator pipes "first 500 chars of each artifact" into a Haiku verifier that emits `STEP_PASS / STEP_WARN / STEP_FAIL`. That's a **two-pass design** — worker writes prose, then Haiku transforms prose to status.

ParaManager design eliminates pass 2: worker emits structured status directly. Orchestrator parses JSON, no second LLM call needed for routine cases.

**Trade-off:**
- ✅ Saves ~200 tokens/subtask (no Haiku verifier on opt-in subtasks)
- ✅ Deterministic flow control via `next_action_signal`
- ✅ Cross-skill consistency (every skill emits same shape)
- ❌ Worker prompt must include schema (slight overhead, ~150 tokens)
- ❌ Workers might emit invalid JSON → fallback path required

Net win when subtask count ≥ 3 per wave (saved verifier passes > schema overhead).

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["status", "subtask_id", "brief"],
  "properties": {
    "status": {
      "type": "string",
      "enum": ["complete", "partial", "blocked", "failed"]
    },
    "subtask_id": {
      "type": "string",
      "description": "Matches subtask id in state.md plan (e.g., 'st-2')"
    },
    "brief": {
      "type": "string",
      "maxLength": 200,
      "description": "1-sentence summary of what was done or why blocked"
    },
    "artifacts": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Paths to files created/modified, or doc identifiers"
    },
    "verified": {
      "type": "boolean",
      "description": "True iff worker ran a check (test, build, grep) and it passed"
    },
    "verification_method": {
      "type": "string",
      "enum": ["tests_pass", "build_succeeds", "grep_check", "manual_inspection", "none"]
    },
    "blockers": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["type", "detail"],
        "properties": {
          "type": {
            "type": "string",
            "enum": ["missing_dep", "ambiguous_spec", "infra_error", "scope_too_big", "needs_user_input", "external_failure"]
          },
          "detail": {"type": "string"}
        }
      }
    },
    "next_action_signal": {
      "type": "string",
      "enum": ["ready_for_critic", "ready_for_next_wave", "needs_user_input", "needs_replan", "needs_retry"]
    }
  }
}
```

### Field semantics

| Field | Required | Notes |
|-------|----------|-------|
| `status` | yes | Mirrors completion semantics: complete=full pass, partial=acceptance criteria met but caveats, blocked=cannot proceed, failed=ran but produced wrong output |
| `subtask_id` | yes | Enables orchestrator to update state.md without disambiguation |
| `brief` | yes | Replaces "first 500 chars" heuristic — worker controls summary |
| `artifacts` | recommended | Empty array if no files modified (e.g., research subtask returning brief only) |
| `verified` + `verification_method` | recommended | When `verified: false`, orchestrator must trigger /verify or accept user risk |
| `blockers` | conditional | Required iff `status` ∈ {blocked, partial, failed} |
| `next_action_signal` | recommended | Drives Phase 4 → Phase 5 flow without LLM inference |

## Examples

### Example 1: Light-tier success (single edit)

```json
{
  "status": "complete",
  "subtask_id": "st-1",
  "brief": "Renamed `parse_url` to `parse_uri` in 3 files; tests still pass.",
  "artifacts": ["src/utils/uri.py", "src/handlers/route.py", "tests/test_uri.py"],
  "verified": true,
  "verification_method": "tests_pass",
  "next_action_signal": "ready_for_critic"
}
```

Orchestrator action: skip Phase 4 step 4 verifier, go directly to Phase 5 critic.

### Example 2: Blocked — missing dependency

```json
{
  "status": "blocked",
  "subtask_id": "st-3",
  "brief": "Cannot implement OAuth flow — `httpx` is not in requirements.txt.",
  "artifacts": [],
  "verified": false,
  "verification_method": "none",
  "blockers": [
    {"type": "missing_dep", "detail": "httpx>=0.27 needed for AsyncClient.post"}
  ],
  "next_action_signal": "needs_user_input"
}
```

Orchestrator action: pause Phase 4, surface blocker to user (don't auto-install deps).

### Example 3: Partial — found unrelated issue

```json
{
  "status": "partial",
  "subtask_id": "st-2",
  "brief": "Migration written and tested, but discovered legacy `users_old` table referenced by 2 unaudited views.",
  "artifacts": ["migrations/0042_add_user_email_idx.sql", "tests/test_migration_0042.py"],
  "verified": true,
  "verification_method": "tests_pass",
  "blockers": [
    {"type": "scope_too_big", "detail": "Views `v_user_summary`, `v_admin_dashboard` reference deprecated table — out of subtask scope but should be tracked"}
  ],
  "next_action_signal": "ready_for_critic"
}
```

Orchestrator action: proceed to critic (subtask is done), but log blockers to state.md as follow-up candidate (potential `mcp__ccd_session__spawn_task`).

## Migration path

### Phase 1 (current): design spec only
- This document exists. Workers continue free-form returns.
- No code/prompt changes elsewhere.

### Phase 2 (opt-in pilot)
- Subtask schema in state.md gains optional `return_format: "json"` field
- Phase 4 worker prompts conditionally append schema instructions:
  > Return your final answer as a JSON object matching the schema in
  > `.claude/skills/orchestrate/references/agent-return-contract.md`. Do not
  > include surrounding prose — JSON only.
- Orchestrator parser:
  1. Try `json.loads(agent_output)` — if success, validate against schema
  2. If invalid JSON or fails validation → fallback to current "first 500 chars" + Haiku verifier
- Run pilot on 3-5 light-tier tasks, compare token cost vs baseline.

### Phase 3 (broad adoption — pending pilot signal)
- Make `return_format: "json"` default for standard+ tier
- Update `Phase 4 step 4` to skip Haiku verifier when JSON status present
- Update agent worker SKILL.md templates to teach contract awareness
- Cross-reference from `completion-contract.md` → per-call contract

### Phase 4 (out of scope for this spec)
- RL training on contract compliance (paper Section 4) — requires labeled trajectories
- SFT with recovery mechanisms — overkill for current STOPA scale

## Backward compatibility

- Workers WITHOUT contract awareness continue working — orchestrator's free-form fallback handles them
- `return_format` field absent in subtask → orchestrator defaults to free-form expectation
- No breaking change for existing skills until Phase 3

## Validation

When opt-in subtasks emit JSON, orchestrator validates against this schema. On validation failure:
1. Log to state.md: `agent_return: invalid_json (subtask st-N)`
2. Fall back to free-form parsing (current Phase 4 step 4)
3. Count toward 3-fix escalation if recurring

## Cross-references

- [`completion-contract.md`](completion-contract.md) — session-level invariants (Phase 5)
- [`agent-execution.md`](agent-execution.md) — Phase 4 worker dispatch detail
- `.claude/rules/skill-files.md` — `output-contract:` field for skill-level shape (this contract is per-Agent() invocation, complementary)
- arXiv:2604.17009 §3 — ParaManager Agent-as-Tool interface design

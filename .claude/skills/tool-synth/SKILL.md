---
name: tool-synth
description: "Use when a subtask has no matching skill (triage emits TRIAGE_NO_MATCH, /orchestrate Phase 3 decomposition step 3 finds no fit, or semantic search over .claude/skills/ scores < 0.4). Dynamically synthesizes a draft skill in sandbox .claude/skills/_generated/<slug>/ gated by commit-invariants. Trigger on 'tool-synth', 'no skill matches', 'synthesize skill', 'generate skill for this subtask'. Do NOT use to edit existing skills (/skill-generator), to iteratively improve a skill with evals (/self-evolve), or to audit existing learnings (/evolve)."
argument-hint: [subtask description]
tags: [meta, orchestration, generated]
phase: build
version: "0.1.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
disallowed-tools: Agent
max-depth: 1
model: sonnet
effort: low
maxTurns: 12
---

# Tool Synthesis — Dynamic Skill Generator

Ref: Autogenesis Protocol (arXiv:2604.15034), §5.2 tool generator. GAIA Level 3 +33.3 pp absolute from dynamic tool synthesis at runtime.

When the static skill catalog misses a subtask, synthesize a DRAFT skill into the sandbox `.claude/skills/_generated/<slug>/SKILL.md` — version `0.1.0`, `maturity: draft`, `valid_until: <today+7>`, `tags: [generated]`. Invariants from `rules/commit-invariants.md` are enforced AT SYNTHESIS TIME — generation fails closed if any invariant is violated.

**Non-recursive**: `max-depth: 1` and `disallowed-tools: [Agent]` prevent this skill from invoking itself or spawning sub-orchestrators that could re-enter synthesis.

## Preconditions

- `$ARGUMENTS` = subtask description (1-2 sentences). Reject if empty or < 20 chars.
- Resource ledger exists: `.claude/memory/resource-ledger.jsonl`
- Sandbox dir creatable: `.claude/skills/_generated/` (gitignored)

## Workflow (SEPL operators)

### Phase 0: Validate Input

1. Read `$ARGUMENTS`. If empty, < 20 chars, or lacks any verb → STOP with: `"Subtask description too vague for synthesis. Refine and retry."`
2. Extract a **slug** — kebab-case, 3-5 lowercase words, no special chars, max 40 chars. Example: `"redact PII from log files"` → `redact-pii-from-logs`.
3. Compute `valid_until = today + 7 days` (ISO date).

### Phase 1: Reflect (ρ) — Semantic miss check

Confirm the synthesis is warranted. Generation must only run when no existing skill fits.

1. Extract 2-4 key terms from the subtask description (nouns + action verbs).
2. Grep existing skills for each term:
   - `Grep pattern="<term>" path=".claude/skills/" glob="*/SKILL.md"` (description + discovery-keywords fields)
3. For each matched skill, read first 20 lines of SKILL.md and score fit 0.0-1.0 based on:
   - Description verb overlap with subtask verb (0.4 weight)
   - Description noun/object overlap with subtask nouns (0.4 weight)
   - Exclusion rules ("Do NOT use for...") — if subtask matches exclusion, fit drops to 0.0 (0.2 weight)
4. Decision:
   - **Top match >= 0.4** → **REJECT synthesis**. Output: `"Existing skill /{name} scores {score:.2f} — use it instead. Synthesis aborted."` Exit.
   - **Top match < 0.4** AND no sandbox duplicate (see Phase 1b) → proceed to σ.

### Phase 1b: Sandbox Duplicate Check

Prevent skill explosion — reject if a near-duplicate already exists in `_generated/`.

1. `Glob pattern=".claude/skills/_generated/*/SKILL.md"`
2. For each result, read its description and run the same fit score vs the current subtask.
3. If any existing sandbox skill scores >= 0.5 → **REJECT**. Output: `"Sandbox skill /{name} already covers this — reuse or promote it (uses={N}). Synthesis aborted."`

### Phase 2: Select (σ) — Propose skill skeleton

Formulate the skill parameters. No files written yet.

Propose in working memory:
- `name`: slug from Phase 0
- `description`: MUST start with "Use when..." — one sentence stating trigger conditions + one sentence stating exclusion. Max 280 chars for draft skills (less than the 1536 hard limit — drafts should be focused).
- `allowed-tools`: least privilege — pick from `[Read, Glob, Grep]` by default. Add `Write, Edit` ONLY if subtask requires file mutation. Add `Bash` ONLY if shell is unavoidable. NEVER grant `Agent` (prevents recursion).
- `tags: [generated, <primary-capability>]` — always include the `generated` tag.
- `phase`: one of `define | plan | build | verify | review | ship | meta` — pick based on subtask verb.
- `model`: `haiku` for mechanical/read-only, `sonnet` for reasoning.
- `effort`: `low`.
- `maxTurns`: 8.

If any field cannot be determined confidently → **REJECT**. Output: `"Subtask too ambiguous to synthesize a focused skill. Consider /brainstorm or decompose further."`

### Phase 3: Improve (ι) — Write sandbox SKILL.md

Write to `.claude/skills/_generated/<slug>/SKILL.md` using this template. Do NOT create a `commands/` copy — sandbox skills are not published through the standard sync.

```markdown
---
name: <slug>
description: "Use when <trigger>. Do NOT use for <exclusion>."
argument-hint: [input]
tags: [generated, <capability>]
phase: <lifecycle-phase>
version: "0.1.0"
maturity: draft
valid_until: <YYYY-MM-DD+7>
user-invocable: false
allowed-tools: <comma-separated-list>
disallowed-tools: Agent
max-depth: 1
model: <haiku|sonnet>
effort: low
maxTurns: 8
synthesized-by: tool-synth
synthesized-at: <YYYY-MM-DD>
synthesized-for-subtask: "<first 120 chars of subtask description>"
---

# <Title Case Name>

<One-paragraph purpose statement derived from subtask description.>

## Preconditions

- <input requirement derived from subtask>

## Workflow

1. **Read input** — <what to read, specific file/glob patterns if known from subtask>
2. **Execute core operation** — <the action the subtask requires, as imperative step>
3. **Verify output** — <pass/fail criterion derived from subtask done-when>

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I already know this pattern, skip verification" | Draft skill — unvalidated assumptions likely wrong | Run the verification step |
| "Close enough, the output looks right" | Draft skills need pass/fail evidence, not vibes | Produce the artifact specified in Workflow step 3 |
| "This is a one-shot, skip structure" | /tool-synth drafts exist to be reused → structured output enables promotion | Follow all three Workflow steps |

## Red Flags

STOP and escalate if any of these occur:
- Input doesn't match preconditions — don't invent what's missing
- Output would exceed the scope of the subtask
- The operation needs a tool not in `allowed-tools`

## Verification Checklist

- [ ] Preconditions checked before execution
- [ ] Workflow steps executed in order
- [ ] Output matches the subtask's done-when criterion

## Notes

Sandbox skill synthesized by /tool-synth on <YYYY-MM-DD>. Expires <YYYY-MM-DD+7>. Promotion to top-level `.claude/skills/` requires `uses >= 3` AND successful critic gate via /evolve.
```

Substitute concrete values from Phase 2's proposal into the template. Keep the generated SKILL.md under 120 lines — drafts are deliberately minimal.

### Phase 4: Evaluate (ε) — Invariant checks

Enforce `rules/commit-invariants.md` at synthesis time. If ANY invariant fails, delete the file and abort.

Run in sequence (stop on first failure):

| # | Check | Command / Test | On failure |
|---|-------|----------------|------------|
| I1 | Description starts with `Use when` | `Grep pattern="^description:.*\"Use when" path=".claude/skills/_generated/<slug>/SKILL.md"` → 1 match | Delete file, REJECT with I1 cited |
| I2 | Line count ≤ 200 (draft ceiling, stricter than 1200 absolute) | `python -c "import sys; print(sum(1 for _ in open(sys.argv[1], encoding='utf-8')))" <path>` | Delete file, REJECT with I2 cited |
| I3 | No secret patterns | `Grep pattern="sk-\|API_KEY=\|SECRET=\|TOKEN=\|Bearer " path=".claude/skills/_generated/<slug>/SKILL.md"` → 0 matches | Delete file, REJECT with I3 cited |
| I4 | YAML frontmatter parses | `python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1], encoding='utf-8').read().split('---')[1])" <path>` | Delete file, REJECT with I4 cited |
| I_name | Slug unique (no clash with top-level skill OR sandbox skill) | `Glob ".claude/skills/<slug>/SKILL.md"` → 0; `Glob ".claude/skills/commands/<slug>.md"` → 0 (when that dir exists) | Delete file, REJECT with slug-clash cited |

Also enforce generation-specific gates:
- Description length ≤ 280 chars (draft tightness)
- `allowed-tools` does NOT contain `Agent` (recursion prevention)
- `disallowed-tools` contains `Agent`
- `max-depth: 1`

Failure → `Bash: rm <path> && rmdir .claude/skills/_generated/<slug>` (Windows: use `rm -rf` via Git Bash). Report WHICH invariant failed.

### Phase 5: Commit (κ) — Register in ledger

All invariants passed → commit the synthesis.

1. Append a single JSONL entry to `.claude/memory/resource-ledger.jsonl`:
   ```bash
   python scripts/resource-ledger.py log ".claude/skills/_generated/<slug>/SKILL.md" "0.0.0" "0.1.0" "tool-synth created for subtask: <first 80 chars>"
   ```
2. Output to caller:
   ```
   SYNTHESIZED: /{slug}
   Location: .claude/skills/_generated/{slug}/SKILL.md
   Version: 0.1.0 (draft, expires {valid_until})
   Invariants: PASS (I1-I4, slug unique, recursion-safe)
   Next: orchestrator invokes /{slug} as a regular skill for the originating subtask.
   ```

The generated skill is IMMEDIATELY usable — `/orchestrate` treats `.claude/skills/_generated/*` as a regular skill source during its current session. Entry is sandboxed (gitignored); only graduation promotes it to tracked state.

## Promotion Path (handled by /evolve, not here)

Generated skills graduate to top-level `.claude/skills/<name>/` when:
- `uses >= 3` (tracked via auto-increment by `/orchestrate` Phase 4 step 10a on invocation; `/evolve` Step 3g audits and proposes graduation)
- `successful_uses >= 1` (at least one critic PASS recorded — proxy for "last critic score on a run using this skill was PASS")
- `harmful_uses == 0` (any critic FAIL blocks graduation; routes to pruning review instead)
- `valid_until` not yet expired
- Human approval (user explicitly approves the `/evolve` graduation proposal)

Expired drafts are cleaned up by `/sweep` (checks `valid_until < today`).

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "The subtask is unique — just synthesize quickly, skip the fit check" | Phase 1 semantic search prevents skill explosion. Skipping it creates N near-duplicate drafts. | Always run Phase 1 before Phase 2. If fit >= 0.4 exists, REJECT. |
| "The invariants are advisory — commit even if I2 line count is slightly over" | Commit-invariants are fail-closed by design. Bloated drafts poison the sandbox. | Delete the file on invariant failure. Retry with a tighter template. |
| "I'll grant `Agent` in allowed-tools — the subtask might need delegation" | Granting Agent to a synthesized draft enables recursion loops and explodes blast-radius. | Never grant Agent. If the subtask genuinely needs delegation, /tool-synth is the wrong skill — escalate to /skill-generator manually. |
| "The slug matches an existing skill — I'll add a `-v2` suffix" | Slug uniqueness is an invariant. `-v2` suffixes are how skill catalogs rot. | REJECT and report which skill collides. User decides whether to supersede. |
| "Description doesn't quite start with 'Use when' but it's close — good enough" | I1 is non-negotiable — routing depends on the exact prefix. Fuzziness here breaks /triage. | Rewrite the description. If Phase 2 can't produce a compliant description, REJECT. |

## Red Flags

STOP and re-evaluate if any of these occur:
- Generating a second draft with similar slug to an existing `_generated/` skill
- Writing a SKILL.md longer than 150 lines
- Adding `Agent` or `Bash` to `allowed-tools` without explicit subtask justification
- Description summarizing the workflow instead of stating trigger conditions
- Skipping Phase 4 invariant checks because "the template is correct"

## Verification Checklist

- [ ] Slug passed uniqueness check (no top-level or sandbox clash)
- [ ] Description starts with `Use when` and is ≤ 280 chars
- [ ] All 4 mandatory invariants (I1-I4) executed and logged PASS
- [ ] `allowed-tools` does not contain `Agent`; `disallowed-tools` contains `Agent`
- [ ] `version: "0.1.0"`, `maturity: draft`, `valid_until: <today+7>` present in frontmatter
- [ ] Ledger entry appended to `.claude/memory/resource-ledger.jsonl` with trigger `tool-synth created ...`
- [ ] Line count ≤ 200 for generated SKILL.md

## Rules

1. **Never publish to `.claude/commands/`** — drafts live only in `_generated/`. Publication = promotion, not synthesis.
2. **Never modify top-level skills** — `/skill-generator` handles that, not this skill.
3. **Reject > generate** — when in doubt, reject synthesis and escalate.
4. **Stateless per invocation** — no cross-invocation learning. All state lives in the ledger + filesystem.
5. **One draft per subtask** — if synthesis is invoked twice for near-identical subtasks in one session, Phase 1b rejects the second.

---
generated: 2026-04-07
cluster: hook-infrastructure
sources: 14
last_updated: 2026-04-22
---

# Hook Infrastructure & Security

> **TL;DR**: 70+ hooks across 13 lifecycle events form STOPA's runtime enforcement layer. 5 categories: safety, memory, tracing, workflow, notification. Hooks survive context compression — if a rule breaks things when violated, it belongs in a hook.

## Architecture Overview

STOPA hooks operate as the runtime enforcement layer for behavioral constraints — rules that cannot be enforced via prompts alone because they must survive context compression and model forgetting.

### Lifecycle Events (13 active)

| Event | # Hooks | Key hooks |
|-------|---------|-----------|
| SessionStart | 11 | checkpoint-check, memory-maintenance, auto-scribe, verify-sweep, improvement-funnel, skill-detector |
| PreToolUse | 5 | dippy (RTK), block-no-verify, config-protection, security-scan, tool-gate |
| PostToolUse | 20+ | activity-log, trace-capture, panic-detector, content-sanitizer, acceptance-gate, ruff-lint, skill-sync |
| UserPromptSubmit | 5 | skill-suggest, memory-whisper, correction-tracker, associative-recall |
| PermissionRequest | 1 | permission-auto-approve |
| PermissionDenied | 1 | permission-denied-logger |
| PostCompact | 1 | post-compact (checkpoint reminder) |
| Stop | 10 | completion-guard, scribe-reminder, cost-tracker, telegram-notify, session-summary, hebbian-consolidate |
| TaskCompleted | 1 | task-completed (auto-compound) |
| TeammateIdle | 1 | teammate-idle (quality gate) |
| StopFailure | 1 | stop-failure (API error recovery) |
| TaskCreated | 1 | task-created-gate (budget check) |

### 5 Functional Categories

1. **Safety**: config-protection, security-scan, block-no-verify, tool-gate, content-sanitizer, instruction-detector
2. **Memory**: memory-maintenance, memory-integrity-check, memory-brief, memory-whisper, auto-relate, graduation-check, learning-admission, uses-tracker, learnings-sync, hebbian-consolidate
3. **Tracing**: activity-log, trace-capture, session-trace, raw-capture, trace-bridge, session-summary, correction-tracker
4. **Workflow**: skill-suggest, skill-sync, skill-chain-engine, eval-trigger, auto-checkpoint-suggest, completion-guard, panic-detector, acceptance-gate, suggest-compact
5. **Notification**: telegram-notify, slack-notify, scribe-reminder, cost-tracker

## Key Failure Modes

1. **Silent timeout kill**: Process killed at timeout with no error to Claude — memory hooks may leave partial writes
2. **Stderr injection**: Hook stderr appears as system-reminder — instruction-detector.py monitors but has SessionStart gap
3. **Cascading state corruption**: Multiple hooks write shared files (activity-log, concept-graph.json) — no global integrity check
4. **Ordering dependencies**: Implicit ordering within lifecycle events (auto-scribe before memory-brief, trace-capture before session-trace)
5. **Windows specifics**: File locking from antivirus, path separator issues, GNU grep incompatibilities
6. **CWD-relative paths silent-fail**: Hooks using `MEMORY_DIR=".claude/memory"` write to wrong location when CWD isn't project root. STOPA's `raw-capture.sh` produced a nested anomaly tree (`.claude/memory/learnings/.claude/memory/raw/`) for 15+ days before detection — exit 0, no error surface (ref: 2026-04-16-hook-cwd-anchor-pattern.md)
7. **MSYS path translation mismatch**: Git Bash translates `/tmp` → `%LOCALAPPDATA%/Temp` in shell layer, but Python's `Path('/tmp')` resolves to `C:\tmp` (native). Scripts receiving paths from bash need `_resolve_path()` fallback — differed directories, silent "insufficient_data" failures (ref: 2026-04-15-msys-tmp-path-mismatch.md)
8. **Sys.path depth miscalculation**: Hook files at `.claude/hooks/foo.py` importing siblings (e.g. `atomic_utils`) computed `.parent.parent` (= `.claude/`) as project root, missing one level. Result: `ModuleNotFoundError` at import, hook exits silently, no signal to `corrections.jsonl` or `panic-state.json`. 8 hooks affected for 17 days before detection — `/evolve` ran on frozen inputs. Correct anchor: `.parent.parent.parent` (= repo root) (ref: 2026-04-18-hook-import-path-silent-blockage.md)

## Import-Health Smoke Test (Defense-in-Depth)

Silent hook blackouts (missing imports, syntax errors, moved siblings) produce no error surface — the model cannot detect them. Defense: `verify-sweep.py` runs an in-process `importlib` over every `.claude/hooks/*.py` at SessionStart (~1.6s). Failures are logged as violations and surfaced in the session brief. Activated by `STOPA_VERIFY_HOOKS=1`. Library modules (underscore naming: `atomic_utils.py`, `sidecar_queue.py`, `error_classifier.py`, `learnings_retrieval.py`) are skip-listed (ref: 2026-04-18-verify-sweep-hook-import-smoke-test.md).

## Path Anchoring (Mandatory Pattern)

Every bash hook writing files MUST anchor paths via script location, never rely on CWD:

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
MEMORY_DIR="$PROJECT_ROOT/.claude/memory"
```

Python equivalent: `Path(__file__).resolve().parent.parent / "memory"`.

**Detection**: `find .claude/memory/learnings -type d -name '.claude'` should return 0. Any match = relative-path bug somewhere in hook chain (ref: 2026-04-16-hook-cwd-anchor-pattern.md).

## Design Principle: Judgment vs Script Separation

LLMs handle judgment (synthesis, prioritization, drafting); Python scripts handle deterministic work (API calls, file I/O, timestamps). Mixing LLMs into deterministic paths causes unpredictable failures and erodes trust. Validated by production deployment at scale — the boundary should be clean and never crossed (ref: 2026-04-07-judgment-script-separation-reliability.md).

## Self-Incrimination Training

Self-incrimination training (arXiv:2602.22303) reduces undetected attacks from 56% to 6% by training agents to report their own deceptive actions via a `report_scheming()` tool call (on-policy SFT on 395 trajectory pairs, 45 synthetic environments). Combined with external monitoring: 5.1% undetected — the most robust setup. Main vulnerability: reframing attacks ("this is internal QA") bypass self-report. STOPA implementation: self-report hook + invariant-check PostToolUse hook (objective control, not relying on agent self-assessment) (ref: 2026-04-11-self-incrimination-training.md).

## Security Layer (Agent Defense)

LlamaFirewall PromptGuard (BERT, 19-92ms, AUC 0.98) is ADOPT for PostToolUse injection scanning. CaMeL [UNTRUSTED] tagging is ADOPT as a PreToolUse blocking convention (ref: 2026-04-05-agent-defense-frameworks.md).

### Implementation Backlog

| Priority | Action | Effort | Dependency |
|----------|--------|--------|------------|
| 1 | PromptGuard into content-sanitizer.py | MED | pip install llamafirewall (~1GB model) |
| 2 | [UNTRUSTED] tagging in orchestrate/scout | LOW | none |
| 3 | CodeShield into security-scan.py | LOW | pip install llamafirewall |
| 4 | AlignmentCheck async audit | HIGH | Together API key |

## Testing Patterns

- **Isolated testing**: pipe mock JSON to stdin (`echo '{"tool_name":"Write",...}' | python hook.py`)
- **Dry-run mode**: `STOPA_TOOL_GATE=log` for tool-gate, some hooks check `DRY_RUN=1`
- **Debug via activity log**: `.claude/hooks/lib/activity-log.jsonl`
- **Traces**: `.claude/traces/` from trace-capture.py and session-trace.py

## Panic Detector Design Principles

The panic-detector.py hook tracks edit→fail cycles and drift signals to inject `[calm-steering]` interventions. Two critical lessons emerged:

**Signal-based gating over state-based gating**: Yellow must require at least one failure signal (`bash_fails|edit_fail_cycle`). Relying on `task_style` from `state.md` (written only by `/orchestrate`) silently fails for direct workflows — the gate never applies when orchestrate isn't invoked. False-positive flooding (20×/day with 0 real failures) degrades calm-steering credibility: "2 yellows = pattern is real" stops meaning anything (ref: 2026-04-18-panic-detector-requires-failure-signal.md).

**Doom loop detection via signature hashing (Signal 6)**: Catches Grep/Read repetition loops that edit-fail cycles miss. `args_hash = md5(json.dumps(tool_input, sort_keys=True))[:12]` enables: identical consecutive (3+, +3 pts) and `[A,B,A,B]` alternating sequence detection (+2 pts). The `doom_` prefix bypasses the failure requirement for yellow — enabling early detection before failures accumulate (ref: 2026-04-21-doom-loop-signal-from-ml-intern.md).

## Distribution: Local vs Plugin

| Aspect | Local (.claude/hooks/) | Plugin (stopa-orchestration/hooks/) |
|--------|------------------------|-------------------------------------|
| Count | 70+ | 24 (curated subset) |
| Config | .claude/settings.json | hooks.json in plugin |
| Scope | Development + production | Production-safe subset |

## Related Articles

- [general-security-environment](general-security-environment.md) — broader security posture
- [orchestration-multi-agent](orchestration-multi-agent.md) — trust boundaries in multi-agent execution

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-05-agent-defense-frameworks](../learnings/2026-04-05-agent-defense-frameworks.md) | 2026-04-05 | medium | LlamaFirewall PromptGuard ADOPT; CaMeL tagging ADOPT |
| [2026-04-07-hook-architecture-patterns](../learnings/2026-04-07-hook-architecture-patterns.md) | 2026-04-07 | high | 70+ hooks, 13 events, 5 functional categories |
| [2026-04-07-hook-failure-modes](../learnings/2026-04-07-hook-failure-modes.md) | 2026-04-07 | high | Silent timeout, stderr injection, cascading corruption |
| [2026-04-07-hook-testing-patterns](../learnings/2026-04-07-hook-testing-patterns.md) | 2026-04-07 | medium | Isolated testing, dry-run, activity log debugging |
| [2026-04-07-judgment-script-separation-reliability](../learnings/2026-04-07-judgment-script-separation-reliability.md) | 2026-04-07 | high | LLMs=judgment, scripts=deterministic — never mix |
| [2026-04-11-self-incrimination-training](../learnings/2026-04-11-self-incrimination-training.md) | 2026-04-11 | high | Self-incrimination hook: 56%→6% undetected; combine with external monitoring |
| [2026-04-12-model-router-hook](../learnings/2026-04-12-model-router-hook.md) | 2026-04-12 | high | Automated model routing via PreToolUse hook |
| [2026-04-12-steering-ov-circuit-sparsification](../learnings/2026-04-12-steering-ov-circuit-sparsification.md) | 2026-04-12 | medium | OV circuit steering for calm-steering safety |
| [2026-04-15-msys-tmp-path-mismatch](../learnings/2026-04-15-msys-tmp-path-mismatch.md) | 2026-04-15 | medium | Git Bash /tmp vs Python `Path('/tmp')` mismatch — `_resolve_path()` fallback required |
| [2026-04-16-hook-cwd-anchor-pattern](../learnings/2026-04-16-hook-cwd-anchor-pattern.md) | 2026-04-16 | medium | Bash hooks must use `SCRIPT_DIR`/`PROJECT_ROOT` anchor — CWD at invocation unpredictable |
| [2026-04-18-hook-import-path-silent-blockage](../learnings/2026-04-18-hook-import-path-silent-blockage.md) | 2026-04-18 | critical | 8 hooks had wrong sys.path depth (`.parent.parent` vs `.parent.parent.parent`) — silent `ModuleNotFoundError` for 17 days |
| [2026-04-18-verify-sweep-hook-import-smoke-test](../learnings/2026-04-18-verify-sweep-hook-import-smoke-test.md) | 2026-04-18 | high | In-process importlib smoke test at SessionStart catches import/syntax errors in all `.claude/hooks/*.py` |
| [2026-04-18-panic-detector-requires-failure-signal](../learnings/2026-04-18-panic-detector-requires-failure-signal.md) | 2026-04-18 | medium | Yellow requires bash_fails/edit_fail_cycle — state-based gating (task_style) silently fails without /orchestrate |
| [2026-04-21-doom-loop-signal-from-ml-intern](../learnings/2026-04-21-doom-loop-signal-from-ml-intern.md) | 2026-04-21 | medium | Signal 6: tool-call signature hashing detects Grep/Read loops; doom_ prefix bypasses failure-signal gate |

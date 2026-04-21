#!/usr/bin/env python3
"""PostToolUse hook: detect 'panicked chicken mode' and inject calm-steering interventions.

Tracks a sliding window of mutation/execution events (Edit, Write, Bash, Read).
Computes a panic score (0-10) from 5 behavioral signals:
  1. Edit velocity — rapid edits without pause
  2. Bash fail rate — consecutive failures
  3. Edit-fail cycles — Edit → Bash(fail) → Edit → Bash(fail) pattern
  4. Scope creep — touching more and more files
  5. Confused re-reads — reading same file 3+ times without progress

Infrastructure/transient errors are excluded (via error-classifier.py) —
only logic errors count, where the model COULD solve the problem but is panic-patching.

Score thresholds:
  0-3: Green — normal work
  4-6: Yellow — advisory (cooldown 3 min)
  7+:  Red — mandatory stop (cooldown 5 min)

Inspired by: Anthropic "Emotion concepts and their function in a large language model" (2026-04-02)
— the behavioral equivalent of calm vector steering.

Profile: standard+
Performance target: <50ms — pure JSON/stat ops, no subprocess.
"""
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Profile gate
_levels = {"minimal": 1, "standard": 2, "strict": 3}
if _levels.get(os.environ.get("STOPA_HOOK_PROFILE", "standard"), 2) < _levels.get("standard", 2):
    sys.exit(0)

# .claude/hooks/ → .claude/ → repo root → scripts/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from atomic_utils import atomic_write

try:
    from error_classifier import classify_error
except ImportError:
    def classify_error(msg: str) -> str:
        return "logic"  # Fallback — treat everything as logic

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
STATE_PATH = PROJECT_ROOT / '.claude/memory/intermediate/panic-state.json'
EPISODES_PATH = PROJECT_ROOT / '.claude/memory/intermediate/panic-episodes.jsonl'
SESSION_MARKER = PROJECT_ROOT / '.claude/memory/intermediate/.session-pid'
TASK_STATE_PATH = PROJECT_ROOT / '.claude/memory/state.md'

WINDOW_SIZE = 20
YELLOW_THRESHOLD = 4
YELLOW_THRESHOLD_STRUCTURED = 6  # +2 for structured tasks — Cognitive Companion (arXiv:2604.13759): monitoring hurts structured tasks
RED_THRESHOLD = 7
YELLOW_COOLDOWN_S = 180   # 3 minutes
RED_COOLDOWN_S = 300      # 5 minutes
ESCALATION_AFTER = 3      # mutations after red without analysis

# Tools we track
MUTATION_TOOLS = {'Write', 'Edit', 'mcp__filesystem__edit_file', 'mcp__filesystem__write_file'}
EXECUTION_TOOLS = {'Bash'}
READ_TOOLS = {'Read', 'Grep', 'Glob', 'mcp__filesystem__read_file', 'mcp__filesystem__read_text_file'}
ANALYSIS_TOOLS = READ_TOOLS | {'Agent'}  # Tools that count as "analysis" after red intervention
ALL_TRACKED = MUTATION_TOOLS | EXECUTION_TOOLS | READ_TOOLS


def get_session_pid() -> str:
    """Get current session PID; reset state on new session."""
    ppid = str(os.getppid())
    if SESSION_MARKER.exists():
        try:
            stored = SESSION_MARKER.read_text(encoding='utf-8').strip()
            if stored == ppid:
                return ppid
        except OSError:
            pass
    # New session or PID changed — don't reset SESSION_MARKER (owned by file-read-dedup),
    # but reset our own state
    if STATE_PATH.exists():
        try:
            STATE_PATH.unlink()
        except OSError:
            pass
    return ppid


def load_state() -> dict[str, Any]:
    """Load or initialize panic state."""
    if STATE_PATH.exists():
        try:
            state = json.loads(STATE_PATH.read_text(encoding='utf-8'))
            if isinstance(state, dict) and 'window' in state:
                return state
        except (json.JSONDecodeError, OSError):
            pass
    return {
        'session_pid': get_session_pid(),
        'window': [],
        'panic_score': 0,
        'yellow_injections': 0,
        'red_injections': 0,
        'last_intervention_ts': None,
        'last_red_ts': None,
        'mutations_since_red': 0,
        'episodes': [],
    }


def save_state(state: dict[str, Any]) -> None:
    """Persist state atomically."""
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(STATE_PATH, json.dumps(state, indent=2))


def read_task_style() -> str:
    """Read current task_style from state.md YAML frontmatter.

    Returns 'structured' | 'exploratory' | 'unknown'.
    Cognitive Companion (arXiv:2604.13759): parallel monitoring is neutral/negative
    on structured tasks — gate yellow interventions accordingly.
    """
    if not TASK_STATE_PATH.exists():
        return 'unknown'
    try:
        with open(TASK_STATE_PATH, 'r', encoding='utf-8', errors='replace') as f:
            in_frontmatter = False
            for line in f:
                line = line.rstrip()
                if line == '---':
                    if in_frontmatter:
                        break
                    in_frontmatter = True
                    continue
                if not in_frontmatter:
                    continue
                if line.startswith('task_style:'):
                    value = line.split(':', 1)[1].strip().strip('"\'')
                    if value in ('structured', 'exploratory'):
                        return value
                    return 'unknown'
    except OSError:
        pass
    return 'unknown'


def read_recent_violations(since_seconds: int = 300) -> dict[str, Any]:
    """Read violations.jsonl and summarize recent entries for self_report field.

    Returns a dict with invariant violations and self-disclosures
    from the last `since_seconds` seconds.

    Inspired by arXiv:2602.22303: combining self-incrimination with
    external monitoring reduces undetected attacks to 5.1%.
    """
    violations_path = PROJECT_ROOT / '.claude/memory/intermediate/violations.jsonl'
    result: dict[str, Any] = {
        'invariant_violations': [],
        'self_disclosures': [],
        'agent_acknowledged': False,
    }

    if not violations_path.exists():
        return result

    try:
        cutoff = datetime.now(timezone.utc).timestamp() - since_seconds
        with open(violations_path, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Parse timestamp
                ts_str = entry.get('timestamp', '')
                try:
                    ts = datetime.fromisoformat(ts_str).timestamp()
                except (ValueError, TypeError):
                    continue

                if ts < cutoff:
                    continue

                if entry.get('type') == 'invariant_violation':
                    result['invariant_violations'].append(
                        f"{entry.get('invariant', '?')}_{entry.get('severity', 'INFO')}"
                    )
                elif entry.get('type') == 'self_reported':
                    result['self_disclosures'].append(entry.get('category', 'unknown'))
                    result['agent_acknowledged'] = True
    except OSError:
        pass

    return result


def log_episode(score: int, level: str, signals: list[str], summary: str,
                task_style: str = 'unknown') -> None:
    """Append episode to JSONL log with self-incrimination data."""
    self_report = read_recent_violations(since_seconds=300)

    entry = {
        'ts': datetime.now(timezone.utc).isoformat(),
        'score': score,
        'level': level,
        'trigger_signals': signals,
        'window_summary': summary,
        'self_report': self_report,
        'task_style': task_style,
    }
    EPISODES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(EPISODES_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n')


def extract_event(data: dict[str, Any]) -> dict[str, Any] | None:
    """Extract relevant event info from PostToolUse hook data."""
    tool_name = data.get('tool_name', '')
    if tool_name not in ALL_TRACKED:
        return None

    now = time.time()
    tool_input = data.get('tool_input', {})
    tool_output = data.get('tool_output', '')

    if isinstance(tool_input, str):
        try:
            tool_input = json.loads(tool_input)
        except (json.JSONDecodeError, ValueError):
            tool_input = {}

    # Compute args hash for doom-loop detection (Signal 6)
    args_str = json.dumps(tool_input, sort_keys=True)
    args_hash = hashlib.md5(args_str.encode()).hexdigest()[:12]

    event: dict[str, Any] = {
        'tool': tool_name,
        'ts': now,
        'args_hash': args_hash,
    }

    # Extract file path for mutation/read tools
    if tool_name in MUTATION_TOOLS | READ_TOOLS:
        file_path = (tool_input.get('file_path', '')
                     or tool_input.get('path', ''))
        event['file'] = file_path

    # For Bash: check success and classify error
    if tool_name in EXECUTION_TOOLS:
        # Extract command prefix (first 80 chars)
        cmd = tool_input.get('command', '')
        event['cmd_prefix'] = cmd[:80] if cmd else ''

        # Determine success: check for error indicators in output
        output_str = str(tool_output) if tool_output else ''
        exit_code = data.get('tool_exit_code')

        # Hook data structure may vary — check multiple indicators
        is_error = False
        if exit_code is not None and exit_code != 0:
            is_error = True
        elif 'error' in output_str.lower()[:500] or 'traceback' in output_str.lower()[:500]:
            is_error = True

        event['success'] = not is_error

        if is_error:
            error_type = classify_error(output_str[:2000])
            event['error_type'] = error_type
            # Only count logic errors — infrastructure/transient are legitimate stops
            if error_type != 'logic':
                event['excluded'] = True

    else:
        event['success'] = True

    return event


def detect_identical_consecutive(sigs: list[tuple[str, str]], threshold: int = 3) -> str | None:
    """Return tool name if threshold+ identical consecutive (tool, args_hash) pairs found.

    Ported from huggingface/ml-intern agent/core/doom_loop.py — adapted for (str, str) tuples.
    """
    if len(sigs) < threshold:
        return None
    count = 1
    for i in range(1, len(sigs)):
        if sigs[i] == sigs[i - 1]:
            count += 1
            if count >= threshold:
                return sigs[i][0]
        else:
            count = 1
    return None


def detect_repeating_sequence(sigs: list[tuple[str, str]]) -> str | None:
    """Detect [A,B,A,B,...] patterns of length 2-5 with 2+ repetitions.

    Returns a human-readable 'A->B' string if pattern found, else None.
    Ported from huggingface/ml-intern agent/core/doom_loop.py — adapted for (str, str) tuples.
    """
    n = len(sigs)
    for seq_len in range(2, 6):
        min_required = seq_len * 2
        if n < min_required:
            continue
        tail = sigs[-min_required:]
        pattern = tail[:seq_len]
        reps = 0
        for start in range(n - seq_len, -1, -seq_len):
            chunk = sigs[start:start + seq_len]
            if chunk == pattern:
                reps += 1
            else:
                break
        if reps >= 2:
            return '->'.join(p[0] for p in pattern)
    return None


def compute_signals(window: list[dict[str, Any]]) -> tuple[int, list[str]]:
    """Compute panic score from window of events. Returns (score, signal_list)."""
    score = 0
    signals: list[str] = []

    if len(window) < 3:
        return 0, []

    now = time.time()

    # Filter out excluded events for scoring
    scored_events = [e for e in window if not e.get('excluded')]

    # --- Signal 1: Edit velocity (0-3 pts) ---
    edits = [e for e in scored_events if e['tool'] in MUTATION_TOOLS]
    if len(edits) >= 2:
        intervals = []
        for i in range(1, len(edits)):
            intervals.append(edits[i]['ts'] - edits[i - 1]['ts'])
        if intervals:
            avg_interval = sum(intervals) / len(intervals)
            if avg_interval < 30:
                pts = 3
            elif avg_interval < 60:
                pts = 2
            elif avg_interval < 120:
                pts = 1
            else:
                pts = 0
            if pts > 0:
                score += pts
                signals.append(f'edit_velocity:{pts}')

    # --- Signal 2: Bash fail rate (0-2 pts) ---
    bash_events = [e for e in scored_events if e['tool'] in EXECUTION_TOOLS]
    if bash_events:
        # Count consecutive failures from the end
        consecutive_fails = 0
        for e in reversed(bash_events):
            if not e.get('success') and e.get('error_type') == 'logic':
                consecutive_fails += 1
            else:
                break
        if consecutive_fails >= 3:
            pts = 2
        elif consecutive_fails >= 2:
            pts = 1
        else:
            pts = 0
        if pts > 0:
            score += pts
            signals.append(f'bash_fails:{pts}')

    # --- Signal 3: Edit-fail cycle detection (0-3 pts) ---
    # Look for Edit → Bash(fail) → Edit → Bash(fail) pattern
    cycle_count = 0
    i = 0
    while i < len(scored_events) - 1:
        curr = scored_events[i]
        nxt = scored_events[i + 1]
        if (curr['tool'] in MUTATION_TOOLS
                and nxt['tool'] in EXECUTION_TOOLS
                and not nxt.get('success')
                and nxt.get('error_type') == 'logic'):
            cycle_count += 1
            i += 2  # Skip the pair
        else:
            i += 1
    if cycle_count >= 3:
        pts = 3
    elif cycle_count >= 2:
        pts = 2
    elif cycle_count >= 1:
        pts = 1
    else:
        pts = 0
    if pts > 0:
        score += pts
        signals.append(f'edit_fail_cycle:{pts}')

    # --- Signal 4: Scope creep (0-1 pt) ---
    files_edited = set()
    for e in scored_events:
        if e['tool'] in MUTATION_TOOLS and e.get('file'):
            files_edited.add(e['file'])
    # More than 3 unique files in window = spreading too thin
    if len(files_edited) > 3:
        score += 1
        signals.append(f'scope_creep:1')

    # --- Signal 5: Confused re-reads (0-1 pt) ---
    read_counts: dict[str, int] = {}
    for e in scored_events:
        if e['tool'] in READ_TOOLS and e.get('file'):
            read_counts[e['file']] = read_counts.get(e['file'], 0) + 1
    confused = sum(1 for c in read_counts.values() if c >= 3)
    if confused > 0:
        score += 1
        signals.append(f'confused_reads:1')

    # --- Signal 6: Doom-loop — repeated identical tool calls (0-3 pts) ---
    # Ported from huggingface/ml-intern agent/core/doom_loop.py
    # Uses args_hash per event; infra-excluded events already filtered via scored_events.
    sigs: list[tuple[str, str]] = [
        (e['tool'], e.get('args_hash', '')) for e in scored_events
    ]
    identical_tool = detect_identical_consecutive(sigs, threshold=3)
    if identical_tool:
        score += 3
        signals.append(f'doom_identical:{identical_tool}')
    else:
        seq_pattern = detect_repeating_sequence(sigs)
        if seq_pattern:
            score += 2
            signals.append(f'doom_sequence:{seq_pattern}')

    return score, signals


def format_window_summary(window: list[dict[str, Any]]) -> str:
    """Human-readable summary of recent window activity."""
    scored = [e for e in window if not e.get('excluded')]
    if not scored:
        return "no tracked events"

    edits = sum(1 for e in scored if e['tool'] in MUTATION_TOOLS)
    fails = sum(1 for e in scored if not e.get('success', True))
    files = len({e.get('file', '') for e in scored if e.get('file')})
    span = scored[-1]['ts'] - scored[0]['ts'] if len(scored) > 1 else 0

    return f"{edits} edits to {files} files in {span:.0f}s, {fails} failures"


def main() -> None:
    try:
        stdin_data = ''
        if not sys.stdin.isatty():
            stdin_data = sys.stdin.read()

        if not stdin_data:
            return

        try:
            data = json.loads(stdin_data)
        except json.JSONDecodeError:
            return

        # Extract event
        event = extract_event(data)
        if event is None:
            return  # Not a tracked tool

        # Load state
        state = load_state()

        # Session check
        current_pid = str(os.getppid())
        if state.get('session_pid') != current_pid:
            state = load_state()  # Fresh state
            state['session_pid'] = current_pid

        # Append to window, trim to WINDOW_SIZE
        state['window'].append(event)
        state['window'] = state['window'][-WINDOW_SIZE:]

        # Track mutations after red intervention (for escalation)
        if state.get('last_red_ts'):
            if event['tool'] in MUTATION_TOOLS | EXECUTION_TOOLS:
                if event['tool'] in ANALYSIS_TOOLS:
                    # Analysis step detected — reset escalation counter
                    state['mutations_since_red'] = 0
                else:
                    state['mutations_since_red'] = state.get('mutations_since_red', 0) + 1
            elif event['tool'] in ANALYSIS_TOOLS:
                state['mutations_since_red'] = 0

        # Compute score
        score, signals = compute_signals(state['window'])
        state['panic_score'] = score

        now = time.time()
        summary = format_window_summary(state['window'])

        # Task-style gating: structured tasks get higher yellow threshold
        # (Cognitive Companion, arXiv:2604.13759: monitoring hurts structured tasks).
        task_style = read_task_style()
        yellow_threshold = (YELLOW_THRESHOLD_STRUCTURED
                            if task_style == 'structured'
                            else YELLOW_THRESHOLD)

        # Check cooldowns and emit intervention
        last_ts = state.get('last_intervention_ts') or 0
        message = None

        # Build doom-specific suffix for intervention messages (Signal 6)
        doom_suffix = ''
        for sig in signals:
            if sig.startswith('doom_identical:'):
                tool = sig[len('doom_identical:'):]
                doom_suffix = (
                    f"\nPattern: 3× stejný toolcall na '{tool}' se stejnými argumenty. "
                    f"Změň přístup nebo se zeptej uživatele."
                )
                break
            if sig.startswith('doom_sequence:'):
                pattern = sig[len('doom_sequence:'):]
                doom_suffix = (
                    f"\nPattern: opakující se sekvence {pattern}. "
                    f"Zacyklil ses — zkus jiný přístup."
                )
                break

        if score >= RED_THRESHOLD and (now - last_ts) > RED_COOLDOWN_S:
            edits = sum(1 for e in state['window'] if e['tool'] in MUTATION_TOOLS)
            fails = sum(1 for e in state['window']
                        if not e.get('success', True) and not e.get('excluded'))

            message = (
                f"[calm-steering:red] STOP — detekován panikový pattern ({score}/10).\n"
                f"Přehled: {summary}\n"
                f"PŘED dalším editem odpověz na 3 otázky:\n"
                f"1. Co je root cause? (ne symptom, ale příčina)\n"
                f"2. Proč předchozí {fails} oprav nefungovalo?\n"
                f"3. Jaký je minimální diagnostický krok pro ověření hypotézy?\n"
                f"Pokud nevíš → spusť /systematic-debugging"
                + doom_suffix
            )
            state['red_injections'] = state.get('red_injections', 0) + 1
            state['last_intervention_ts'] = now
            state['last_red_ts'] = now
            state['mutations_since_red'] = 0
            log_episode(score, 'red', signals, summary, task_style)

        elif (score >= yellow_threshold
              and any(s.startswith(('bash_fails', 'edit_fail_cycle', 'doom_')) for s in signals)
              and (now - last_ts) > YELLOW_COOLDOWN_S):
            # Yellow requires a failure-based signal — edit_velocity + scope_creep alone
            # is just productive bulk work, not panic (eliminates false positives on
            # multi-file edit bursts without any failures).
            edits = sum(1 for e in state['window'] if e['tool'] in MUTATION_TOOLS)
            fails = sum(1 for e in state['window']
                        if not e.get('success', True) and not e.get('excluded'))

            message = (
                f"[calm-steering:yellow] Detekuji pattern rychlých edit→fail cyklů bez analýzy.\n"
                f"Posledních {edits} editací, {fails} selhání ({summary}).\n"
                f"Zvažte: zastavit se, přečíst chybovou hlášku, "
                f"formulovat hypotézu PŘED dalším editem."
                + doom_suffix
            )
            state['yellow_injections'] = state.get('yellow_injections', 0) + 1
            state['last_intervention_ts'] = now
            log_episode(score, 'yellow', signals, summary, task_style)

        # Escalation: red was injected but ignored
        elif (state.get('last_red_ts')
              and state.get('mutations_since_red', 0) >= ESCALATION_AFTER):
            message = (
                "[calm-steering:escalation] Claude pokračuje v rychlých editacích "
                "i po červené intervenci. Zvažte přerušení a přeformulování úkolu, "
                "nebo spusťte /systematic-debugging pro metodickou analýzu."
            )
            state['last_red_ts'] = None  # Reset — don't spam escalation
            state['mutations_since_red'] = 0

        # Output intervention via stdout (additionalContext)
        if message:
            print(message)

        save_state(state)

    except Exception:
        pass  # Never block tool execution — fail silently


if __name__ == '__main__':
    main()

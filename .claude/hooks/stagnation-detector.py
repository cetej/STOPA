#!/usr/bin/env python3
"""PostToolUse hook: detect iteration stagnation in autoloop/self-evolve/autoresearch.

Monitors TSV result files and optstate JSON for plateau patterns.
When stagnation is detected, injects [stagnation-steering] messages
to force strategy pivots — analogous to CORAL's heartbeat mechanism.

Unlike panic-detector.py (which catches edit→fail desperation),
this hook catches PRODUCTIVE-LOOKING but UNPRODUCTIVE iteration:
agent keeps iterating, no crashes, but zero improvement.

Signals:
  1. Consecutive discards — N iterations discarded in a row
  2. Score plateau — delta < threshold across N iterations
  3. Strategy repetition — same strategy type used 3+ times without gain

Thresholds:
  0-2 discards: Green — normal exploration
  3 discards:   Yellow — advisory (suggest strategy pivot)
  4+ discards:  Red — force radical shift or consolidation

CORAL reference: arXiv:2604.01658 — heartbeat-triggered intervention
Profile: standard+
Performance target: <30ms — pure file stat/read, no subprocess.
"""
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

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from atomic_utils import atomic_write

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

STATE_PATH = Path('.claude/memory/intermediate/stagnation-state.json')
EPISODES_PATH = Path('.claude/memory/intermediate/stagnation-episodes.jsonl')

# TSV result files from iterative skills
TSV_PATTERNS = [
    '.claude/memory/intermediate/autoloop-results.tsv',
    '.claude/memory/intermediate/autoresearch-results.tsv',
]
# Optstate files for velocity tracking
OPTSTATE_DIR = Path('.claude/memory/optstate')

# Thresholds
CONSECUTIVE_DISCARD_YELLOW = 3
CONSECUTIVE_DISCARD_RED = 4
PLATEAU_WINDOW = 4          # iterations to check for score plateau
PLATEAU_DELTA_THRESHOLD = 0.01  # < 1% relative improvement = plateau
STRATEGY_REPEAT_THRESHOLD = 3   # same strategy N times without gain
YELLOW_COOLDOWN_S = 120     # 2 minutes
RED_COOLDOWN_S = 240        # 4 minutes

# Only fire on tools that indicate an iteration step just happened
ITERATION_INDICATORS = {'Bash', 'Write', 'Edit'}


def load_state() -> dict[str, Any]:
    """Load or initialize stagnation state."""
    if STATE_PATH.exists():
        try:
            state = json.loads(STATE_PATH.read_text(encoding='utf-8'))
            if isinstance(state, dict) and 'session_pid' in state:
                return state
        except (json.JSONDecodeError, OSError):
            pass
    return {
        'session_pid': str(os.getppid()),
        'last_tsv_lines': {},      # {filepath: line_count} — detect new entries
        'last_intervention_ts': 0,
        'last_red_ts': 0,
        'yellow_count': 0,
        'red_count': 0,
    }


def save_state(state: dict[str, Any]) -> None:
    """Persist state atomically."""
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(STATE_PATH, json.dumps(state, indent=2))


def log_episode(level: str, signal: str, detail: str) -> None:
    """Append episode to JSONL log."""
    entry = {
        'ts': datetime.now(timezone.utc).isoformat(),
        'level': level,
        'signal': signal,
        'detail': detail,
    }
    EPISODES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(EPISODES_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n')


def read_tsv_tail(path: Path, n: int = 8) -> list[dict[str, str]]:
    """Read last N lines of a TSV file, parse into dicts.

    Expected TSV columns: iteration, status, score, delta, strategy, timestamp
    (autoloop format). Adapts if columns differ.
    """
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding='utf-8', errors='replace').strip().split('\n')
        if len(lines) < 2:  # header + at least 1 data row
            return []

        header = lines[0].split('\t')
        data_lines = lines[1:]
        tail = data_lines[-n:]

        result = []
        for line in tail:
            fields = line.split('\t')
            row = {}
            for i, col in enumerate(header):
                row[col.strip().lower()] = fields[i].strip() if i < len(fields) else ''
            result.append(row)
        return result
    except OSError:
        return []


def check_consecutive_discards(rows: list[dict[str, str]]) -> tuple[int, str]:
    """Count consecutive discards/reverts from the tail.

    Returns (count, detail_string).
    """
    if not rows:
        return 0, ''

    count = 0
    for row in reversed(rows):
        status = row.get('status', '').lower()
        if status in ('discard', 'revert', 'crash', 'fail'):
            count += 1
        else:
            break

    detail = f"{count} consecutive non-keep results"
    return count, detail


def check_score_plateau(rows: list[dict[str, str]]) -> tuple[bool, str]:
    """Check if scores are plateauing (< threshold relative change).

    Returns (is_plateau, detail_string).
    """
    if len(rows) < PLATEAU_WINDOW:
        return False, ''

    window = rows[-PLATEAU_WINDOW:]
    scores = []
    for row in window:
        score_str = row.get('score', '') or row.get('best_score', '')
        try:
            scores.append(float(score_str))
        except (ValueError, TypeError):
            continue

    if len(scores) < PLATEAU_WINDOW:
        return False, ''

    # Check relative delta across window
    first, last = scores[0], scores[-1]
    if first == 0:
        # Avoid division by zero — use absolute delta
        delta = abs(last - first)
        is_plateau = delta < 0.001
    else:
        delta = abs(last - first) / abs(first)
        is_plateau = delta < PLATEAU_DELTA_THRESHOLD

    if is_plateau:
        detail = f"Score plateau: {scores[0]:.4f} → {scores[-1]:.4f} (delta {delta:.4f}) across {PLATEAU_WINDOW} iterations"
        return True, detail

    return False, ''


def check_strategy_repetition(rows: list[dict[str, str]]) -> tuple[bool, str]:
    """Check if same strategy is being repeated without improvement.

    Returns (is_repeating, detail_string).
    """
    if len(rows) < STRATEGY_REPEAT_THRESHOLD:
        return False, ''

    tail = rows[-STRATEGY_REPEAT_THRESHOLD:]
    strategies = [r.get('strategy', '').lower() for r in tail if r.get('strategy')]
    if len(strategies) < STRATEGY_REPEAT_THRESHOLD:
        return False, ''

    # All same strategy?
    if len(set(strategies)) == 1:
        # And none of them kept?
        statuses = [r.get('status', '').lower() for r in tail]
        if all(s in ('discard', 'revert', 'crash', 'fail') for s in statuses):
            detail = f"Strategy '{strategies[0]}' repeated {len(strategies)}× without improvement"
            return True, detail

    return False, ''


def find_active_tsv() -> Path | None:
    """Find the most recently modified TSV result file."""
    candidates = []
    for pattern in TSV_PATTERNS:
        p = Path(pattern)
        if p.exists():
            candidates.append((p.stat().st_mtime, p))

    # Also check for any *-results.tsv in intermediate/
    intermediate = Path('.claude/memory/intermediate')
    if intermediate.exists():
        for f in intermediate.glob('*-results.tsv'):
            if f not in [c[1] for c in candidates]:
                candidates.append((f.stat().st_mtime, f))

    if not candidates:
        return None

    # Return most recently modified
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


def has_new_entries(tsv_path: Path, state: dict) -> bool:
    """Check if TSV has new entries since last check."""
    key = str(tsv_path)
    try:
        current_lines = len(tsv_path.read_text(encoding='utf-8', errors='replace').strip().split('\n'))
    except OSError:
        return False

    last_lines = state.get('last_tsv_lines', {}).get(key, 0)

    if current_lines > last_lines:
        if 'last_tsv_lines' not in state:
            state['last_tsv_lines'] = {}
        state['last_tsv_lines'][key] = current_lines
        return True

    return False


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

        tool_name = data.get('tool_name', '')
        if tool_name not in ITERATION_INDICATORS:
            return

        # Find active TSV
        tsv_path = find_active_tsv()
        if tsv_path is None:
            return  # No iterative skill running

        # Load state
        state = load_state()

        # Session check
        current_pid = str(os.getppid())
        if state.get('session_pid') != current_pid:
            state = {
                'session_pid': current_pid,
                'last_tsv_lines': {},
                'last_intervention_ts': 0,
                'last_red_ts': 0,
                'yellow_count': 0,
                'red_count': 0,
            }

        # Only check if TSV has new entries (avoid re-firing on same data)
        if not has_new_entries(tsv_path, state):
            save_state(state)
            return

        # Read tail of TSV
        rows = read_tsv_tail(tsv_path, n=8)
        if len(rows) < 2:
            save_state(state)
            return

        # Run checks
        discard_count, discard_detail = check_consecutive_discards(rows)
        is_plateau, plateau_detail = check_score_plateau(rows)
        is_repeating, repeat_detail = check_strategy_repetition(rows)

        now = time.time()
        last_ts = state.get('last_intervention_ts', 0)
        message = None

        # Red: 4+ consecutive discards OR plateau + repetition
        if discard_count >= CONSECUTIVE_DISCARD_RED and (now - last_ts) > RED_COOLDOWN_S:
            signals = [discard_detail]
            if is_plateau:
                signals.append(plateau_detail)
            if is_repeating:
                signals.append(repeat_detail)

            message = (
                f"[stagnation-steering:red] Detekováno {discard_count} po sobě neúspěšných iterací.\n"
                f"{chr(10).join(signals)}\n"
                f"CORAL heartbeat — POVINNÉ kroky:\n"
                f"1. PAUSE — nezačínej další iteraci\n"
                f"2. Reflexion: Co jsem zkoušel? Proč to nefungovalo? Co zkusit ZÁSADNĚ jinak?\n"
                f"3. Přepni na NEJMÉNĚ použitou strategii, nebo zjednodušuj (priority 5-6)\n"
                f"4. Zapiš reflexion do run diary: 'Heartbeat: forcing radical shift'"
            )
            state['red_count'] = state.get('red_count', 0) + 1
            state['last_intervention_ts'] = now
            state['last_red_ts'] = now
            log_episode('red', 'consecutive_discards', discard_detail)

        # Yellow: 3 consecutive discards OR pure plateau
        elif (discard_count >= CONSECUTIVE_DISCARD_YELLOW or (is_plateau and is_repeating)) \
                and (now - last_ts) > YELLOW_COOLDOWN_S:
            signals = []
            if discard_count >= CONSECUTIVE_DISCARD_YELLOW:
                signals.append(discard_detail)
            if is_plateau:
                signals.append(plateau_detail)
            if is_repeating:
                signals.append(repeat_detail)

            message = (
                f"[stagnation-steering:yellow] Iterační smyčka stagnuje.\n"
                f"{chr(10).join(signals)}\n"
                f"Zvažte: změnu strategie, zjednodušení přístupu, "
                f"nebo skill consolidation (extrahuj co funguje do bullet pointů)."
            )
            state['yellow_count'] = state.get('yellow_count', 0) + 1
            state['last_intervention_ts'] = now
            log_episode('yellow', 'stagnation', '; '.join(signals))

        if message:
            print(message)

        save_state(state)

    except Exception:
        pass  # Never block tool execution


if __name__ == '__main__':
    main()

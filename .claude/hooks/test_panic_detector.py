#!/usr/bin/env python3
"""Tests for panic-detector.py Signal 6 (doom-loop detection).

Four test cases from T-2026-04-21-001 acceptance criteria:
1. identical consecutive triggers
2. repeating sequence triggers
3. no false positive on productive work
4. infra errors excluded from doom
"""
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

# Load panic-detector module (hyphen in name requires importlib)
_hook_path = Path(__file__).resolve().parent / 'panic-detector.py'
_spec = importlib.util.spec_from_file_location('panic_detector', _hook_path)
_mod = importlib.util.module_from_spec(_spec)
sys.modules['panic_detector'] = _mod
_spec.loader.exec_module(_mod)

from panic_detector import (  # noqa: E402
    detect_identical_consecutive,
    detect_repeating_sequence,
    compute_signals,
    MUTATION_TOOLS,
    READ_TOOLS,
    EXECUTION_TOOLS,
)

PASS_COUNT = 0
FAIL_COUNT = 0


def make_hash(args_dict: dict) -> str:
    args_str = json.dumps(args_dict, sort_keys=True)
    return hashlib.md5(args_str.encode()).hexdigest()[:12]


def make_event(tool: str, args_dict: dict, ts_offset: float = 0.0,
               success: bool = True, excluded: bool = False,
               error_type: str = 'logic') -> dict:
    """Build a minimal event dict as compute_signals expects."""
    event: dict = {
        'tool': tool,
        'ts': time.time() - 3600 + ts_offset,
        'args_hash': make_hash(args_dict),
        'success': success,
    }
    if not success:
        event['error_type'] = error_type
    if excluded:
        event['excluded'] = True
    if tool in READ_TOOLS or tool in MUTATION_TOOLS:
        event['file'] = args_dict.get('file_path', args_dict.get('path', 'test.py'))
    if tool in EXECUTION_TOOLS:
        event['cmd_prefix'] = args_dict.get('command', '')[:80]
    return event


def assert_true(condition: bool, label: str, detail: str = '') -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        print(f'  PASS: {label}')
        PASS_COUNT += 1
    else:
        print(f'  FAIL: {label}' + (f' — {detail}' if detail else ''))
        FAIL_COUNT += 1


def test_identical_consecutive_triggers() -> None:
    """TC1: 3 events with tool='Grep' + same args_hash → doom_identical:Grep, +3 pts."""
    print('\nTC1: identical consecutive triggers')
    same_args = {'pattern': 'def foo', 'path': 'src/'}
    events = [make_event('Grep', same_args, ts_offset=i * 10.0) for i in range(3)]
    score, signals = compute_signals(events)
    assert_true(
        'doom_identical:Grep' in signals,
        "doom_identical:Grep in signals",
        f"signals={signals}"
    )
    assert_true(
        score >= 3,
        f"score >= 3 (got {score})",
        f"score={score}"
    )


def test_repeating_sequence_triggers() -> None:
    """TC2: [Read,Bash,Read,Bash,Read,Bash] with identical args → doom_sequence:Read->Bash, +2."""
    print('\nTC2: repeating sequence triggers')
    read_args = {'file_path': 'app.py'}
    bash_args = {'command': 'python -m pytest tests/'}
    events = []
    for i in range(3):
        events.append(make_event('Read', read_args, ts_offset=i * 20.0))
        events.append(make_event('Bash', bash_args, ts_offset=i * 20.0 + 10.0))
    score, signals = compute_signals(events)
    doom_seq = [s for s in signals if s.startswith('doom_sequence:')]
    assert_true(
        len(doom_seq) > 0,
        "doom_sequence:* in signals",
        f"signals={signals}"
    )
    if doom_seq:
        assert_true(
            'Read->Bash' in doom_seq[0],
            f"pattern is Read->Bash (got {doom_seq[0]})",
            f"doom_seq={doom_seq}"
        )
    assert_true(
        score >= 2,
        f"score >= 2 (got {score})",
        f"score={score}"
    )


def test_no_false_positive_productive_work() -> None:
    """TC3: 5 distinct Read+Edit pairs on different files → NO doom_* signal."""
    print('\nTC3: no false positive on productive work')
    events = []
    for i in range(5):
        events.append(make_event('Read', {'file_path': f'src/module_{i}.py'}, ts_offset=i * 60.0))
        events.append(make_event('Edit', {'file_path': f'src/module_{i}.py'}, ts_offset=i * 60.0 + 30.0))
    score, signals = compute_signals(events)
    doom_signals = [s for s in signals if s.startswith('doom_')]
    assert_true(
        len(doom_signals) == 0,
        "no doom_* signals on productive diverse work",
        f"signals={signals}, doom_signals={doom_signals}"
    )


def test_infra_errors_excluded_from_doom() -> None:
    """TC4: 3 identical Bash with ENOENT (excluded=True) → NO doom signal."""
    print('\nTC4: infra errors excluded from doom')
    bash_args = {'command': 'cat /nonexistent/path.txt'}
    events = [
        make_event('Bash', bash_args, ts_offset=i * 5.0, success=False,
                   excluded=True, error_type='resource')
        for i in range(3)
    ]
    score, signals = compute_signals(events)
    doom_signals = [s for s in signals if s.startswith('doom_')]
    assert_true(
        len(doom_signals) == 0,
        "no doom_* signals when events are infra-excluded",
        f"signals={signals}, doom_signals={doom_signals}"
    )


if __name__ == '__main__':
    print('=== panic-detector Signal 6 tests ===')
    test_identical_consecutive_triggers()
    test_repeating_sequence_triggers()
    test_no_false_positive_productive_work()
    test_infra_errors_excluded_from_doom()

    print(f'\nResults: {PASS_COUNT} passed, {FAIL_COUNT} failed')
    sys.exit(0 if FAIL_COUNT == 0 else 1)

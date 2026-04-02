#!/usr/bin/env python3
"""Parse JSONL harness traces and compute quality metrics.

Usage:
    python trace-parser.py <trace.jsonl>                  # Single trace analysis
    python trace-parser.py <trace1.jsonl> <trace2.jsonl>  # Diff two traces
    python trace-parser.py --validate <trace.jsonl>       # Structural validation only

Output: JSON with metrics, validation results, and (optionally) diff.
"""

import json
import sys
from pathlib import Path


def parse_trace(path: str) -> list[dict]:
    """Read JSONL trace file into list of records."""
    records = []
    with open(path, encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"WARN: Line {line_num} invalid JSON: {e}", file=sys.stderr)
    return records


def validate_structure(records: list[dict]) -> list[dict]:
    """Run structural validation checks on trace records.

    Returns list of check results: {check, status, detail}
    """
    checks = []

    # Check 1: Header record
    has_header = any(
        r.get("phase") == 0 and r.get("event") == "start" for r in records
    )
    checks.append({
        "check": "header_present",
        "status": "PASS" if has_header else "FAIL",
        "flag": None if has_header else "INCOMPLETE",
    })

    # Check 2: Final record
    has_final = any(
        r.get("phase") == "final" and r.get("event") == "end" for r in records
    )
    checks.append({
        "check": "final_present",
        "status": "PASS" if has_final else "FAIL",
        "flag": None if has_final else "TRUNCATED",
    })

    # Check 3: No phase gaps
    phase_nums = sorted(
        r["phase"] for r in records
        if isinstance(r.get("phase"), (int, float))
        and r.get("phase") not in (0, 0.5)
        and r.get("event") != "end"
    )
    has_gaps = False
    for i in range(1, len(phase_nums)):
        if phase_nums[i] - phase_nums[i - 1] > 1:
            has_gaps = True
            break
    checks.append({
        "check": "no_phase_gaps",
        "status": "FAIL" if has_gaps else "PASS",
        "flag": "MISSING_PHASE" if has_gaps else None,
    })

    # Check 4: All phases have validation field
    phase_records = [
        r for r in records
        if isinstance(r.get("phase"), (int, float))
        and r["phase"] not in (0, 0.5)
        and r.get("event") != "end"
    ]
    unvalidated = [r for r in phase_records if "validation" not in r]
    checks.append({
        "check": "all_phases_validated",
        "status": "FAIL" if unvalidated else "PASS",
        "flag": "UNVALIDATED" if unvalidated else None,
    })

    # Check 5: Preflight record
    has_preflight = any(r.get("phase") == 0.5 for r in records)
    checks.append({
        "check": "preflight_present",
        "status": "PASS" if has_preflight else "FAIL",
        "flag": "NO_PREFLIGHT" if not has_preflight else None,
    })

    return checks


def compute_metrics(records: list[dict]) -> dict:
    """Compute quality metrics from trace records.

    Returns dict with: pass_rate, retry_rate, preflight_score,
    phase_coverage, harness_health, total_phases, phases_passed.
    """
    phase_records = [
        r for r in records
        if isinstance(r.get("phase"), (int, float))
        and r["phase"] not in (0, 0.5)
        and r.get("event") != "end"
    ]

    total_phases = len(phase_records)
    if total_phases == 0:
        return {
            "pass_rate": 0.0,
            "retry_rate": 0.0,
            "preflight_score": 0.0,
            "phase_coverage": 0.0,
            "harness_health": 0.0,
            "total_phases": 0,
            "phases_passed": 0,
        }

    phases_passed = sum(
        1 for r in phase_records if r.get("validation") == "PASS"
    )
    phases_with_retry = sum(
        1 for r in phase_records if r.get("retry") is True
    )
    phases_validated = sum(
        1 for r in phase_records if "validation" in r
    )

    pass_rate = phases_passed / total_phases
    retry_rate = phases_with_retry / total_phases
    phase_coverage = phases_validated / total_phases

    # Preflight score (0-5 scale)
    preflight = next((r for r in records if r.get("phase") == 0.5), None)
    preflight_score = preflight.get("score", 0) if preflight else 0

    # Composite health metric
    harness_health = pass_rate * phase_coverage * (preflight_score / 5) if preflight_score > 0 else 0.0

    return {
        "pass_rate": round(pass_rate, 3),
        "retry_rate": round(retry_rate, 3),
        "preflight_score": preflight_score,
        "phase_coverage": round(phase_coverage, 3),
        "harness_health": round(harness_health, 3),
        "total_phases": total_phases,
        "phases_passed": phases_passed,
    }


def diff_traces(metrics1: dict, metrics2: dict) -> dict:
    """Compare two trace metrics and classify drift.

    Returns dict with: deltas per metric, drift classification.
    """
    deltas = {}
    for key in ("pass_rate", "retry_rate", "preflight_score", "phase_coverage", "harness_health"):
        v1 = metrics1.get(key, 0)
        v2 = metrics2.get(key, 0)
        delta = round(v2 - v1, 3)
        if delta > 0.1:
            classification = "IMPROVEMENT"
        elif delta < -0.1:
            classification = "REGRESSION"
        else:
            classification = "STABLE"
        deltas[key] = {"trace1": v1, "trace2": v2, "delta": delta, "drift": classification}

    # Overall drift: worst individual drift wins
    all_drifts = [d["drift"] for d in deltas.values()]
    if "REGRESSION" in all_drifts:
        overall = "REGRESSION"
    elif "IMPROVEMENT" in all_drifts:
        overall = "IMPROVEMENT"
    else:
        overall = "STABLE"

    return {"deltas": deltas, "overall_drift": overall}


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    validate_only = "--validate" in sys.argv
    paths = [a for a in sys.argv[1:] if a != "--validate"]

    if not paths:
        print("ERROR: No trace file specified", file=sys.stderr)
        sys.exit(1)

    # Single trace analysis
    records1 = parse_trace(paths[0])
    validation = validate_structure(records1)
    metrics1 = compute_metrics(records1)

    result = {
        "trace": paths[0],
        "records": len(records1),
        "validation": validation,
        "metrics": metrics1,
    }

    if validate_only:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # Diff mode
    if len(paths) >= 2:
        records2 = parse_trace(paths[1])
        metrics2 = compute_metrics(records2)
        validation2 = validate_structure(records2)
        diff = diff_traces(metrics1, metrics2)
        result = {
            "trace1": {"path": paths[0], "metrics": metrics1, "validation": validation},
            "trace2": {"path": paths[1], "metrics": metrics2, "validation": validation2},
            "diff": diff,
        }

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Deterministic state management for autoloop and self-evolve skills.

Offloads TSV logging, delta computation, stagnation detection, regression
detection, Pareto updates, circuit breakers, and performance records
from the model to Python.

Usage:
    python scripts/loop-state.py <subcommand> [options]

Subcommands:
    tsv-append        Append iteration row to autoloop-results.tsv
    stagnation        Detect stagnation from TSV tail
    regression        Check per-axis regression against previous scores
    pareto-update     Update Pareto frontier JSON
    circuit-breaker   Check all circuit breaker conditions
    perf-record       Generate performance record JSON
    optstate-update   Update optimizer state JSON (FIFO ledger)
    exploration-weight  Compute adaptive exploration weight from TSV
    decay-predict     Fit exponential decay to predict ceiling (Parcae arXiv:2604.12946)

Design: Model does LATENT (what to mutate, quality judgment).
        This script does DETERMINISTIC (arithmetic, state, thresholds).
"""
import argparse
import csv
import json
import math
import sys
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MEMORY = Path(".claude/memory")


def _resolve_path(path: Path) -> Path:
    """Resolve MSYS2/Git Bash path translation on Windows.

    Git Bash translates /tmp → C:\\Users\\<user>\\AppData\\Local\\Temp before
    Python sees the argument, but Python's own Path('/tmp') resolves to C:\\tmp.
    When the MSYS-translated path doesn't exist, try the Python-native resolution.
    """
    if path.exists():
        return path
    if sys.platform == "win32":
        # Try interpreting the original Unix-style path via Python's resolution
        posix = path.as_posix()
        if "/AppData/Local/Temp/" in posix:
            # MSYS translated /tmp/foo → C:\Users\...\AppData\Local\Temp\foo
            # Try C:\tmp\foo instead
            basename = posix.split("/AppData/Local/Temp/", 1)[1]
            alt = Path("C:/tmp") / basename
            if alt.exists():
                return alt
    return path  # Return original even if not found (caller handles missing)


def read_tsv_tail(path: Path, n: int = 10) -> list[dict]:
    """Read last N rows from TSV file."""
    path = _resolve_path(path)
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").strip().split("\n")
    if len(lines) <= 1:  # header only or empty
        return []
    header = lines[0].split("\t")
    rows = []
    for line in lines[max(1, len(lines) - n):]:
        vals = line.split("\t")
        row = dict(zip(header, vals))
        rows.append(row)
    return rows


def tsv_row_count(path: Path) -> int:
    """Count data rows (excluding header)."""
    if not path.exists():
        return 0
    lines = path.read_text(encoding="utf-8", errors="replace").strip().split("\n")
    return max(0, len(lines) - 1)


# =============================================================================
# Subcommand: tsv-append
# =============================================================================
def cmd_tsv_append(args):
    """Append iteration row to TSV, computing delta from previous."""
    path = Path(args.tsv_path)

    # Read previous metric for delta
    rows = read_tsv_tail(path, 1)
    prev_metric = float(rows[-1].get("metric", 0)) if rows else 0
    current_metric = args.metric
    delta = round(current_metric - prev_metric, 6)

    row = {
        "iteration": args.iteration,
        "commit": args.commit or "",
        "metric": current_metric,
        "delta": delta,
        "guard": args.guard or "pass",
        "status": args.status,
        "description": args.description or "",
    }

    # Create file with header if doesn't exist
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "iteration\tcommit\tmetric\tdelta\tguard\tstatus\tdescription\n",
            encoding="utf-8",
        )

    # Append row
    line = "\t".join(str(row[k]) for k in [
        "iteration", "commit", "metric", "delta", "guard", "status", "description"
    ])
    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

    result = {
        "appended": row,
        "total_rows": tsv_row_count(path),
        "delta": delta,
        "improved": delta > 0,
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: stagnation
# =============================================================================
def cmd_stagnation(args):
    """Detect stagnation from TSV tail."""
    path = Path(args.tsv_path)
    rows = read_tsv_tail(path, args.window or 4)

    if len(rows) < 2:
        print(json.dumps({"stagnant": False, "reason": "insufficient_data"}))
        return

    statuses = [r.get("status", "").lower() for r in rows]
    consecutive_discards = 0
    for s in reversed(statuses):
        if s in ("discard", "crash", "revert"):
            consecutive_discards += 1
        else:
            break

    all_bad = all(s in ("discard", "crash", "revert") for s in statuses[-4:]) if len(statuses) >= 4 else False

    # Exploration weight ramp
    weight_table = {0: 1.0, 1: 1.0, 2: 1.2, 3: 1.4, 4: 1.7, 5: 2.0}
    exploration_weight = weight_table.get(
        min(consecutive_discards, 5), 2.0
    )

    stagnant = consecutive_discards >= 2 and int(rows[-1].get("iteration", 0)) > 4

    result = {
        "stagnant": stagnant,
        "consecutive_discards": consecutive_discards,
        "all_bad_last_4": all_bad,
        "exploration_weight": exploration_weight,
        "total_iterations": len(rows),
        "last_statuses": statuses[-4:],
        "steering": "yellow" if consecutive_discards >= 2 else (
            "red" if consecutive_discards >= 4 else "none"
        ),
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: regression
# =============================================================================
def cmd_regression(args):
    """Check per-axis regression against previous scores."""
    current = json.loads(args.current_scores)
    previous = json.loads(args.previous_scores)
    threshold = args.threshold or 0.5

    regressions = []
    improvements = []

    for dim in set(list(current.keys()) + list(previous.keys())):
        cur = current.get(dim, 0)
        prev = previous.get(dim, 0)
        diff = cur - prev
        if diff < -threshold:
            regressions.append({
                "dimension": dim,
                "previous": prev,
                "current": cur,
                "delta": round(diff, 4),
            })
        elif diff > threshold:
            improvements.append({
                "dimension": dim,
                "previous": prev,
                "current": cur,
                "delta": round(diff, 4),
            })

    result = {
        "has_regression": len(regressions) > 0,
        "regressions": regressions,
        "improvements": improvements,
        "net_change": round(
            sum(current.get(d, 0) for d in current) -
            sum(previous.get(d, 0) for d in previous), 4
        ),
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: pareto-update
# =============================================================================
def cmd_pareto_update(args):
    """Update Pareto frontier JSON with new candidate."""
    path = _resolve_path(Path(args.pareto_path))
    new_metric = args.metric
    new_cost = args.cost

    # Load existing frontier
    if path.exists():
        pareto = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    else:
        pareto = []

    new_point = {
        "metric": new_metric,
        "cost": new_cost,
        "iteration": args.iteration,
        "commit": args.commit or "",
    }

    # Check if new point is dominated
    dominated_by_existing = any(
        p["metric"] >= new_metric and p["cost"] <= new_cost
        for p in pareto
    )

    if dominated_by_existing:
        result = {
            "added": False,
            "reason": "dominated",
            "frontier_size": len(pareto),
        }
    else:
        # Remove points dominated by new
        before = len(pareto)
        pareto = [
            p for p in pareto
            if not (new_metric >= p["metric"] and new_cost <= p["cost"])
        ]
        removed = before - len(pareto)
        pareto.append(new_point)

        # Sort by metric descending
        pareto.sort(key=lambda p: -p["metric"])

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(pareto, indent=2), encoding="utf-8")

        result = {
            "added": True,
            "removed_dominated": removed,
            "frontier_size": len(pareto),
            "new_point": new_point,
        }

    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: circuit-breaker
# =============================================================================
def cmd_circuit_breaker(args):
    """Check all circuit breaker conditions."""
    triggers = []

    # 1. Consecutive reverts
    if args.consecutive_reverts is not None and args.consecutive_reverts >= 3:
        triggers.append({
            "type": "consecutive_reverts",
            "value": args.consecutive_reverts,
            "threshold": 3,
        })

    # 2. Max eval cases
    if args.eval_cases is not None and args.eval_cases >= 20:
        triggers.append({
            "type": "max_eval_cases",
            "value": args.eval_cases,
            "threshold": 20,
        })

    # 3. Skill file too large
    if args.skill_lines is not None and args.skill_lines > 500:
        triggers.append({
            "type": "skill_too_large",
            "value": args.skill_lines,
            "threshold": 500,
        })

    # 4. Max iterations
    if args.iteration is not None and args.max_iterations is not None:
        if args.iteration >= args.max_iterations:
            triggers.append({
                "type": "max_iterations",
                "value": args.iteration,
                "threshold": args.max_iterations,
            })

    # 5. Budget exhausted
    if args.budget_remaining is not None and args.budget_remaining <= 0:
        triggers.append({
            "type": "budget_exhausted",
            "value": args.budget_remaining,
            "threshold": 0,
        })

    result = {
        "stop": len(triggers) > 0,
        "triggers": triggers,
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: perf-record
# =============================================================================
def cmd_perf_record(args):
    """Generate performance record JSON from TSV data."""
    path = Path(args.tsv_path)
    rows = read_tsv_tail(path, 100)  # all rows

    if not rows:
        print(json.dumps({"error": "no TSV data"}))
        return

    iterations = len(rows)
    kept = sum(1 for r in rows if r.get("status", "").lower() == "keep")
    discarded = sum(1 for r in rows if r.get("status", "").lower() in ("discard", "revert"))
    crashed = sum(1 for r in rows if r.get("status", "").lower() == "crash")

    # First and last metrics
    try:
        start_metric = float(rows[0].get("metric", 0))
    except (ValueError, TypeError):
        start_metric = 0
    try:
        end_metric = float(rows[-1].get("metric", 0))
    except (ValueError, TypeError):
        end_metric = 0

    tokens_est = iterations * 3500

    record = {
        "skill": args.skill or "autoloop",
        "slug": args.slug or "unknown",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "iterations": iterations,
        "kept": kept,
        "discarded": discarded,
        "crashed": crashed,
        "metric_start": start_metric,
        "metric_end": end_metric,
        "metric_delta": round(end_metric - start_metric, 6),
        "tokens_est": tokens_est,
        "outcome": (
            "success" if end_metric > start_metric and kept > 0
            else "partial" if kept > 0
            else "failure"
        ),
    }

    # Write to performance dir if requested
    if args.write:
        perf_dir = MEMORY / "performance"
        perf_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_path = perf_dir / f"{record['skill']}-{record['slug']}-{ts}.json"
        out_path.write_text(json.dumps(record, indent=2), encoding="utf-8")
        record["written_to"] = str(out_path)

    print(json.dumps(record, indent=2))


# =============================================================================
# Subcommand: optstate-update
# =============================================================================
def cmd_optstate_update(args):
    """Update optimizer state JSON with new run data."""
    path = _resolve_path(Path(args.optstate_path))

    # Load existing
    if path.exists():
        state = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    else:
        state = {
            "last_updated": None,
            "total_runs": 0,
            "health": "unknown",
            "change_ledger": [],
            "strategies_that_work": [],
            "strategies_that_fail": [],
            "recurring_failure_patterns": [],
            "optimization_velocity": {"stage": "exploring", "trend": "flat"},
        }

    # Parse new entry
    entry = json.loads(args.entry_json)

    # Append to ledger (FIFO, max 20)
    state["change_ledger"].append(entry)
    if len(state["change_ledger"]) > 20:
        state["change_ledger"] = state["change_ledger"][-20:]

    # Update counters
    state["total_runs"] = state.get("total_runs", 0) + 1
    state["last_updated"] = datetime.now(timezone.utc).isoformat()

    # Aggregate strategies from ledger
    successes = [e.get("strategy", "") for e in state["change_ledger"]
                 if e.get("outcome") == "success"]
    failures = [e.get("strategy", "") for e in state["change_ledger"]
                if e.get("outcome") == "failure"]

    # Deduplicate, keep order
    seen = set()
    work = []
    for s in successes:
        if s and s not in seen:
            work.append(s)
            seen.add(s)
    state["strategies_that_work"] = work

    seen = set()
    fail = []
    for s in failures:
        if s and s not in seen:
            fail.append(s)
            seen.add(s)
    state["strategies_that_fail"] = fail

    # Velocity trend from last 5 entries
    recent = state["change_ledger"][-5:]
    recent_outcomes = [e.get("outcome", "") for e in recent]
    success_rate = sum(1 for o in recent_outcomes if o == "success") / max(len(recent_outcomes), 1)

    if success_rate >= 0.6:
        state["optimization_velocity"]["trend"] = "improving"
        state["health"] = "good"
    elif success_rate >= 0.3:
        state["optimization_velocity"]["trend"] = "flat"
        state["health"] = "fair"
    else:
        state["optimization_velocity"]["trend"] = "declining"
        state["health"] = "poor"

    # Write back
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    result = {
        "updated": True,
        "total_runs": state["total_runs"],
        "ledger_size": len(state["change_ledger"]),
        "health": state["health"],
        "velocity_trend": state["optimization_velocity"]["trend"],
        "strategies_work": len(state["strategies_that_work"]),
        "strategies_fail": len(state["strategies_that_fail"]),
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: exploration-weight
# =============================================================================
# =============================================================================
# Subcommand: decay-predict (Parcae-inspired, arXiv:2604.12946)
# =============================================================================
def _fit_exponential_decay(iterations: list[float], scores: list[float]) -> dict | None:
    """Fit L(T) = L_inf + Z * exp(-z * T) to score trajectory.

    For optimization (higher=better), we flip: S(T) = S_inf - Z * exp(-z * T)
    where S_inf is the predicted ceiling, Z is the initial gap, z is the decay rate.

    Uses simple least-squares grid search (no scipy dependency).
    """
    n = len(iterations)
    if n < 3:
        return None

    s_min = min(scores)
    s_max = max(scores)
    s_range = s_max - s_min
    if s_range < 1e-9:
        # All scores identical — no decay to fit
        return {"s_inf": s_max, "z": 0.0, "Z": 0.0, "r_squared": 1.0}

    best_err = float("inf")
    best_params = None

    # Grid search over S_inf candidates (ceiling above current max)
    for s_inf_mult in [1.0, 1.02, 1.05, 1.1, 1.15, 1.2, 1.3, 1.5]:
        s_inf = s_max + s_range * (s_inf_mult - 1.0)
        if s_inf_mult == 1.0:
            s_inf = s_max * 1.001  # Tiny offset to avoid log(0)

        # Z = S_inf - S(0), must be positive
        Z_est = s_inf - s_min
        if Z_est <= 0:
            continue

        # Grid search over decay rate z
        for z in [0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]:
            err = 0.0
            for i_idx in range(n):
                predicted = s_inf - Z_est * math.exp(-z * iterations[i_idx])
                err += (predicted - scores[i_idx]) ** 2
            if err < best_err:
                best_err = err
                best_params = {"s_inf": s_inf, "Z": Z_est, "z": z}

    if best_params is None:
        return None

    # R² calculation
    mean_s = sum(scores) / n
    ss_tot = sum((s - mean_s) ** 2 for s in scores)
    r_squared = 1.0 - best_err / ss_tot if ss_tot > 1e-9 else 0.0

    best_params["r_squared"] = max(0.0, r_squared)
    return best_params


def cmd_decay_predict(args):
    """Fit exponential decay to score trajectory, predict ceiling and remaining gain.

    Model: S(T) = S_inf - Z * exp(-z * T)
    where S_inf = predicted ceiling, Z = initial gap, z = decay rate.

    Returns JSON:
    {
      "fitted": true/false,
      "s_inf": predicted ceiling score,
      "current_best": current best score,
      "remaining_gain": s_inf - current_best,
      "remaining_gain_pct": remaining_gain / current_best * 100,
      "z": decay rate,
      "r_squared": fit quality (>0.8 = trustworthy),
      "early_stop_recommended": true if remaining gain < 1% of current,
      "target_reachable": true/false (if --target given),
      "iterations_to_target": estimated iterations to reach target (null if unreachable)
    }
    """
    path = _resolve_path(Path(args.tsv_path))
    rows = read_tsv_tail(path, 50)  # Read up to 50 iterations

    if len(rows) < (args.min_points or 4):
        print(json.dumps({
            "fitted": False,
            "reason": f"insufficient_data (need {args.min_points}, have {len(rows)})",
            "early_stop_recommended": False,
        }))
        return

    # Extract iteration numbers and metric values (only keeps, not discards/crashes)
    points = []
    best_so_far = None
    for r in rows:
        try:
            it = int(r.get("iteration", 0))
            metric = float(r.get("metric", 0))
            status = r.get("status", "").lower()
        except (ValueError, TypeError):
            continue

        # Track best-so-far trajectory (running max) — this is what we fit
        if best_so_far is None or metric > best_so_far:
            best_so_far = metric
        points.append((float(it), best_so_far))

    if len(points) < (args.min_points or 4):
        print(json.dumps({
            "fitted": False,
            "reason": "insufficient_valid_points",
            "early_stop_recommended": False,
        }))
        return

    iterations = [p[0] for p in points]
    scores = [p[1] for p in points]
    current_best = scores[-1]

    params = _fit_exponential_decay(iterations, scores)
    if params is None:
        print(json.dumps({
            "fitted": False,
            "reason": "fit_failed",
            "early_stop_recommended": False,
        }))
        return

    s_inf = params["s_inf"]
    remaining = max(0, s_inf - current_best)
    remaining_pct = (remaining / abs(current_best) * 100) if abs(current_best) > 1e-9 else 0.0

    result = {
        "fitted": True,
        "s_inf": round(s_inf, 4),
        "current_best": round(current_best, 4),
        "remaining_gain": round(remaining, 4),
        "remaining_gain_pct": round(remaining_pct, 2),
        "z": round(params["z"], 4),
        "Z": round(params["Z"], 4),
        "r_squared": round(params["r_squared"], 4),
        "data_points": len(points),
        "early_stop_recommended": remaining_pct < 1.0 and params["r_squared"] > 0.7,
    }

    # Target analysis (optional)
    if args.target is not None:
        target = args.target
        result["target"] = target
        if s_inf >= target:
            result["target_reachable"] = True
            # Solve: target = s_inf - Z * exp(-z * T) → T = -ln((s_inf - target) / Z) / z
            gap = s_inf - target
            if gap > 0 and params["Z"] > 0 and params["z"] > 0:
                ratio = gap / params["Z"]
                if 0 < ratio < 1:
                    iters_needed = -math.log(ratio) / params["z"]
                    result["iterations_to_target"] = round(iters_needed, 1)
                else:
                    result["iterations_to_target"] = 0
            else:
                result["iterations_to_target"] = 0
        else:
            result["target_reachable"] = False
            result["iterations_to_target"] = None

    print(json.dumps(result, indent=2))


def cmd_exploration_weight(args):
    """Compute adaptive exploration weight from consecutive discards."""
    path = Path(args.tsv_path)
    rows = read_tsv_tail(path, 10)

    consecutive = 0
    for r in reversed(rows):
        if r.get("status", "").lower() in ("discard", "crash", "revert"):
            consecutive += 1
        else:
            break

    weight_table = {0: 1.0, 1: 1.0, 2: 1.2, 3: 1.4, 4: 1.7, 5: 2.0}
    weight = weight_table.get(min(consecutive, 5), 2.0)

    exit_signal = consecutive >= (args.exit_threshold or 6)

    result = {
        "consecutive_discards": consecutive,
        "exploration_weight": weight,
        "exit_signal": exit_signal,
        "should_list_all_keeps": weight > 1.0,
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Main parser
# =============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Deterministic state for autoloop/self-evolve",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # tsv-append
    p = sub.add_parser("tsv-append", help="Append iteration row")
    p.add_argument("tsv_path", help="Path to TSV file")
    p.add_argument("--iteration", type=int, required=True)
    p.add_argument("--metric", type=float, required=True)
    p.add_argument("--status", required=True, choices=["keep", "discard", "crash", "revert", "baseline"])
    p.add_argument("--commit", default="")
    p.add_argument("--guard", default="pass")
    p.add_argument("--description", default="")
    p.set_defaults(func=cmd_tsv_append)

    # stagnation
    p = sub.add_parser("stagnation", help="Detect stagnation")
    p.add_argument("tsv_path")
    p.add_argument("--window", type=int, default=4)
    p.set_defaults(func=cmd_stagnation)

    # regression
    p = sub.add_parser("regression", help="Check per-axis regression")
    p.add_argument("current_scores", help='JSON: {"dim1": 4.0, "dim2": 3.5}')
    p.add_argument("previous_scores", help='JSON: {"dim1": 4.2, "dim2": 3.0}')
    p.add_argument("--threshold", type=float, default=0.5)
    p.set_defaults(func=cmd_regression)

    # pareto-update
    p = sub.add_parser("pareto-update", help="Update Pareto frontier")
    p.add_argument("pareto_path", help="Path to pareto.json")
    p.add_argument("--metric", type=float, required=True)
    p.add_argument("--cost", type=float, required=True)
    p.add_argument("--iteration", type=int, default=0)
    p.add_argument("--commit", default="")
    p.set_defaults(func=cmd_pareto_update)

    # circuit-breaker
    p = sub.add_parser("circuit-breaker", help="Check circuit breakers")
    p.add_argument("--consecutive-reverts", type=int)
    p.add_argument("--eval-cases", type=int)
    p.add_argument("--skill-lines", type=int)
    p.add_argument("--iteration", type=int)
    p.add_argument("--max-iterations", type=int)
    p.add_argument("--budget-remaining", type=float)
    p.set_defaults(func=cmd_circuit_breaker)

    # perf-record
    p = sub.add_parser("perf-record", help="Generate performance record")
    p.add_argument("tsv_path")
    p.add_argument("--skill", default="autoloop")
    p.add_argument("--slug", default="unknown")
    p.add_argument("--write", action="store_true", help="Write to performance dir")
    p.set_defaults(func=cmd_perf_record)

    # optstate-update
    p = sub.add_parser("optstate-update", help="Update optimizer state")
    p.add_argument("optstate_path")
    p.add_argument("entry_json", help="JSON ledger entry")
    p.set_defaults(func=cmd_optstate_update)

    # exploration-weight
    p = sub.add_parser("exploration-weight", help="Compute exploration weight")
    p.add_argument("tsv_path")
    p.add_argument("--exit-threshold", type=int, default=6)
    p.set_defaults(func=cmd_exploration_weight)

    # decay-predict (Parcae-inspired, arXiv:2604.12946)
    p = sub.add_parser("decay-predict", help="Fit exponential decay to score trajectory, predict ceiling")
    p.add_argument("tsv_path", help="Path to TSV with iteration/metric columns")
    p.add_argument("--target", type=float, default=None, help="Target score (optional, for gap analysis)")
    p.add_argument("--min-points", type=int, default=4, help="Min data points before fitting (default: 4)")
    p.set_defaults(func=cmd_decay_predict)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

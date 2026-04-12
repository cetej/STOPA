#!/usr/bin/env python3
"""Deterministic gates for orchestrate skill.

Offloads arithmetic, threshold checks, set operations, and structured data
parsing from the model to Python. Each subcommand returns JSON to stdout
for the model to consume.

Usage:
    python scripts/deterministic-gates.py <subcommand> [options]

Subcommands:
    tier-select       Auto-detect complexity tier from signals
    budget-check      Check budget constraints and compute allocations
    file-disjoint     Verify WRITE file lists don't overlap across subtasks
    failure-pattern   Detect recurring failure patterns in failures/
    cache-stale       Check if scout/research cache is still fresh
    amdahl-gate       Compute parallelizability fraction and tier cap
    cost-gate         Pre-execution ROI check for planned agents
    wave-check        Inter-wave completeness verification
    context-health    Score context health for auto-compact trigger

Design principle (Garry Tan — Thin Harness, Fat Skills):
    Model does LATENT work (judgment, synthesis, interpretation).
    This script does DETERMINISTIC work (arithmetic, thresholds, set ops).
"""
import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MEMORY = Path(".claude/memory")
LEARNINGS = MEMORY / "learnings"
FAILURES = MEMORY / "failures"
INTERMEDIATE = MEMORY / "intermediate"

# --- Tier definitions ---
TIER_AGENT_LIMITS = {
    "light": 1, "standard": 4, "deep": 8, "farm": 8
}
TIER_AVG_COST = {
    "light": 0.02, "standard": 0.05, "deep": 0.10, "farm": 0.03
}
KEYWORD_TIER = {
    "fix": "light", "typo": "light", "rename": "light", "lint": "light",
    "refactor": "standard", "implement": "standard", "add": "standard",
    "feature": "standard", "migrate": "standard",
    "redesign": "deep", "architecture": "deep", "rearchitect": "deep",
    "bulk": "farm", "20+": "farm",
}
TIER_ORDER = ["light", "standard", "deep", "farm"]


def tier_rank(t: str) -> int:
    """Numeric rank for tier comparison."""
    return TIER_ORDER.index(t) if t in TIER_ORDER else 1


def parse_yaml_frontmatter(text: str) -> dict:
    """Extract simple YAML frontmatter from markdown file."""
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    yaml_block = text[3:end].strip()
    result = {}
    for line in yaml_block.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            val = val.strip().strip('"').strip("'")
            result[key.strip()] = val
    return result


def parse_budget_remaining() -> float:
    """Read remaining budget from budget.md Event Log."""
    path = MEMORY / "budget.md"
    if not path.exists():
        return 10.0  # default generous budget
    text = path.read_text(encoding="utf-8", errors="replace")
    # Find last Running Total value
    totals = re.findall(r"\$(\d+\.?\d*)", text)
    if totals:
        spent = float(totals[-1])
        return max(0, 10.0 - spent)  # assume $10 default budget
    return 10.0


# =============================================================================
# Subcommand: tier-select
# =============================================================================
def cmd_tier_select(args):
    """Auto-detect complexity tier from signals."""
    signals = {}
    tier_candidates = []

    # 1. Budget constraint
    if args.budget_used_pct and args.budget_used_pct >= 80:
        signals["budget_constraint"] = f"{args.budget_used_pct}% used → cap at standard"
        tier_candidates.append("standard")

    # 2. Keyword signals
    if args.keywords:
        for kw in args.keywords:
            kw_lower = kw.lower()
            for pattern, tier in KEYWORD_TIER.items():
                if pattern in kw_lower:
                    signals[f"keyword_{pattern}"] = tier
                    tier_candidates.append(tier)
                    break

    # 3. File count
    if args.file_count is not None:
        fc = args.file_count
        if fc <= 1:
            fc_tier = "light"
        elif fc <= 5:
            fc_tier = "standard"
        elif fc >= 20 and args.mechanical:
            fc_tier = "farm"
        else:
            fc_tier = "deep"
        signals["file_count"] = f"{fc} files → {fc_tier}"
        tier_candidates.append(fc_tier)

    # 4. Uncertainty → bump one tier
    if args.uncertain:
        signals["uncertainty"] = "vague scope → +1 tier"

    # Select tier: max of candidates (most conservative)
    if not tier_candidates:
        selected = "standard"  # safe default
    else:
        selected = max(tier_candidates, key=tier_rank)

    # Apply uncertainty bump (but cap at deep)
    if args.uncertain and selected != "deep":
        idx = tier_rank(selected)
        if idx < 2:  # don't bump farm
            selected = TIER_ORDER[idx + 1]
            signals["uncertainty_applied"] = f"bumped to {selected}"

    # Budget cap override
    if args.budget_used_pct and args.budget_used_pct >= 80:
        if tier_rank(selected) > tier_rank("standard"):
            selected = "standard"
            signals["budget_cap_applied"] = True

    result = {
        "tier": selected,
        "signals": signals,
        "agent_limit": TIER_AGENT_LIMITS[selected],
        "avg_cost": TIER_AVG_COST[selected],
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: budget-check
# =============================================================================
def cmd_budget_check(args):
    """Check budget constraints and compute per-agent allocations."""
    remaining = args.remaining if args.remaining is not None else parse_budget_remaining()
    planned = args.planned_agents or 1
    tier = args.tier or "standard"
    avg_cost = TIER_AVG_COST.get(tier, 0.05)

    estimated_cost = planned * avg_cost
    reserve = remaining * 0.20
    allocatable = remaining - reserve

    # Complexity weights for allocation
    complexities = []
    if args.scope_sizes:
        for s in args.scope_sizes:
            weight = s + (2 if args.has_security else 0)
            complexities.append(weight)
    else:
        complexities = [1] * planned

    total_complexity = sum(complexities) or 1
    allocations = [
        round(allocatable * (c / total_complexity), 4)
        for c in complexities
    ]

    min_viable = 0.03
    merge_candidates = [
        i for i, a in enumerate(allocations) if a < min_viable
    ]

    # Gate decision
    if estimated_cost > remaining:
        gate = "STOP"
    elif estimated_cost > remaining * 0.8:
        gate = "WARNING"
    else:
        gate = "PASS"

    result = {
        "gate": gate,
        "remaining_budget": round(remaining, 2),
        "estimated_cost": round(estimated_cost, 2),
        "reserve": round(reserve, 2),
        "allocatable": round(allocatable, 2),
        "per_agent_allocation": allocations,
        "merge_candidates": merge_candidates,
        "min_viable": min_viable,
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: file-disjoint
# =============================================================================
def cmd_file_disjoint(args):
    """Verify WRITE file lists don't overlap across subtasks."""
    # Input: JSON array of arrays, e.g. [["a.py","b.py"],["c.py"],["b.py","d.py"]]
    write_lists = json.loads(args.write_lists)
    collisions = []

    for i in range(len(write_lists)):
        for j in range(i + 1, len(write_lists)):
            overlap = set(write_lists[i]) & set(write_lists[j])
            if overlap:
                collisions.append({
                    "subtask_a": i,
                    "subtask_b": j,
                    "overlapping_files": sorted(overlap),
                })

    result = {
        "disjoint": len(collisions) == 0,
        "collisions": collisions,
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: failure-pattern
# =============================================================================
def cmd_failure_pattern(args):
    """Detect recurring failure patterns in failures/ directory."""
    if not FAILURES.exists():
        print(json.dumps({"patterns": [], "total_failures": 0}))
        return

    failures = []
    for f in FAILURES.glob("*.md"):
        if f.name.startswith("."):
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        meta = parse_yaml_frontmatter(text)
        if meta:
            failures.append({
                "file": f.name,
                "failure_class": meta.get("failure_class", "unknown"),
                "failure_agent": meta.get("failure_agent", "unknown"),
                "resolved": meta.get("resolved", "false") == "true",
                "date": meta.get("date", ""),
            })

    # Count co-occurrences of (failure_class, failure_agent)
    pair_counts = Counter(
        (f["failure_class"], f["failure_agent"]) for f in failures
    )

    patterns = []
    for (fc, fa), count in pair_counts.most_common():
        if count >= 2:
            patterns.append({
                "failure_class": fc,
                "failure_agent": fa,
                "count": count,
                "trigger": "learn-from-failure" if count >= 2 else None,
                "circuit_breaker": count >= 3,
            })

    result = {
        "total_failures": len(failures),
        "unresolved": sum(1 for f in failures if not f["resolved"]),
        "patterns": patterns,
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: cache-stale
# =============================================================================
def cmd_cache_stale(args):
    """Check if scout/research cache is still fresh."""
    max_age_hours = args.max_age or 2
    now = datetime.now(timezone.utc)
    results = []

    if not INTERMEDIATE.exists():
        print(json.dumps({"caches": [], "all_stale": True}))
        return

    for pattern in ["scout-*.json", "research-*.json"]:
        for f in INTERMEDIATE.glob(pattern):
            try:
                data = json.loads(f.read_text(encoding="utf-8", errors="replace"))
            except (json.JSONDecodeError, OSError):
                results.append({"file": f.name, "stale": True, "reason": "parse_error"})
                continue

            saved_at = data.get("savedAt", data.get("saved_at", ""))
            if not saved_at:
                results.append({"file": f.name, "stale": True, "reason": "no_timestamp"})
                continue

            try:
                # Try ISO format
                saved_dt = datetime.fromisoformat(saved_at.replace("Z", "+00:00"))
            except ValueError:
                results.append({"file": f.name, "stale": True, "reason": "bad_timestamp"})
                continue

            age_hours = (now - saved_dt).total_seconds() / 3600
            is_stale = age_hours > max_age_hours

            results.append({
                "file": f.name,
                "stale": is_stale,
                "age_hours": round(age_hours, 1),
                "summary_key": "summary" if "summary" in data else None,
            })

    result = {
        "caches": results,
        "all_stale": all(r["stale"] for r in results) if results else True,
        "reusable": [r["file"] for r in results if not r["stale"]],
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: amdahl-gate
# =============================================================================
def cmd_amdahl_gate(args):
    """Compute parallelizability fraction and tier cap."""
    total = args.total_subtasks
    independent = args.independent_subtasks

    if total <= 0:
        print(json.dumps({"error": "total_subtasks must be > 0"}))
        return

    p = independent / total

    if p < 0.4:
        cap = "light"
        max_agents = 1
    elif p < 0.7:
        cap = "standard"
        max_agents = 3
    else:
        cap = None  # no cap
        max_agents = TIER_AGENT_LIMITS.get(args.current_tier, 8)

    # Apply cap (only downgrade, never upgrade)
    original_tier = args.current_tier or "standard"
    final_tier = original_tier
    capped = False

    if cap and tier_rank(original_tier) > tier_rank(cap):
        # Farm is exempt
        if original_tier != "farm":
            final_tier = cap
            capped = True

    result = {
        "p": round(p, 2),
        "independent": independent,
        "total": total,
        "cap_tier": cap,
        "original_tier": original_tier,
        "final_tier": final_tier,
        "capped": capped,
        "max_agents": max_agents,
        "log": f"Amdahl gate: p={p:.1f} ({independent}/{total} independent). "
               f"Tier: {original_tier} -> {final_tier}.",
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: cost-gate
# =============================================================================
def cmd_cost_gate(args):
    """Pre-execution ROI check for planned agents."""
    planned = args.planned_agents or 1
    tier = args.tier or "standard"
    remaining = args.remaining if args.remaining is not None else parse_budget_remaining()
    avg_cost = TIER_AVG_COST.get(tier, 0.05)

    estimated = planned * avg_cost

    # ROI: would a single agent at higher tier be cheaper?
    single_higher = None
    tier_idx = tier_rank(tier)
    if tier_idx < len(TIER_ORDER) - 1 and planned >= 3:
        higher = TIER_ORDER[tier_idx + 1]
        higher_cost = TIER_AVG_COST.get(higher, 0.10)
        if higher_cost < estimated:
            single_higher = {
                "tier": higher,
                "cost": higher_cost,
                "savings": round(estimated - higher_cost, 4),
            }

    gate = "PASS"
    if estimated > remaining:
        gate = "STOP"
    elif estimated > remaining * 0.8:
        gate = "WARNING"

    lower_tier = TIER_ORDER[max(0, tier_idx - 1)]
    lower_agents = max(1, planned - 2)

    result = {
        "gate": gate,
        "estimated_cost": round(estimated, 4),
        "remaining": round(remaining, 2),
        "utilization_pct": round((estimated / remaining) * 100, 1) if remaining > 0 else 999,
        "single_higher_tier_option": single_higher,
        "downgrade_suggestion": {
            "tier": lower_tier,
            "agents": lower_agents,
            "estimated": round(lower_agents * TIER_AVG_COST.get(lower_tier, 0.02), 4),
        } if gate != "PASS" else None,
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: wave-check
# =============================================================================
def cmd_wave_check(args):
    """Inter-wave completeness verification."""
    # Input: JSON with subtasks array
    subtasks = json.loads(args.subtasks_json)
    current_wave = args.current_wave

    issues = []
    completed_ids = set()

    for st in subtasks:
        if st.get("status") == "done":
            completed_ids.add(st["id"])
            # Check artifact presence
            if not st.get("artifacts"):
                issues.append({
                    "type": "missing_artifacts",
                    "subtask": st["id"],
                    "severity": "high",
                })

    # Check downstream readiness for next wave
    next_wave = current_wave + 1
    for st in subtasks:
        if st.get("wave") == next_wave:
            deps = st.get("depends_on", [])
            missing = [d for d in deps if d not in completed_ids]
            if missing:
                issues.append({
                    "type": "unmet_dependency",
                    "subtask": st["id"],
                    "missing_deps": missing,
                    "severity": "blocker",
                })

    result = {
        "wave": current_wave,
        "next_wave": next_wave,
        "ready": len(issues) == 0,
        "issues": issues,
        "completed_in_wave": sorted(completed_ids),
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: context-health
# =============================================================================
def cmd_context_health(args):
    """Score context health for auto-compact trigger."""
    score = 0
    signals = []

    if args.subtasks_done is not None and args.subtasks_total is not None:
        pct = args.subtasks_done / max(args.subtasks_total, 1)
        if pct >= 0.7:
            score += 2
            signals.append(f"70%+ subtasks done ({args.subtasks_done}/{args.subtasks_total})")

    if args.agents_spawned is not None and args.agents_spawned >= 3:
        score += 2
        signals.append(f"{args.agents_spawned} agents spawned")

    if args.concerns is not None and args.concerns > 0:
        score += args.concerns
        signals.append(f"{args.concerns} DONE_WITH_CONCERNS")

    if args.blocked is not None and args.blocked > 0:
        score += args.blocked * 2
        signals.append(f"{args.blocked} blocked subtasks")

    if score <= 2:
        level = "green"
        action = "continue"
    elif score <= 4:
        level = "yellow"
        action = "consider_checkpoint"
    elif score <= 6:
        level = "orange"
        action = "auto_compact"
    else:
        level = "red"
        action = "save_checkpoint_now"

    result = {
        "score": score,
        "level": level,
        "action": action,
        "signals": signals,
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Main parser
# =============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Deterministic gates for orchestrate skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # tier-select
    p = sub.add_parser("tier-select", help="Auto-detect complexity tier")
    p.add_argument("--keywords", nargs="*", help="Task keywords (fix, refactor, etc.)")
    p.add_argument("--file-count", type=int, help="Number of affected files")
    p.add_argument("--mechanical", action="store_true", help="Mechanical/repetitive task")
    p.add_argument("--uncertain", action="store_true", help="Vague scope")
    p.add_argument("--budget-used-pct", type=float, help="Percentage of budget already used")
    p.set_defaults(func=cmd_tier_select)

    # budget-check
    p = sub.add_parser("budget-check", help="Budget constraints and allocations")
    p.add_argument("--remaining", type=float, help="Remaining budget in $")
    p.add_argument("--planned-agents", type=int, help="Number of planned agents")
    p.add_argument("--tier", help="Current tier")
    p.add_argument("--scope-sizes", type=int, nargs="*",
                    help="Number of context_scope files per subtask")
    p.add_argument("--has-security", action="store_true",
                    help="Any subtask touches security/auth/payment")
    p.set_defaults(func=cmd_budget_check)

    # file-disjoint
    p = sub.add_parser("file-disjoint", help="Check WRITE file lists overlap")
    p.add_argument("write_lists", help='JSON array of arrays: [["a.py"],["b.py","a.py"]]')
    p.set_defaults(func=cmd_file_disjoint)

    # failure-pattern
    p = sub.add_parser("failure-pattern", help="Detect recurring failure patterns")
    p.set_defaults(func=cmd_failure_pattern)

    # cache-stale
    p = sub.add_parser("cache-stale", help="Check scout/research cache freshness")
    p.add_argument("--max-age", type=float, default=2, help="Max age in hours (default: 2)")
    p.set_defaults(func=cmd_cache_stale)

    # amdahl-gate
    p = sub.add_parser("amdahl-gate", help="Parallelizability check")
    p.add_argument("--total-subtasks", type=int, required=True)
    p.add_argument("--independent-subtasks", type=int, required=True)
    p.add_argument("--current-tier", default="standard")
    p.set_defaults(func=cmd_amdahl_gate)

    # cost-gate
    p = sub.add_parser("cost-gate", help="Pre-execution ROI check")
    p.add_argument("--planned-agents", type=int, required=True)
    p.add_argument("--tier", default="standard")
    p.add_argument("--remaining", type=float, help="Remaining budget in $")
    p.set_defaults(func=cmd_cost_gate)

    # wave-check
    p = sub.add_parser("wave-check", help="Inter-wave completeness check")
    p.add_argument("subtasks_json", help="JSON string with subtasks array")
    p.add_argument("--current-wave", type=int, required=True)
    p.set_defaults(func=cmd_wave_check)

    # context-health
    p = sub.add_parser("context-health", help="Score context health")
    p.add_argument("--subtasks-done", type=int)
    p.add_argument("--subtasks-total", type=int)
    p.add_argument("--agents-spawned", type=int)
    p.add_argument("--concerns", type=int, default=0)
    p.add_argument("--blocked", type=int, default=0)
    p.set_defaults(func=cmd_context_health)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

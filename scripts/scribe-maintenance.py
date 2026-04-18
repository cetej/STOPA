#!/usr/bin/env python3
"""Deterministic maintenance operations for scribe skill.

Offloads deduplication, staleness checks, counter health, history pruning,
archive rotation, and supersedes validation from the model to Python.

Usage:
    python scripts/scribe-maintenance.py <subcommand> [options]

Subcommands:
    dedup-check       Find near-duplicate learnings (Jaccard on tags+summary words)
    staleness         List learnings older than N days
    counter-health    Flag problematic/high-performing learnings by counters
    supersedes-check  Validate supersedes: references point to existing files
    confidence-decay  Compute decayed confidence for all learnings
    archive-rotate    Check if files need rotation (budget, performance, state)
    salience-gate     Compute salience score for a new learning

Design: Model does LATENT (decide which learnings to merge/prune).
        This script does DETERMINISTIC (similarity, date math, counter checks).
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MEMORY = Path(".claude/memory")
LEARNINGS = MEMORY / "learnings"


def parse_frontmatter(path: Path) -> dict:
    """Extract YAML frontmatter from markdown file."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    yaml_block = text[3:end].strip()
    result = {"_file": path.name, "_path": str(path)}
    for line in yaml_block.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            # Handle arrays like [tag1, tag2]
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",") if v.strip()]
            result[key] = val
    return result


def load_all_learnings() -> list[dict]:
    """Load frontmatter from all learning files."""
    if not LEARNINGS.exists():
        return []
    return [
        fm for f in sorted(LEARNINGS.glob("*.md"))
        if not f.name.startswith(".") and f.name != "critical-patterns.md"
        and (fm := parse_frontmatter(f))
        and fm.get("date")  # must have date field
    ]


def word_set(text: str) -> set[str]:
    """Extract word set from text for Jaccard similarity."""
    return set(re.findall(r'\w+', text.lower())) - {"the", "a", "an", "is", "to", "of", "in", "for", "and", "or"}


def jaccard(s1: set, s2: set) -> float:
    """Jaccard similarity between two sets."""
    if not s1 and not s2:
        return 0.0
    return len(s1 & s2) / len(s1 | s2)


# =============================================================================
# Subcommand: dedup-check
# =============================================================================
def cmd_dedup_check(args):
    """Find near-duplicate learnings."""
    learnings = load_all_learnings()
    threshold = args.threshold or 0.6
    duplicates = []

    for i in range(len(learnings)):
        for j in range(i + 1, len(learnings)):
            a, b = learnings[i], learnings[j]

            # Same component?
            if a.get("component") != b.get("component"):
                continue

            # Tag overlap
            tags_a = set(a.get("tags", []) if isinstance(a.get("tags"), list) else [])
            tags_b = set(b.get("tags", []) if isinstance(b.get("tags"), list) else [])
            if len(tags_a & tags_b) < 2:
                continue

            # Summary word similarity
            words_a = word_set(a.get("summary", ""))
            words_b = word_set(b.get("summary", ""))
            sim = jaccard(words_a, words_b)

            if sim >= threshold:
                duplicates.append({
                    "file_a": a["_file"],
                    "file_b": b["_file"],
                    "component": a.get("component"),
                    "shared_tags": sorted(tags_a & tags_b),
                    "similarity": round(sim, 3),
                })

    result = {
        "total_learnings": len(learnings),
        "duplicates_found": len(duplicates),
        "threshold": threshold,
        "duplicates": duplicates,
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: staleness
# =============================================================================
def cmd_staleness(args):
    """List learnings older than N days."""
    learnings = load_all_learnings()
    max_days = args.days or 90
    today = datetime.now()
    stale = []

    for l in learnings:
        date_str = l.get("date", "")
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            stale.append({"file": l["_file"], "reason": "unparseable_date", "date": date_str})
            continue

        age = (today - d).days
        if age > max_days:
            uses = int(l.get("uses", 0)) if l.get("uses", "0").isdigit() else 0
            stale.append({
                "file": l["_file"],
                "date": date_str,
                "age_days": age,
                "uses": uses,
                "component": l.get("component", ""),
                "severity": l.get("severity", ""),
            })

    # Sort by age descending
    stale.sort(key=lambda x: x.get("age_days", 0), reverse=True)

    result = {
        "total_learnings": len(learnings),
        "stale_count": len(stale),
        "threshold_days": max_days,
        "stale": stale,
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: counter-health
# =============================================================================
def cmd_counter_health(args):
    """Flag problematic/high-performing learnings by counters."""
    learnings = load_all_learnings()
    problematic = []
    high_performing = []
    graduation_candidates = []

    for l in learnings:
        uses = int(l.get("uses", 0)) if str(l.get("uses", "0")).isdigit() else 0
        harmful = int(l.get("harmful_uses", 0)) if str(l.get("harmful_uses", "0")).isdigit() else 0
        successful = int(l.get("successful_uses", 0)) if str(l.get("successful_uses", "0")).isdigit() else 0
        conf_str = l.get("confidence", "0.7")
        try:
            confidence = float(conf_str)
        except (ValueError, TypeError):
            confidence = 0.7

        entry = {
            "file": l["_file"],
            "uses": uses,
            "harmful_uses": harmful,
            "successful_uses": successful,
            "confidence": confidence,
            "component": l.get("component", ""),
        }

        # Problematic: harmful >= uses and harmful > 0
        if harmful >= uses and harmful > 0:
            entry["reason"] = "harmful_dominates"
            problematic.append(entry)

        # Also problematic: low confidence
        if confidence < 0.3:
            entry["reason"] = "low_confidence"
            if entry not in problematic:
                problematic.append(entry)

        # High performing: uses > 5 and harmful < 2
        if uses > 5 and harmful < 2:
            high_performing.append(entry)

        # Graduation: uses >= 10 AND confidence >= 0.8 AND harmful < 2
        if uses >= 10 and confidence >= 0.8 and harmful < 2:
            graduation_candidates.append(entry)

    result = {
        "total_learnings": len(learnings),
        "problematic": problematic,
        "high_performing": high_performing,
        "graduation_candidates": graduation_candidates,
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: supersedes-check
# =============================================================================
def cmd_supersedes_check(args):
    """Validate supersedes: references point to existing files."""
    learnings = load_all_learnings()
    broken = []
    valid = 0

    for l in learnings:
        sup = l.get("supersedes", "")
        if not sup:
            continue

        target = LEARNINGS / sup
        if target.exists():
            valid += 1
        else:
            broken.append({
                "file": l["_file"],
                "supersedes": sup,
                "reason": "target_not_found",
            })

    # Also check related: refs
    broken_related = []
    for l in learnings:
        related = l.get("related", [])
        if isinstance(related, str):
            related = [r.strip() for r in related.strip("[]").split(",") if r.strip()]
        for r in related:
            target = LEARNINGS / r
            if not target.exists():
                broken_related.append({
                    "file": l["_file"],
                    "related": r,
                    "reason": "target_not_found",
                })

    result = {
        "supersedes_valid": valid,
        "supersedes_broken": broken,
        "related_broken": broken_related,
        "total_issues": len(broken) + len(broken_related),
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: confidence-decay
# =============================================================================
def cmd_confidence_decay(args):
    """Compute decayed confidence for all learnings."""
    learnings = load_all_learnings()
    today = datetime.now()
    decayed = []

    for l in learnings:
        uses = int(l.get("uses", 0)) if str(l.get("uses", "0")).isdigit() else 0
        conf_str = l.get("confidence", "0.7")
        try:
            original_conf = float(conf_str)
        except (ValueError, TypeError):
            original_conf = 0.7

        date_str = l.get("date", "")
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue

        age_days = (today - d).days

        # Decay: unused learnings (uses == 0) 60+ days old lose 0.1 per 30 days
        # Learnings with uses > 0 don't decay
        effective_conf = original_conf
        if uses == 0 and age_days > 60:
            decay_periods = (age_days - 60) // 30
            decay = decay_periods * 0.1
            effective_conf = max(0.1, original_conf - decay)

        if effective_conf < original_conf:
            decayed.append({
                "file": l["_file"],
                "original_confidence": original_conf,
                "effective_confidence": round(effective_conf, 2),
                "decay": round(original_conf - effective_conf, 2),
                "age_days": age_days,
                "uses": uses,
            })

    result = {
        "total_learnings": len(learnings),
        "decayed_count": len(decayed),
        "decayed": sorted(decayed, key=lambda x: x["effective_confidence"]),
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: archive-rotate
# =============================================================================
def cmd_archive_rotate(args):
    """Check if files need rotation."""
    checks = []

    # Budget history rows
    budget_path = MEMORY / "budget.md"
    if budget_path.exists():
        text = budget_path.read_text(encoding="utf-8", errors="replace")
        # Count table rows in History section
        in_history = False
        row_count = 0
        for line in text.split("\n"):
            if "## History" in line or "## History (Enriched Traces)" in line:
                in_history = True
                continue
            if in_history and line.startswith("|") and not line.startswith("| Task") and not line.startswith("|---"):
                row_count += 1
        if row_count > 10:
            checks.append({
                "file": "budget.md",
                "type": "table_rows",
                "count": row_count,
                "threshold": 10,
                "action": "archive_oldest_to_budget-archive.md",
            })

    # Performance files
    perf_dir = MEMORY / "performance"
    if perf_dir.exists():
        perf_files = sorted(perf_dir.glob("*.json"), key=lambda f: f.stat().st_mtime)
        if len(perf_files) > 30:
            checks.append({
                "file": "performance/",
                "type": "file_count",
                "count": len(perf_files),
                "threshold": 30,
                "oldest_files": [f.name for f in perf_files[:len(perf_files) - 30]],
                "action": "move_oldest_to_performance/archive/",
            })

    # Learnings count
    if LEARNINGS.exists():
        learning_files = list(LEARNINGS.glob("*.md"))
        learning_count = len([f for f in learning_files if f.name != "critical-patterns.md"])
        if learning_count > 200:
            checks.append({
                "file": "learnings/",
                "type": "file_count",
                "count": learning_count,
                "threshold": 200,
                "action": "prune_low_confidence_learnings",
            })

    # State.md line count
    state_path = MEMORY / "state.md"
    if state_path.exists():
        line_count = len(state_path.read_text(encoding="utf-8", errors="replace").split("\n"))
        if line_count > 500:
            checks.append({
                "file": "state.md",
                "type": "line_count",
                "count": line_count,
                "threshold": 500,
                "action": "prune_task_history_keep_last_5",
            })

    # Failures count
    failures_dir = MEMORY / "failures"
    if failures_dir.exists():
        failure_files = list(failures_dir.glob("*.md"))
        if len(failure_files) > 50:
            checks.append({
                "file": "failures/",
                "type": "file_count",
                "count": len(failure_files),
                "threshold": 50,
                "action": "archive_oldest_to_failures/archive/",
            })

    result = {
        "needs_rotation": len(checks) > 0,
        "checks": checks,
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Subcommand: salience-gate
# =============================================================================
def cmd_salience_gate(args):
    """Compute salience score for a new learning."""
    # Source reputation weights
    source_weights = {
        "user_correction": 1.5,
        "critic_finding": 1.2,
        "auto_pattern": 1.0,
        "external_research": 0.9,
        "agent_generated": 0.8,
    }

    source = args.source or "auto_pattern"
    source_rep = source_weights.get(source, 1.0)

    # Novelty: 1.0 if no similar exists, lower if duplicate found
    novelty = args.novelty if args.novelty is not None else 1.0

    # Reliability: based on verify_check presence
    reliability = 1.0 if args.has_verify_check else 0.7

    salience = round(source_rep * novelty * reliability, 3)
    threshold = 0.4

    result = {
        "salience": salience,
        "threshold": threshold,
        "decision": "WRITE" if salience >= threshold else "SKIP",
        "breakdown": {
            "source_reputation": source_rep,
            "novelty": novelty,
            "reliability": reliability,
        },
    }
    print(json.dumps(result, indent=2))


# =============================================================================
# Main parser
# =============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Deterministic maintenance for scribe skill",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # dedup-check
    p = sub.add_parser("dedup-check", help="Find near-duplicate learnings")
    p.add_argument("--threshold", type=float, default=0.6, help="Jaccard threshold")
    p.set_defaults(func=cmd_dedup_check)

    # staleness
    p = sub.add_parser("staleness", help="List stale learnings")
    p.add_argument("--days", type=int, default=90, help="Age threshold in days")
    p.set_defaults(func=cmd_staleness)

    # counter-health
    p = sub.add_parser("counter-health", help="Flag learnings by counter health")
    p.set_defaults(func=cmd_counter_health)

    # supersedes-check
    p = sub.add_parser("supersedes-check", help="Validate supersedes references")
    p.set_defaults(func=cmd_supersedes_check)

    # confidence-decay
    p = sub.add_parser("confidence-decay", help="Compute decayed confidence")
    p.set_defaults(func=cmd_confidence_decay)

    # archive-rotate
    p = sub.add_parser("archive-rotate", help="Check rotation needs")
    p.set_defaults(func=cmd_archive_rotate)

    # salience-gate
    p = sub.add_parser("salience-gate", help="Compute salience score")
    p.add_argument("--source", default="auto_pattern",
                    choices=["user_correction", "critic_finding", "auto_pattern",
                             "external_research", "agent_generated"])
    p.add_argument("--novelty", type=float, help="Novelty score 0-1")
    p.add_argument("--has-verify-check", action="store_true")
    p.set_defaults(func=cmd_salience_gate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Auto-detect orchestration tier from task description and file count.

Usage:
    python tier-detector.py "<task description>" [file_count]
    python tier-detector.py --roi <total_subtasks> <independent_subtasks> <agent_count>
    python tier-detector.py --ltask --c-exec <none|light|heavy> --s-space <narrow|moderate|broad|unknown> --d-feedback <strong|weak|manual>

Output: JSON with recommended tier, reasoning, and (for ROI/L_task) analysis.
"""

import json
import re
import sys


# Tier keyword patterns (checked in order, first match wins)
TIER_KEYWORDS = {
    "light": [
        r"\bfix\b", r"\btypo\b", r"\brename\b", r"\bupdate\b", r"\bbump\b",
        r"\btweak\b", r"\badd comment\b", r"\bremove\b",
    ],
    "standard": [
        r"\brefactor\b", r"\badd feature\b", r"\bimplement\b", r"\bmigrate\b",
        r"\bextend\b", r"\bintegrate\b",
    ],
    "deep": [
        r"\bredesign\b", r"\barchitecture\b", r"\bcross-cutting\b",
        r"\bsecurity audit\b", r"\bunknown scope\b", r"\bmajor\b",
    ],
    "farm": [
        r"\ball files\b", r"\beverywhere\b", r"\bbulk\b", r"\blint fix\b",
        r"\b20\+\b", r"\bmechanical\b",
    ],
}

TIER_FILE_THRESHOLDS = {
    1: "light",
    5: "standard",  # 2-5
    20: "deep",     # 6-19
    999: "farm",    # 20+
}

TIER_AGENT_LIMITS = {
    "light": {"agents": 1, "critics": 1, "model": "haiku"},
    "standard": {"agents": 4, "critics": 2, "model": "sonnet"},
    "deep": {"agents": 8, "critics": 3, "model": "opus"},
    "farm": {"agents": 8, "critics": 1, "model": "sonnet"},
}


def detect_tier_from_keywords(description: str) -> tuple[str | None, str]:
    """Match task description against keyword patterns.

    Returns (tier, matched_keyword) or (None, "") if no match.
    """
    desc_lower = description.lower()
    for tier, patterns in TIER_KEYWORDS.items():
        for pattern in patterns:
            match = re.search(pattern, desc_lower)
            if match:
                return tier, match.group()
    return None, ""


def detect_tier_from_files(file_count: int) -> str:
    """Determine tier based on number of files affected."""
    for threshold, tier in sorted(TIER_FILE_THRESHOLDS.items()):
        if file_count <= threshold:
            return tier
    return "deep"


def resolve_tier(keyword_tier: str | None, file_tier: str, description: str) -> tuple[str, str]:
    """Resolve final tier from keyword and file signals.

    Returns (tier, reasoning).
    """
    tier_order = ["light", "standard", "deep", "farm"]

    if keyword_tier and file_tier:
        # Take the higher tier (more conservative)
        ki = tier_order.index(keyword_tier) if keyword_tier in tier_order else 1
        fi = tier_order.index(file_tier)
        final = tier_order[max(ki, fi)]
        reasoning = f"keyword='{keyword_tier}', files='{file_tier}' → resolved to '{final}'"
    elif keyword_tier:
        final = keyword_tier
        reasoning = f"keyword match → '{final}'"
    elif file_tier:
        final = file_tier
        reasoning = f"file count → '{final}'"
    else:
        final = "standard"
        reasoning = "no clear signal → default 'standard'"

    # Uncertainty escalation: vague descriptions bump one tier
    vague_signals = [r"\bmaybe\b", r"\bnot sure\b", r"\bexplore\b", r"\binvestigate\b", r"\btry\b"]
    is_vague = any(re.search(p, description.lower()) for p in vague_signals)
    if is_vague and final != "deep":
        idx = tier_order.index(final)
        final = tier_order[min(idx + 1, 2)]  # cap at deep
        reasoning += " + uncertainty escalation (+1)"

    return final, reasoning


# --- L_task Difficulty Model (ASI-Evolve, arXiv:2603.29640) ---

C_EXEC_SCORES = {"none": 0, "light": 1, "heavy": 2}
S_SPACE_SCORES = {"narrow": 0, "moderate": 1, "broad": 2, "unknown": 3}
D_FEEDBACK_SCORES = {"strong": 0, "weak": 1, "manual": 2}

LTASK_TIER_THRESHOLDS = [(1, "light"), (3, "standard"), (5, "deep"), (7, "farm")]


def compute_ltask(c_exec: str, s_space: str, d_feedback: str) -> dict:
    """Compute L_task difficulty score and recommended tier.

    L_task = <C_exec, S_space, D_feedback> — three independent dimensions
    summed to derive tier assignment. ASI-Evolve integration.
    """
    scores = {
        "c_exec": C_EXEC_SCORES.get(c_exec, 1),
        "s_space": S_SPACE_SCORES.get(s_space, 1),
        "d_feedback": D_FEEDBACK_SCORES.get(d_feedback, 1),
    }
    total = sum(scores.values())

    recommended_tier = "deep"  # default
    for threshold, tier in LTASK_TIER_THRESHOLDS:
        if total <= threshold:
            recommended_tier = tier
            break

    return {
        "ltask": {
            "c_exec": c_exec,
            "s_space": s_space,
            "d_feedback": d_feedback,
            "scores": scores,
            "total": total,
            "recommended_tier": recommended_tier,
        },
        "limits": TIER_AGENT_LIMITS[recommended_tier],
    }


def compute_roi(total_subtasks: int, independent_subtasks: int, agent_count: int) -> dict:
    """Compute Amdahl-based ROI for agent parallelization.

    Returns: {parallelizability, theoretical_speedup, estimated_speedup,
              cost_multiplier, roi, recommendation}
    """
    if total_subtasks == 0:
        return {"error": "total_subtasks must be > 0"}

    p = independent_subtasks / total_subtasks  # parallelizability
    n = max(agent_count, 1)

    theoretical_speedup = 1.0 / ((1.0 - p) + (p / n))
    estimated_speedup = theoretical_speedup * 0.75  # empirical discount
    cost_multiplier = n * 1.15  # 15% coordination overhead
    roi = estimated_speedup / cost_multiplier

    # Amdahl cap: if serial > 30%, cap at standard
    serial_fraction = (total_subtasks - independent_subtasks) / total_subtasks
    amdahl_cap = serial_fraction > 0.3

    if roi < 0.5:
        recommendation = "DOWNGRADE — ROI too low, reduce agent count"
    elif amdahl_cap:
        recommendation = "CAP_STANDARD — >30% serial dependencies, cap tier at standard"
    else:
        recommendation = "PROCEED"

    return {
        "parallelizability": round(p, 2),
        "theoretical_speedup": round(theoretical_speedup, 2),
        "estimated_speedup": round(estimated_speedup, 2),
        "cost_multiplier": round(cost_multiplier, 2),
        "roi": round(roi, 2),
        "serial_fraction": round(serial_fraction, 2),
        "amdahl_cap": amdahl_cap,
        "recommendation": recommendation,
    }


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    # L_task mode (ASI-Evolve)
    if sys.argv[1] == "--ltask":
        c_exec = "light"
        s_space = "moderate"
        d_feedback = "weak"
        args = sys.argv[2:]
        i = 0
        while i < len(args):
            if args[i] == "--c-exec" and i + 1 < len(args):
                c_exec = args[i + 1]
                i += 2
            elif args[i] == "--s-space" and i + 1 < len(args):
                s_space = args[i + 1]
                i += 2
            elif args[i] == "--d-feedback" and i + 1 < len(args):
                d_feedback = args[i + 1]
                i += 2
            else:
                i += 1
        result = compute_ltask(c_exec, s_space, d_feedback)
        print(json.dumps(result, indent=2))
        return

    # ROI mode
    if sys.argv[1] == "--roi":
        if len(sys.argv) < 5:
            print("Usage: --roi <total> <independent> <agents>", file=sys.stderr)
            sys.exit(1)
        result = compute_roi(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
        print(json.dumps(result, indent=2))
        return

    # Tier detection mode
    description = sys.argv[1]
    file_count = int(sys.argv[2]) if len(sys.argv) >= 3 else 0

    keyword_tier, matched = detect_tier_from_keywords(description)
    file_tier = detect_tier_from_files(file_count) if file_count > 0 else ""
    final_tier, reasoning = resolve_tier(keyword_tier, file_tier, description)

    result = {
        "task": description,
        "file_count": file_count,
        "keyword_match": {"tier": keyword_tier, "keyword": matched} if keyword_tier else None,
        "file_match": file_tier if file_tier else None,
        "recommended_tier": final_tier,
        "reasoning": reasoning,
        "limits": TIER_AGENT_LIMITS[final_tier],
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

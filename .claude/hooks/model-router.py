#!/usr/bin/env python3
"""PreToolUse hook: Intelligent model routing for Agent tool calls.

Analyzes agent prompt signals to recommend optimal model selection.
Injects additionalContext with routing recommendation — does NOT block.

Signals analyzed:
- WRITE manifest file count (0-1 → haiku, 2-5 → sonnet, 6+ → opus)
- Keywords (security/auth/payment → opus, rename/format/lint → haiku)
- FAILED context → upgrade +1 tier
- Explicit model override → respect, but warn if signals disagree

Reads: model-routing.json for cross-session performance data.
Writes: model-routing.json (increment routing_count only).
"""

import json
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PERF_FILE = Path(".claude/memory/optstate/model-routing.json")

# --- Signal extraction ---

# Keywords that strongly signal model level
OPUS_KEYWORDS = re.compile(
    r"\b(security|auth|payment|credential|encryption|permission|"
    r"cross-cutting|architect|redesign)\b",
    re.IGNORECASE,
)
HAIKU_KEYWORDS = re.compile(
    r"\b(rename|format|lint|typo|simple|mechanical|"
    r"single.file|straightforward|one.liner|boilerplate)\b",
    re.IGNORECASE,
)
FAILURE_SIGNAL = re.compile(r"\bFAILED\b|\bfailed\b|\bBLOCKED\b|\berror\b.*\bprevious\b", re.IGNORECASE)

MODEL_HIERARCHY = ["haiku", "sonnet", "opus"]


def extract_write_files(prompt: str) -> list[str]:
    """Extract WRITE manifest files from agent prompt."""
    files = []
    in_write = False
    for line in prompt.splitlines():
        stripped = line.strip()
        if stripped.startswith("- WRITE:") or stripped.startswith("WRITE:"):
            in_write = True
            # Inline list: WRITE: [file1, file2]
            bracket_match = re.search(r"\[(.+?)\]", stripped)
            if bracket_match:
                files.extend(
                    f.strip().strip("'\"")
                    for f in bracket_match.group(1).split(",")
                    if f.strip()
                )
                in_write = False
        elif in_write:
            if stripped.startswith("- READ:") or stripped.startswith("- FORBIDDEN:"):
                in_write = False
            elif stripped.startswith("- ") or stripped.startswith("* "):
                files.append(stripped.lstrip("-* ").strip())
            elif not stripped:
                in_write = False
    return files


def upgrade_model(model: str) -> str:
    """Upgrade model one tier."""
    idx = MODEL_HIERARCHY.index(model) if model in MODEL_HIERARCHY else 1
    return MODEL_HIERARCHY[min(idx + 1, len(MODEL_HIERARCHY) - 1)]


def recommend_model(prompt: str) -> tuple[str, str]:
    """Analyze prompt and return (recommended_model, reasoning)."""
    write_files = extract_write_files(prompt)
    file_count = len(write_files)

    # Start from file-count heuristic
    if file_count <= 1:
        base_model = "haiku"
        reason = f"{file_count} file(s) in WRITE manifest"
    elif file_count <= 5:
        base_model = "sonnet"
        reason = f"{file_count} files in WRITE manifest"
    else:
        base_model = "opus"
        reason = f"{file_count} files in WRITE manifest (complex)"

    # Keyword overrides
    opus_hits = OPUS_KEYWORDS.findall(prompt[:3000])  # scan first 3K chars
    haiku_hits = HAIKU_KEYWORDS.findall(prompt[:3000])

    if opus_hits and not haiku_hits:
        if base_model != "opus":
            base_model = "opus"
            reason = f"keyword signal: {', '.join(opus_hits[:3])}"
    elif haiku_hits and not opus_hits and file_count <= 2:
        base_model = "haiku"
        reason = f"keyword signal: {', '.join(haiku_hits[:3])}"

    # Failure escalation
    if FAILURE_SIGNAL.search(prompt[:5000]):
        old_model = base_model
        base_model = upgrade_model(base_model)
        if old_model != base_model:
            reason += f" + failure escalation ({old_model}→{base_model})"

    # Performance data adjustment
    perf = load_perf_data()
    if perf and file_count <= 1:
        haiku_stats = perf.get("by_subtask_type", {}).get("single_file_edit", {}).get("haiku", {})
        if haiku_stats.get("attempts", 0) >= 5:
            success_rate = haiku_stats.get("success", 0) / max(haiku_stats["attempts"], 1)
            if success_rate < 0.5:
                base_model = "sonnet"
                reason += f" + perf data: haiku success rate {success_rate:.0%} on single_file"

    return base_model, reason


def load_perf_data() -> dict | None:
    """Load performance data from optstate."""
    try:
        return json.loads(PERF_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def update_routing_count():
    """Increment total routing count."""
    try:
        data = json.loads(PERF_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        data = {"last_updated": "", "total_routings": 0, "by_subtask_type": {}}

    from datetime import date
    data["total_routings"] = data.get("total_routings", 0) + 1
    data["last_updated"] = str(date.today())
    PERF_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    tool_name = os.environ.get("CLAUDE_TOOL_NAME", "")
    if tool_name != "Agent":
        sys.exit(0)

    try:
        raw = sys.stdin.read().strip()
        tool_input = json.loads(raw) if raw else {}
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    prompt = tool_input.get("prompt", "")
    if not prompt or len(prompt) < 50:
        sys.exit(0)  # Too short to analyze meaningfully

    explicit_model = tool_input.get("model", "")
    recommended, reason = recommend_model(prompt)

    # Update routing count
    try:
        update_routing_count()
    except Exception:
        pass  # Non-critical

    # If model was explicitly set and matches recommendation — silent
    if explicit_model and explicit_model == recommended:
        sys.exit(0)

    # If no model set — recommend
    if not explicit_model:
        msg = f"[model-router] Recommended model: {recommended} ({reason}). No model was specified — consider adding model: \"{recommended}\"."
        print(json.dumps({"additionalContext": msg}))
        sys.exit(0)

    # If model was set but signals strongly disagree — warn
    explicit_idx = MODEL_HIERARCHY.index(explicit_model) if explicit_model in MODEL_HIERARCHY else -1
    recommended_idx = MODEL_HIERARCHY.index(recommended) if recommended in MODEL_HIERARCHY else -1

    if explicit_idx >= 0 and recommended_idx >= 0:
        gap = abs(explicit_idx - recommended_idx)
        if gap >= 2:
            # Strong disagreement (e.g., haiku assigned but opus recommended)
            msg = (
                f"[model-router] Warning: explicit model={explicit_model} but signals suggest {recommended} ({reason}). "
                f"Gap={gap} tiers. Consider adjusting."
            )
            print(json.dumps({"additionalContext": msg}))
        elif gap == 1 and recommended_idx > explicit_idx:
            # Mild under-assignment (e.g., haiku but sonnet recommended)
            msg = (
                f"[model-router] Note: {explicit_model} assigned, {recommended} might be better ({reason})."
            )
            print(json.dumps({"additionalContext": msg}))
        # If explicit is HIGHER than recommended — no warning (user chose stronger, fine)


if __name__ == "__main__":
    main()

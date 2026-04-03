#!/usr/bin/env python3
"""UserPromptSubmit hook: associative recall via spreading activation.

Hippocampus-inspired (Phase 2d): supplements keyword-based memory-whisper
with graph-based associative recall for cross-concept discovery.

Runs AFTER memory-whisper.py (keyword recall). Adds graph-based recall
that finds concepts memory-whisper misses due to indirect associations.

Must complete in <3s. No LLM calls.
"""
import json
import os
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Profile gate
_levels = {'minimal': 1, 'standard': 2, 'strict': 3}
if _levels.get(os.environ.get('STOPA_HOOK_PROFILE', 'standard'), 2) < _levels.get('standard', 2):
    sys.exit(0)

# Add hooks/lib to path for importing associative_engine
sys.path.insert(0, str(Path(__file__).parent / "lib"))

try:
    from associative_engine import load_graph, activate, compress_to_packet
except ImportError:
    sys.exit(0)  # Engine not available — skip silently

GRAPH_PATH = Path(".claude/memory/concept-graph.json")
# Token budget for associative recall (separate from memory-whisper's 1500)
# Total injection should be <2500 tokens combined
ASSOC_TOKEN_BUDGET = 800


def extract_prompt(hook_input: dict) -> str:
    """Extract user prompt text from hook input."""
    message = hook_input.get("message", {})
    if isinstance(message, dict):
        content = message.get("content", "")
        if isinstance(content, list):
            content = " ".join(
                c.get("text", "") for c in content if isinstance(c, dict)
            )
    elif isinstance(message, str):
        content = message
    else:
        content = str(message)
    return content


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    prompt = extract_prompt(hook_input)
    if not prompt or len(prompt) < 10:
        return

    # Skip slash commands
    if prompt.strip().startswith("/"):
        return

    # Check graph exists and is fresh enough (max 7 days old)
    if not GRAPH_PATH.exists():
        return

    try:
        stat = GRAPH_PATH.stat()
        age_days = (time.time() - stat.st_mtime) / 86400
        if age_days > 7:
            return  # Graph too stale — needs rebuild
    except OSError:
        return

    # Load graph and activate
    start = time.monotonic()
    graph = load_graph()
    if not graph.get("entities"):
        return

    # Get workspace for context boosting
    cwd = str(Path.cwd())

    nodes = activate(prompt[:500], workspace=cwd, graph=graph)
    elapsed_ms = int((time.monotonic() - start) * 1000)

    if not nodes:
        return

    # Only output if we have high-confidence associations
    # (activation > 0.25 for at least one node)
    if nodes[0].activation < 0.25:
        return

    packet = compress_to_packet(nodes, max_tokens=ASSOC_TOKEN_BUDGET)
    if not packet or len(packet) < 30:
        return

    # Add timing info
    packet = packet.replace(
        "[Associative recall",
        f"[Associative recall ({elapsed_ms}ms)"
    )

    print(json.dumps({"additionalContext": packet}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # Never block prompt submission

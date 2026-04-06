#!/usr/bin/env python3
"""
PostToolUse hook: tracks generative API calls (fal.ai, ElevenLabs).
Accumulates stats in .claude/memory/intermediate/generation-stats.json.
After N generations, suggests running /prompt-evolve.

Matched on: Bash (detects fal_client.subscribe/submit calls)
"""

import json
import os
import sys
import re
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

STATS_FILE = Path(__file__).parent.parent / "memory" / "intermediate" / "generation-stats.json"
EVOLVE_THRESHOLD = 10  # suggest /prompt-evolve after N generations


def load_stats():
    if STATS_FILE.exists():
        try:
            return json.loads(STATS_FILE.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "total_generations": 0,
        "since_last_evolve": 0,
        "last_evolve": None,
        "categories": {},
        "history": []
    }


def save_stats(stats):
    STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATS_FILE.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding='utf-8')


def detect_generation(tool_input: str, tool_output: str) -> dict | None:
    """Detect if a Bash call was a generative API call."""
    combined = (tool_input or "") + (tool_output or "")

    # fal.ai image generation
    if "nano-banana" in combined and ("fal_client" in combined):
        return {"api": "fal.ai", "type": "image", "category": "image_styles"}

    # fal.ai video generation (Kling)
    if "kling-video" in combined and ("fal_client" in combined):
        return {"api": "fal.ai", "type": "video", "category": "video"}

    # ElevenLabs TTS
    if "elevenlabs" in combined.lower() and "text-to-speech" in combined:
        return {"api": "elevenlabs", "type": "tts", "category": "voice"}

    # google.genai image
    if "genai" in combined and ("generate_content" in combined or "generate_image" in combined):
        return {"api": "gemini", "type": "image", "category": "image_styles"}

    return None


def main():
    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = hook_input.get("tool_name", "")
    if tool_name != "Bash":
        return

    tool_input = json.dumps(hook_input.get("tool_input", {}))
    tool_output = hook_input.get("tool_output", "")
    if isinstance(tool_output, dict):
        tool_output = json.dumps(tool_output)

    detection = detect_generation(tool_input, tool_output)
    if not detection:
        return

    stats = load_stats()
    stats["total_generations"] += 1
    stats["since_last_evolve"] += 1

    cat = detection["category"]
    if cat not in stats["categories"]:
        stats["categories"][cat] = 0
    stats["categories"][cat] += 1

    # Keep last 50 entries in history
    stats["history"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "api": detection["api"],
        "type": detection["type"],
        "category": cat,
    })
    stats["history"] = stats["history"][-50:]

    save_stats(stats)

    # Suggest optimization after threshold
    if stats["since_last_evolve"] >= EVOLVE_THRESHOLD:
        top_cat = max(stats["categories"], key=stats["categories"].get)
        print(json.dumps({
            "result": f"[prompt-evolve] {stats['since_last_evolve']} generations since last optimization. "
                      f"Top category: {top_cat} ({stats['categories'][top_cat]}x). "
                      f"Consider running `/prompt-evolve {top_cat}` to optimize templates.",
            "suppressOutput": False
        }))


if __name__ == "__main__":
    main()

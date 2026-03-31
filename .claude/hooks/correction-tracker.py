#!/usr/bin/env python3
"""UserPromptSubmit hook: detect user corrections and log to corrections.jsonl.

Auto-promotes to critical-patterns.md suggestion when same pattern corrected 2+ times.
Corrections are the most valuable signal for the evolution system.

Detection: Czech + English correction phrases.
Input: stdin JSON {"prompt": "..."} (Claude Code UserPromptSubmit format)
Output: stdout (injected into Claude context as system message)
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import sys, os
_levels = {'minimal': 1, 'standard': 2, 'strict': 3}
if _levels.get(os.environ.get('STOPA_HOOK_PROFILE', 'standard'), 2) < _levels.get('standard', 2):
    sys.exit(0)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

CORRECTIONS_LOG = Path(".claude/memory/corrections.jsonl")

# Correction signal patterns — Czech + English
# Ordered from most specific to most general to reduce false positives
CORRECTION_SIGNALS_RAW = [
    # Czech — high confidence
    r"\bnikdy\b.{0,30}\b(nedělej|nepsat|nepiš|nepoužívej)\b",
    r"\b(nedělej|nepiš|nepsat|nepoužívej)\b",
    r"\b(řekl jsem|říkal jsem|říkám)\b",
    r"\bjak jsem (řekl|říkal|psal)\b",
    r"\b(to jsem nechtěl|to nechci)\b",
    r"\b(špatně|špatný přístup|špatná cesta)\b",
    r"\b(přestaň|stop)\b.{0,20}\b(dělat|psát|používat)\b",
    r"\bneděláme tak\b",
    r"\bmy\b.{0,10}\b(vždy|nikdy|nepoužíváme|používáme)\b",
    r"\bmísto toho\b.{0,10}\b(vždy|používej|piš)\b",
    # English — high confidence
    r"\bdon'?t\b.{0,20}\b(do|use|write|add|create)\b",
    r"\bnever\b.{0,20}\b(do|use|write|add|put)\b",
    r"\bi told you\b",
    r"\bwe don'?t\b",
    r"\bwe never\b",
    r"\bnot like that\b",
    r"\bstop\b.{0,20}\b(doing|using|writing|adding)\b",
    r"\bthat'?s wrong\b",
    r"\bwrong approach\b",
    r"\bno[,!]\s+\w",  # "No, use X instead"
]

CORRECTION_RE = re.compile(
    "|".join(CORRECTION_SIGNALS_RAW),
    re.IGNORECASE,
)

# Minimum prompt length to avoid false positives on short "no" messages
MIN_PROMPT_LEN = 15

# Similarity: keyword overlap threshold for duplicate detection
SIMILARITY_MIN_OVERLAP = 2
SIMILARITY_MIN_WORD_LEN = 4


def read_prompt() -> str:
    """Read user prompt from stdin JSON (UserPromptSubmit format)."""
    try:
        raw = sys.stdin.buffer.read()
        if raw:
            data = json.loads(raw.decode("utf-8", errors="replace"))
            return data.get("prompt", "")
    except Exception:
        pass
    return ""


def extract_correction_sentence(prompt: str) -> str:
    """Extract the most relevant correction sentence from the prompt."""
    sentences = re.split(r"[.!?\n]+", prompt)
    for sentence in sentences:
        if CORRECTION_RE.search(sentence) and len(sentence.strip()) >= 8:
            return sentence.strip()[:200]
    return prompt.strip()[:200]


def extract_keywords(text: str) -> set[str]:
    """Extract meaningful keywords for similarity comparison."""
    words = re.findall(r"\b\w{" + str(SIMILARITY_MIN_WORD_LEN) + r",}\b", text.lower())
    # Remove common stop words
    stop = {"that", "this", "with", "from", "have", "will", "when", "then",
            "also", "into", "just", "should", "would", "could", "jsem", "nebo",
            "jako", "není", "jsou", "jsou", "bylo", "bylo", "jejich", "tohle"}
    return set(words) - stop


def find_similar_correction(summary: str) -> dict | None:
    """Find a previous similar correction in corrections.jsonl."""
    if not CORRECTIONS_LOG.exists():
        return None

    new_words = extract_keywords(summary)
    if len(new_words) < 2:
        return None

    try:
        text = CORRECTIONS_LOG.read_text(encoding="utf-8", errors="replace")
        lines = [l for l in text.strip().split("\n") if l.strip()]
        # Check most recent 100 entries
        for line in reversed(lines[-100:]):
            try:
                entry = json.loads(line)
                old_words = extract_keywords(entry.get("summary", ""))
                overlap = new_words & old_words
                if len(overlap) >= SIMILARITY_MIN_OVERLAP:
                    return entry
            except (json.JSONDecodeError, KeyError):
                continue
    except Exception:
        pass

    return None


def log_correction(summary: str, prompt_snippet: str, times: int) -> dict:
    """Append correction entry to corrections.jsonl."""
    CORRECTIONS_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
        "prompt_snippet": prompt_snippet[:300],
        "times_corrected": times,
        "verify_check": "manual",  # Updated by /evolve when pattern is clear
    }
    with CORRECTIONS_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # Prune to last 500 entries
    try:
        lines = CORRECTIONS_LOG.read_text(encoding="utf-8").strip().split("\n")
        if len(lines) > 500:
            CORRECTIONS_LOG.write_text(
                "\n".join(lines[-500:]) + "\n", encoding="utf-8"
            )
    except Exception:
        pass

    return entry


def generate_eval_case(summary: str, prompt_snippet: str, times: int) -> str | None:
    """Auto-generate a skeleton eval case from a repeated correction.

    Creates case files in .claude/evals/<component>/case-auto-<N>/ with:
    - input.md: context that triggered the correction
    - expected.md: the corrected behavior
    - eval.md: check that the bad behavior is NOT repeated
    Returns the case directory path, or None if generation failed.
    """
    evals_dir = Path(".claude/evals")

    # Infer component from correction keywords
    component = "general"
    component_map = {
        "skill": "skill", "hook": "hook", "memory": "memory",
        "orchestrat": "orchestration", "pipeline": "pipeline",
        "prompt": "prompt", "config": "config",
    }
    lower_summary = summary.lower()
    for keyword, comp in component_map.items():
        if keyword in lower_summary:
            component = comp
            break

    case_dir = evals_dir / component
    case_dir.mkdir(parents=True, exist_ok=True)

    # Find next auto case number
    existing = [d.name for d in case_dir.iterdir() if d.is_dir() and d.name.startswith("case-auto-")]
    next_num = len(existing) + 1
    case_path = case_dir / f"case-auto-{next_num:03d}"
    case_path.mkdir(parents=True, exist_ok=True)

    # Write input.md
    (case_path / "input.md").write_text(
        f"---\nsource: auto-correction\ntimes_corrected: {times}\n---\n\n"
        f"# Context\n\n{prompt_snippet[:500]}\n",
        encoding="utf-8",
    )

    # Write expected.md
    (case_path / "expected.md").write_text(
        f"# Expected Behavior\n\n"
        f"The correction states: {summary}\n\n"
        f"The output should follow this corrected behavior.\n",
        encoding="utf-8",
    )

    # Write eval.md
    (case_path / "eval.md").write_text(
        f"# Eval Criteria\n\n"
        f"- [ ] Output does NOT repeat the corrected mistake\n"
        f"- [ ] Behavior aligns with: {summary}\n"
        f"- [ ] No regression in related functionality\n",
        encoding="utf-8",
    )

    return str(case_path)


def main():
    prompt = read_prompt()
    if not prompt or len(prompt) < MIN_PROMPT_LEN:
        sys.exit(0)

    # Check if this looks like a correction
    if not CORRECTION_RE.search(prompt):
        sys.exit(0)

    summary = extract_correction_sentence(prompt)
    similar = find_similar_correction(summary)
    times = (similar["times_corrected"] + 1) if similar else 1

    log_correction(summary, prompt, times)

    # Notify Claude when this is a repeated correction
    if similar:
        print(f"\n[correction-tracker] Opakovaná korekce ({times}. výskyt):")
        print(f"  1. výskyt: {similar['summary']}")
        print(f"  Nový:      {summary}")
        print(
            f"  → Tato korekce se opakuje. Zvažte: /scribe pro zachycení jako learning,"
            f"\n    nebo /evolve pro analýzu a graduaci do critical-patterns.md."
        )

        # Auto-generate eval case from repeated corrections (times >= 2)
        if times >= 2:
            try:
                case_path = generate_eval_case(summary, prompt, times)
                if case_path:
                    print(f"  → Auto-generated eval case: {case_path}")
                    print(f"    Use /self-evolve to train against this pattern.")
            except Exception:
                pass  # Don't break the hook on eval generation failure

    sys.exit(0)


if __name__ == "__main__":
    main()

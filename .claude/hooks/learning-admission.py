#!/usr/bin/env python3
"""Write-time admission control for learnings — soft gate + contradiction check.

PostToolUse hook: triggers on Write operations to .claude/memory/learnings/.
Inspired by A-MAC (arXiv:2603.04549) — preventing bad memories from entering
is more effective than retroactive correction.

Outputs warnings to stdout (soft gate — does NOT block writes).
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

LEARNINGS_DIR = Path(".claude/memory/learnings")

# Source reputation scores (from scribe SKILL.md salience formula)
SOURCE_REPUTATION = {
    "user_correction": 1.0,
    "critic_finding": 0.8,
    "auto_pattern": 0.6,
    "external_research": 0.5,
    "agent_generated": 0.4,
}

# Contradiction signal words — opposing pairs
# Each tuple: (set_A, set_B) — if new has A words and existing has B (or vice versa),
# it's a potential contradiction on the same topic (same component + 2+ tags).
CONTRADICTION_PAIRS = [
    # Core: never vs always
    ({"never", "nikdy", "don't", "avoid", "zakázáno", "nesmí"},
     {"always", "vždy", "must", "require", "povinné", "musí"}),
    # Lifecycle: remove vs keep
    ({"remove", "delete", "smaž", "odstraň", "drop"},
     {"keep", "preserve", "zachovej", "ponech", "retain"}),
    # Toggle: disable vs enable
    ({"disable", "vypni", "off", "deactivate"},
     {"enable", "zapni", "on", "activate"}),
    # Preference: prefer vs discourage
    ({"prefer", "recommend", "doporučuj", "upřednostni"},
     {"avoid", "discourage", "vyhni", "nedoporučuj", "nepoužívej"}),
    # Execution: parallel vs sequential
    ({"parallel", "concurrent", "paralelně", "simultaneously"},
     {"sequential", "serial", "sekvenčně", "one-by-one", "postupně"}),
    # Complexity: simple vs complex
    ({"simple", "minimal", "jednoduchý", "lightweight"},
     {"complex", "comprehensive", "komplexní", "heavyweight"}),
    # Ordering: before vs after
    ({"before", "first", "předem", "nejdřív"},
     {"after", "last", "potom", "nakonec"}),
    # Scope: skip vs require
    ({"skip", "přeskoč", "optional", "volitelný"},
     {"require", "mandatory", "povinný", "enforce", "vyžaduj"}),
]

# Regex patterns for verb-extraction contradiction detection
# Detects "never/don't <verb>" vs "always/must <same-verb>" — semantic, not keyword
NEGATION_PATTERN = re.compile(
    r"\b(?:never|nikdy|don'?t|do not|nepoužívej|nepiš|nespouštěj)\s+(\w{4,})",
    re.IGNORECASE,
)
OBLIGATION_PATTERN = re.compile(
    r"\b(?:always|vždy|must|require|používej|piš|spouštěj)\s+(\w{4,})",
    re.IGNORECASE,
)


def parse_yaml_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter as flat string dict."""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    yaml_block = content[3:end].strip()
    result = {}
    for line in yaml_block.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip()
    return result


def parse_tags(meta: dict) -> set:
    """Parse tags field from YAML (handles [tag1, tag2] format)."""
    raw = meta.get("tags", "")
    if not raw:
        return set()
    cleaned = raw.strip("[]")
    return {t.strip().strip("'\"") for t in cleaned.split(",") if t.strip()}


def extract_keywords(text: str, min_len: int = 4) -> set:
    """Extract significant words from text for dedup comparison."""
    words = re.findall(r'\b[a-záčďéěíňóřšťúůýž]{%d,}\b' % min_len, text.lower())
    stop = {"that", "this", "with", "from", "have", "been", "will", "when",
            "jsou", "není", "jako", "nebo", "proto", "pokud", "musí", "může"}
    return {w for w in words if w not in stop}


def compute_salience(meta: dict, existing_learnings: list[dict]) -> tuple[float, str]:
    """Compute salience score = source_reputation × novelty.

    Returns (score, reason) tuple.
    """
    source = meta.get("source", "auto_pattern")
    reputation = SOURCE_REPUTATION.get(source, 0.6)

    # Novelty check: find near-duplicates by component + tags + summary keywords
    new_component = meta.get("component", "")
    new_tags = parse_tags(meta)
    new_summary = meta.get("summary", "").strip("'\"")
    new_keywords = extract_keywords(new_summary)

    novelty = 1.0
    duplicate_of = None

    for existing in existing_learnings:
        ex_component = existing.get("component", "")
        ex_tags = parse_tags(existing)
        ex_summary = existing.get("summary", "").strip("'\"")
        ex_keywords = extract_keywords(ex_summary)

        # Same component + 2+ shared tags + 3+ shared keywords = near-duplicate
        if (new_component == ex_component
                and len(new_tags & ex_tags) >= 2
                and len(new_keywords & ex_keywords) >= 3):
            novelty = 0.1
            duplicate_of = existing.get("_filename", "unknown")
            break

    score = reputation * novelty
    reason = ""
    if novelty < 0.5:
        reason = f"near-duplicate of {duplicate_of}"
    elif reputation < 0.5:
        reason = f"low-reputation source ({source})"

    return score, reason


def check_contradictions(meta: dict, summary: str,
                          existing_learnings: list[dict]) -> list[str]:
    """Check if new learning contradicts existing ones.

    Two detection methods:
    1. Keyword pairs: hardcoded opposing word sets (fast, high precision)
    2. Verb extraction: "never <verb>" vs "always <same-verb>" (semantic, broader)

    Returns list of warning strings (empty = no contradictions found).
    """
    warnings = []
    new_component = meta.get("component", "")
    new_tags = parse_tags(meta)
    summary_lower = summary.lower()

    # Pre-extract negated/obligated verbs from new learning
    new_negated = {m.group(1).lower() for m in NEGATION_PATTERN.finditer(summary_lower)}
    new_obligated = {m.group(1).lower() for m in OBLIGATION_PATTERN.finditer(summary_lower)}

    for existing in existing_learnings:
        ex_component = existing.get("component", "")
        ex_tags = parse_tags(existing)
        ex_summary = existing.get("summary", "").strip("'\"").lower()

        # Only check learnings with same component AND 2+ shared tags
        if new_component != ex_component or len(new_tags & ex_tags) < 2:
            continue

        filename = existing.get("_filename", "unknown")
        found = False

        # Method 1: keyword pair detection
        for set_a, set_b in CONTRADICTION_PAIRS:
            new_has_a = any(w in summary_lower for w in set_a)
            new_has_b = any(w in summary_lower for w in set_b)
            ex_has_a = any(w in ex_summary for w in set_a)
            ex_has_b = any(w in ex_summary for w in set_b)

            if (new_has_a and ex_has_b) or (new_has_b and ex_has_a):
                warnings.append(
                    f"[hard] Contradiction with {filename}: "
                    f"opposing recommendations detected. "
                    f"Consider adding 'supersedes: {filename}' if this replaces it."
                )
                found = True
                break

        if found:
            continue

        # Method 2: verb-extraction detection
        # "never use X" (new) vs "always use X" (existing) or vice versa
        ex_negated = {m.group(1).lower() for m in NEGATION_PATTERN.finditer(ex_summary)}
        ex_obligated = {m.group(1).lower() for m in OBLIGATION_PATTERN.finditer(ex_summary)}

        # New negates a verb that existing obligates (or vice versa)
        conflict_verbs = (new_negated & ex_obligated) | (new_obligated & ex_negated)
        if conflict_verbs:
            verbs_str = ", ".join(sorted(conflict_verbs))
            warnings.append(
                f"[soft] Possible verb contradiction with {filename}: "
                f"conflicting stance on '{verbs_str}'. "
                f"Review both learnings to determine if one supersedes the other."
            )

    return warnings


def load_existing_learnings() -> list[dict]:
    """Load YAML frontmatter from all existing learning files."""
    if not LEARNINGS_DIR.exists():
        return []
    learnings = []
    for f in LEARNINGS_DIR.glob("*.md"):
        if f.name in ("critical-patterns.md", "index-general.md",
                       "block-manifest.json", "ecosystem-scan.md"):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        meta = parse_yaml_frontmatter(content)
        if meta:
            meta["_filename"] = f.name
            learnings.append(meta)
    return learnings


def main():
    """Hook entry point — reads tool_input from stdin."""
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Only trigger on Write/Edit to learnings/
    if tool_name not in ("Write", "Edit"):
        return

    file_path = tool_input.get("file_path", "")
    if "learnings/" not in file_path.replace("\\", "/"):
        return

    # Skip non-learning files
    basename = Path(file_path).name
    if basename in ("critical-patterns.md", "index-general.md",
                     "block-manifest.json", "ecosystem-scan.md"):
        return

    # Read the just-written file
    target = Path(file_path)
    if not target.exists():
        return
    try:
        content = target.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return

    meta = parse_yaml_frontmatter(content)
    if not meta:
        return

    # Load existing learnings for comparison
    existing = load_existing_learnings()
    # Exclude self from comparison
    existing = [e for e in existing if e.get("_filename") != basename]

    messages = []

    # 1. Salience gate
    salience, reason = compute_salience(meta, existing)
    if salience < 0.2:
        messages.append(
            f"[admission-gate] LOW SALIENCE ({salience:.2f}): {reason}. "
            f"Consider if this learning adds enough value to keep."
        )
    elif salience < 0.4 and reason:
        messages.append(
            f"[admission-gate] Moderate salience ({salience:.2f}): {reason}."
        )

    # 2. Contradiction check
    summary = meta.get("summary", "").strip("'\"")
    contradictions = check_contradictions(meta, summary, existing)
    for warning in contradictions:
        messages.append(f"[contradiction-check] {warning}")

    # 3. Missing verify_check warning
    if not meta.get("verify_check"):
        messages.append(
            "[admission-gate] No verify_check field — "
            "rules without checks are wishes, rules with checks are guardrails."
        )

    # Output warnings (soft gate — informational only)
    if messages:
        for msg in messages:
            print(msg)


if __name__ == "__main__":
    main()

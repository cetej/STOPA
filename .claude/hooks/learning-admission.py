#!/usr/bin/env python3
"""Write-time admission control for learnings — configurable gate + contradiction check + origin tagging.

PostToolUse hook: triggers on Write operations to .claude/memory/learnings/.
Inspired by A-MAC (arXiv:2603.04549) — preventing bad memories from entering
is more effective than retroactive correction.

Gate mode (env var STOPA_ADMISSION_GATE):
  - soft (default): warnings only, never blocks writes
  - hard: blocks on hard contradiction, near-duplicate (novelty<0.2), or memory poisoning

Phase 2 defense (AI Agent Traps, DeepMind 2026-04-01):
  - Detects web-originated learnings via URL presence and source field
  - Caps confidence for web/agent-originated content at 0.6
  - Warns on trust escalation (web content with user_correction source)
  - Checks for instruction-like content in learning body (memory poisoning defense)
"""
import json
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

LEARNINGS_DIR = Path(".claude/memory/learnings")

# Gate mode: soft (warn) or hard (block on critical violations)
GATE_MODE = os.environ.get("STOPA_ADMISSION_GATE", "soft")

# Max confidence for web-originated or agent-generated learnings
# DeepMind AI Agent Traps: 0.1% data contamination achieves 80%+ memory poisoning
WEB_CONFIDENCE_CAP = 0.6
UNTRUSTED_SOURCES = {"external_research", "agent_generated"}

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


def detect_web_origin(content: str, meta: dict) -> tuple[bool, list[str]]:
    """Detect if a learning likely originated from web content.

    Checks:
    1. URLs in learning body (http/https links)
    2. Source field is external_research or agent_generated
    3. References to web tools (WebFetch, browse, fetch)
    4. Common web-content markers (HTML tags, DOM references)

    Returns (is_web_originated, reasons).
    """
    reasons = []
    body = content.split("---", 2)[-1] if content.startswith("---") else content
    body_lower = body.lower()

    # Check for URLs in body
    url_count = len(re.findall(r'https?://[^\s\)]+', body))
    if url_count >= 2:
        reasons.append(f"contains {url_count} URLs")

    # Check source field
    source = meta.get("source", "auto_pattern")
    if source in UNTRUSTED_SOURCES:
        reasons.append(f"source={source}")

    # Check for web tool references
    web_tool_markers = ["webfetch", "web search", "browse", "/fetch", "/deepresearch",
                        "brave_web_search", "get_page_text"]
    if any(marker in body_lower for marker in web_tool_markers):
        reasons.append("references web tools")

    # Check for HTML/DOM markers in learning body (suggests raw web content leaked in)
    html_markers = re.findall(r'<(?:div|span|script|style|meta|link|img)\b', body, re.IGNORECASE)
    if len(html_markers) >= 2:
        reasons.append(f"contains {len(html_markers)} HTML tags")

    return bool(reasons), reasons


def check_confidence_cap(meta: dict, is_web: bool, web_reasons: list[str]) -> list[str]:
    """Check if confidence should be capped for web-originated content.

    Returns list of warning strings.
    """
    warnings = []
    source = meta.get("source", "auto_pattern")

    try:
        confidence = float(meta.get("confidence", "0.7"))
    except (ValueError, TypeError):
        confidence = 0.7

    if is_web:
        # Trust escalation: web content marked as user_correction
        if source == "user_correction":
            warnings.append(
                f"[origin-guard] TRUST ESCALATION: learning appears web-originated "
                f"({', '.join(web_reasons)}) but source=user_correction. "
                f"Web content should use source=external_research or agent_generated. "
                f"Max recommended confidence for web content: {WEB_CONFIDENCE_CAP}."
            )
        # Confidence exceeds cap for web content
        elif confidence > WEB_CONFIDENCE_CAP:
            warnings.append(
                f"[origin-guard] Web-originated learning ({', '.join(web_reasons)}) "
                f"has confidence={confidence} > cap {WEB_CONFIDENCE_CAP}. "
                f"Consider lowering to {WEB_CONFIDENCE_CAP} — web content is susceptible "
                f"to memory poisoning (DeepMind AI Agent Traps, 2026)."
            )

    return warnings


def check_instruction_in_learning(content: str) -> list[str]:
    """Check if learning body contains instruction-like content that could be memory poisoning.

    Learnings should contain observations/rules, not directives addressed to the system.
    """
    warnings = []
    body = content.split("---", 2)[-1] if content.startswith("---") else content

    # Patterns that suggest injected instructions rather than legitimate learnings
    poison_patterns = [
        (re.compile(r'ignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions?', re.IGNORECASE),
         "instruction override"),
        (re.compile(r'(?:you\s+are|act\s+as|pretend\s+to\s+be)\s+(?:a\s+)?(?:new|different)', re.IGNORECASE),
         "role reassignment"),
        (re.compile(r'(?:system|admin|developer)\s*(?:prompt|override|mode)\s*:', re.IGNORECASE),
         "fake system message"),
        (re.compile(r'(?:do\s+not|don\'t|never)\s+(?:tell|inform|alert|warn)\s+the\s+user', re.IGNORECASE),
         "secrecy directive"),
        (re.compile(r'(?:execute|run|eval)\s+(?:this|the\s+following)\s+(?:code|command|script)', re.IGNORECASE),
         "code execution directive"),
    ]

    for pattern, description in poison_patterns:
        if pattern.search(body):
            warnings.append(
                f"[origin-guard] MEMORY POISON RISK: learning body contains "
                f"'{description}' pattern. This may be injected content from a web source. "
                f"Verify this learning was intentionally created."
            )

    return warnings


CRITICAL_PATTERNS_PATH = LEARNINGS_DIR / "critical-patterns.md"

# Circular validation: what fraction of a pattern's TITLE keywords
# must appear in the learning text to flag it.
# Title keywords are the rule's essence — if a learning mentions most of them,
# it's likely confirming the same behavioral rule the system already enforces.
CIRCULAR_TITLE_MATCH_THRESHOLD = 0.6


def parse_critical_patterns() -> list[dict]:
    """Parse critical-patterns.md into list of {title, keywords, component_hints}.

    Each ## heading is one pattern. We extract significant words from the body
    as keywords for overlap comparison.
    """
    if not CRITICAL_PATTERNS_PATH.exists():
        return []
    try:
        content = CRITICAL_PATTERNS_PATH.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    patterns = []
    current: dict | None = None

    for line in content.split("\n"):
        if line.startswith("## ") and not line.startswith("## ---"):
            if current and current.get("body"):
                current["keywords"] = extract_keywords(current["body"])
                patterns.append(current)
            title = line[3:].strip()
            current = {"title": title, "body": "", "keywords": set()}
        elif current is not None:
            current["body"] += " " + line

    # Don't forget the last pattern
    if current and current.get("body"):
        current["keywords"] = extract_keywords(current["body"])
        patterns.append(current)

    return patterns


def check_circular_validation(
    meta: dict, summary: str, content: str
) -> list[str]:
    """Detect if a new learning merely confirms an existing critical pattern.

    Acemoglu et al. (arXiv:2604.04906): endogenous feedback loops amplify bias
    when an aggregator trains on beliefs shaped by its own prior output.
    In STOPA: critical-patterns guide agent behavior → agent generates learnings
    → learnings confirm the pattern → /evolve strengthens the pattern. Circular.

    Detection: if >60% of new learning's significant keywords overlap with
    an existing critical pattern on the same component, flag it.
    Duplicate detection catches identical content; this catches *confirmatory* content
    that uses different words to validate the same behavioral rule.

    Returns list of warning strings.
    """
    warnings = []
    new_component = meta.get("component", "")
    new_tags = parse_tags(meta)

    # Combine summary + body keywords for richer comparison
    body = content.split("---", 2)[-1] if content.startswith("---") else content
    new_keywords = extract_keywords(summary) | extract_keywords(body)

    if len(new_keywords) < 3:
        return warnings  # Too few keywords to judge

    patterns = parse_critical_patterns()

    for pattern in patterns:
        # Use TITLE keywords as the pattern's essence — short, specific, high signal.
        # A learning that mentions most of a pattern's title words is likely
        # confirming the same behavioral rule.
        title_kw = extract_keywords(pattern["title"])
        if len(title_kw) < 2:
            continue

        matched = title_kw & new_keywords
        ratio = len(matched) / len(title_kw)

        if ratio >= CIRCULAR_TITLE_MATCH_THRESHOLD and len(matched) >= 2:
            warnings.append(
                f"[circular-risk] Learning matches {len(matched)}/{len(title_kw)} "
                f"title keywords of critical pattern '{pattern['title']}' "
                f"({', '.join(sorted(matched))}). "
                f"This may be circular validation — the agent behavior that "
                f"produced this learning was likely guided by the same pattern. "
                f"Consider: does this add INDEPENDENT evidence, "
                f"or just confirm behavior the system already enforces?"
            )
            break  # One flag is enough

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

    # 3. Circular validation detection (Acemoglu arXiv:2604.04906)
    circular_warnings = check_circular_validation(meta, summary, content)
    messages.extend(circular_warnings)

    # 4. Origin detection + confidence cap (Phase 2 — AI Agent Traps defense)
    is_web, web_reasons = detect_web_origin(content, meta)
    cap_warnings = check_confidence_cap(meta, is_web, web_reasons)
    messages.extend(cap_warnings)

    # 5. Memory poisoning check (instruction patterns in learning body)
    poison_warnings = check_instruction_in_learning(content)
    messages.extend(poison_warnings)

    # 6. Missing verify_check warning
    if not meta.get("verify_check"):
        messages.append(
            "[admission-gate] No verify_check field — "
            "rules without checks are wishes, rules with checks are guardrails."
        )

    # Output warnings
    if messages:
        for msg in messages:
            print(msg)

    # Hard gate mode: block on critical violations (A-MAC inspired, 31% latency reduction)
    if GATE_MODE == "hard" and messages:
        hard_contradictions = [
            m for m in messages if "[contradiction-check] [hard]" in m
        ]
        if hard_contradictions:
            print(
                "[ADMISSION HARD GATE] Blocked: hard contradiction detected. "
                "Set STOPA_ADMISSION_GATE=soft to override."
            )
            sys.exit(1)

        if salience < 0.2:
            print(
                "[ADMISSION HARD GATE] Blocked: near-duplicate learning "
                f"(salience={salience:.2f}). "
                "Set STOPA_ADMISSION_GATE=soft to override."
            )
            sys.exit(1)

        if poison_warnings:
            print(
                "[ADMISSION HARD GATE] Blocked: memory poisoning pattern detected. "
                "Set STOPA_ADMISSION_GATE=soft to override."
            )
            sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""PostToolUse hook: auto-detect and populate `related:` field for new learnings.

Fires after Write/Edit to learnings/ directory (after learning-admission.py).
Uses block-manifest.json for fast similarity scoring without parsing individual YAML files.
Creates BIDIRECTIONAL links: new → existing AND existing → new (max 3 per learning).

Also increments wiki-pending.json for Gap 4 (wiki freshness tracking).
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LEARNINGS_DIR = PROJECT_ROOT / ".claude/memory/learnings"
MANIFEST_PATH = LEARNINGS_DIR / "block-manifest.json"
WIKI_PENDING = PROJECT_ROOT / ".claude/memory/intermediate/wiki-pending.json"
MAX_RELATED = 3
MIN_SCORE = 0.3

SKIP_FILES = frozenset({
    "critical-patterns.md", "block-manifest.json", "ecosystem-scan.md",
})


def parse_yaml_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter as flat string dict."""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    result = {}
    for line in content[3:end].strip().split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip()
    return result


def parse_tags(raw: str) -> set[str]:
    """Parse tags from YAML value string."""
    if not raw:
        return set()
    cleaned = raw.strip("[]")
    return {t.strip().strip("'\"") for t in cleaned.split(",") if t.strip()}


def parse_related(raw: str) -> list[str]:
    """Parse related field from YAML value string."""
    if not raw:
        return []
    cleaned = raw.strip("[]")
    return [r.strip().strip("'\"") for r in cleaned.split(",") if r.strip()]


def extract_keywords(text: str, min_len: int = 4) -> set[str]:
    """Extract significant words from text."""
    words = re.findall(r'\b[a-záčďéěíňóřšťúůýž]{%d,}\b' % min_len, text.lower())
    stop = {"that", "this", "with", "from", "have", "been", "will", "when",
            "jsou", "není", "jako", "nebo", "proto", "pokud", "musí", "může",
            "learning", "pattern", "should", "using", "after"}
    return {w for w in words if w not in stop}


def compute_similarity(new_tags: set, new_keywords: set, new_component: str,
                        existing: dict) -> float:
    """Score similarity between new learning and existing manifest block.

    Score = tag_jaccard × 0.4 + keyword_overlap × 0.4 + same_component × 0.2
    """
    ex_tags = set(existing.get("tags", []))
    ex_summary = existing.get("summary", "")
    ex_keywords = extract_keywords(ex_summary)
    ex_component = existing.get("component", "")

    # Tag Jaccard similarity
    tag_union = new_tags | ex_tags
    tag_jaccard = len(new_tags & ex_tags) / len(tag_union) if tag_union else 0

    # Keyword overlap (normalized)
    kw_union = new_keywords | ex_keywords
    kw_overlap = len(new_keywords & ex_keywords) / len(kw_union) if kw_union else 0

    # Component match
    comp_match = 1.0 if new_component == ex_component else 0.0

    return tag_jaccard * 0.4 + kw_overlap * 0.4 + comp_match * 0.2


def find_related(new_meta: dict, manifest: dict) -> list[str]:
    """Find top related learnings from manifest."""
    new_tags = parse_tags(new_meta.get("tags", ""))
    new_keywords = extract_keywords(new_meta.get("summary", "").strip("'\""))
    new_component = new_meta.get("component", "")
    new_file = new_meta.get("_filename", "")

    scores = []
    for fid, block in manifest.get("blocks", {}).items():
        if fid == new_file:
            continue
        if not block.get("active", True):
            continue
        score = compute_similarity(new_tags, new_keywords, new_component, block)
        if score >= MIN_SCORE:
            scores.append((fid, score))

    # Sort by score descending, take top MAX_RELATED
    scores.sort(key=lambda x: x[1], reverse=True)
    return [fid for fid, _ in scores[:MAX_RELATED]]


def update_related_field(filepath: Path, related_files: list[str]) -> bool:
    """Update the related: field in a learning's YAML frontmatter."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False

    formatted = "[" + ", ".join(related_files) + "]"

    # Replace existing related: field
    related_match = re.search(r"^related:.*$", content, re.MULTILINE)
    if related_match:
        old_related = parse_related(related_match.group().split(":", 1)[1])
        if old_related:
            # Merge existing + new, dedup, cap at MAX_RELATED
            merged = list(dict.fromkeys(old_related + related_files))[:MAX_RELATED]
            formatted = "[" + ", ".join(merged) + "]"
        content = content.replace(related_match.group(), f"related: {formatted}", 1)
    else:
        # Insert related: field before the closing ---
        end = content.find("---", 3)
        if end == -1:
            return False
        content = content[:end] + f"related: {formatted}\n" + content[end:]

    try:
        filepath.write_text(content, encoding="utf-8")
        return True
    except OSError:
        return False


def add_backlink(target_file: str, source_file: str) -> bool:
    """Add a backlink from target learning to source learning (bidirectional)."""
    filepath = LEARNINGS_DIR / target_file
    if not filepath.exists():
        return False

    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False

    meta = parse_yaml_frontmatter(content)
    existing_related = parse_related(meta.get("related", ""))

    # Already linked or at capacity
    if source_file in existing_related or len(existing_related) >= MAX_RELATED:
        return False

    existing_related.append(source_file)
    return update_related_field(filepath, existing_related)


def increment_wiki_pending(component: str) -> None:
    """Track pending learnings per component for wiki freshness (Gap 4)."""
    if not component:
        return

    WIKI_PENDING.parent.mkdir(parents=True, exist_ok=True)

    pending = {}
    if WIKI_PENDING.exists():
        try:
            pending = json.loads(WIKI_PENDING.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pending = {}

    pending[component] = pending.get(component, 0) + 1

    try:
        WIKI_PENDING.write_text(
            json.dumps(pending, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except OSError:
        pass


def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    if tool_name not in ("Write", "Edit"):
        return

    file_path = tool_input.get("file_path", "").replace("\\", "/")
    if "learnings/" not in file_path:
        return

    basename = Path(file_path).name
    if basename in SKIP_FILES or basename.startswith("index-"):
        return

    # Read the new/edited learning
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
    meta["_filename"] = basename

    # Skip if already has related (manually set)
    existing_related = parse_related(meta.get("related", ""))
    if len(existing_related) >= MAX_RELATED:
        return

    # Load manifest for fast similarity scoring
    if not MANIFEST_PATH.exists():
        return
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return

    # Find related learnings
    related = find_related(meta, manifest)
    if not related:
        # Track wiki pending even if no related found
        increment_wiki_pending(meta.get("component", ""))
        return

    # Merge with any existing related
    if existing_related:
        merged = list(dict.fromkeys(existing_related + related))[:MAX_RELATED]
    else:
        merged = related

    # Update new learning's related field
    if update_related_field(target, merged):
        # Add backlinks to related learnings
        backlinks = 0
        for rel_file in related:
            if add_backlink(rel_file, basename):
                backlinks += 1

        print(f"[auto-relate] Linked {basename} → {merged}" +
              (f" (+{backlinks} backlinks)" if backlinks else ""))

    # Track wiki pending
    increment_wiki_pending(meta.get("component", ""))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # Never block tool execution

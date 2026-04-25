#!/usr/bin/env python3
"""autoDream: Lightweight daily confidence maintenance for learnings.

Runs as a scheduled task (no LLM calls, no external deps).
Complements /evolve (deep manual analysis) with automated numerical maintenance:
- Confidence decay for unused learnings (60+ days), modulated by reward_factor
- Confidence boost from uses counter (log2 cumulative, Hippo-inspired)
- Penalty from harmful_uses counter (reduced; reward_factor handles continuous case)
- Auto-archive learnings with confidence < 0.3
- Staleness flagging (90+ days + low confidence)
- Dedup detection (same component + 3+ shared tags)
- Graduation candidate reporting

Confidence dynamics (Hippo-inspired, kitfunso/hippo-memory src/memory.ts):
  reward_ratio  = (succ - harm) / (succ + harm + 1)   # ∈ [-1, +1]
  reward_factor = 1 + 0.5 * reward_ratio              # ∈ [0.5, 1.5]
  decay_rate    = base_rate * (2 - reward_factor)     # ∈ [0.5, 1.5] × base
  boost         = 0.1 * log2(uses + 1) * reward_factor

Output: JSON report to intermediate/autodream-report.json + stdout summary.
"""
import json
import math
import re
import shutil
import sys
from datetime import date, datetime
from pathlib import Path

# .claude/hooks/ → .claude/ → repo root → scripts/
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "scripts"))
from atomic_utils import atomic_write

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

LEARNINGS_DIR = _REPO_ROOT / ".claude/memory/learnings"
ARCHIVE_DIR = LEARNINGS_DIR / "archive"
REPORT_PATH = _REPO_ROOT / ".claude/memory/intermediate/autodream-report.json"
MERGE_CANDIDATES_DIR = _REPO_ROOT / ".claude/memory/intermediate/merge-candidates"

# Confidence defaults by source (from memory-files.md rules)
SOURCE_DEFAULTS: dict[str, float] = {
    "user_correction": 0.9,
    "critic_finding": 0.8,
    "auto_pattern": 0.7,
    "external_research": 0.6,
    "agent_generated": 0.5,
}
DEFAULT_CONFIDENCE = 0.7


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> tuple[dict, str, str]:
    """Extract YAML frontmatter fields, raw YAML block, and body text.

    Returns:
        (fields_dict, raw_yaml_text, body_after_closing_dashes)
    """
    if not content.startswith("---"):
        return {}, "", content
    end = content.find("---", 3)
    if end == -1:
        return {}, "", content
    raw_yaml = content[3:end].strip()
    body = content[end + 3:]

    fields: dict[str, str] = {}
    for line in raw_yaml.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key:
                fields[key] = val
    return fields, raw_yaml, body


def parse_tags(tags_str: str) -> list[str]:
    """Parse YAML tags field: [tag1, tag2] or tag1, tag2."""
    tags_str = tags_str.strip().strip("[]")
    return [t.strip().lower() for t in tags_str.split(",") if t.strip()]


def safe_float(val: str, default: float = 0.0) -> float:
    """Parse float from string, returning default on failure."""
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def safe_int(val: str, default: int = 0) -> int:
    """Parse int from string, returning default on failure."""
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


# ---------------------------------------------------------------------------
# Confidence computation
# ---------------------------------------------------------------------------

def compute_effective_confidence(
    base: float,
    date_str: str,
    uses: int,
    successful_uses: int,
    harmful_uses: int,
    today: date,
) -> float:
    """Compute effective confidence per STOPA rules with Hippo reward modulation.

    Hippo-inspired (kitfunso/hippo-memory src/memory.ts):
    - reward_factor ∈ [0.5, 1.5] continuously modulates decay rate AND boost magnitude
    - Successful learnings (factor → 1.5): decay halved, boost amplified
    - Harmful learnings (factor → 0.5): decay 1.5×, boost dampened
    - Untracked (succ=harm=0, factor=1.0): unchanged behaviour

    Order: parse → reward_factor → decay (modulated) → boost (modulated) → harm penalty → clamp
    """
    # Parse learning date
    try:
        learning_date = date.fromisoformat(date_str)
    except (ValueError, TypeError):
        learning_date = today  # Can't decay if date unknown

    days_old = (today - learning_date).days

    # Hippo continuous reward modulation
    denom = successful_uses + harmful_uses + 1
    reward_ratio = (successful_uses - harmful_uses) / denom
    reward_factor = 1.0 + 0.5 * reward_ratio  # ∈ [0.5, 1.5]

    result = base

    # Decay: amplified for harmful, dampened for successful
    # decay_multiplier = (2 - reward_factor) ∈ [0.5, 1.5]
    if days_old > 60 and uses == 0:
        decay_periods = (days_old - 60) // 30
        result -= decay_periods * 0.1 * (2.0 - reward_factor)

    # Boost: log2 cumulative (matches outcome-credit.py per-step delta), modulated by reward
    if uses > 0:
        base_boost = 0.1 * math.log2(uses + 1)
        result += base_boost * reward_factor

    # Discrete penalty for hard signals — reduced from 0.15 since reward_factor
    # already handles continuous adjustment via dampened boost + amplified decay
    result -= harmful_uses * 0.10

    # Clamp
    return round(max(0.1, min(1.0, result)), 2)


# ---------------------------------------------------------------------------
# Frontmatter update
# ---------------------------------------------------------------------------

def update_frontmatter_field(raw_yaml: str, field: str, value: str) -> str:
    """Update or add a field in raw YAML frontmatter text."""
    pattern = re.compile(rf"^{re.escape(field)}:.*$", re.MULTILINE)
    new_line = f"{field}: {value}"
    if pattern.search(raw_yaml):
        return pattern.sub(new_line, raw_yaml)
    # Field not present — append
    return raw_yaml + "\n" + new_line


def reassemble_file(raw_yaml: str, body: str) -> str:
    """Reconstruct full file from YAML block and body."""
    return f"---\n{raw_yaml}\n---{body}"


# ---------------------------------------------------------------------------
# Dedup detection
# ---------------------------------------------------------------------------

_TOKEN_RE = re.compile(r"[a-zA-Z0-9_-]{3,}")


def _summary_tokens(summary: str) -> set[str]:
    """Extract distinctive tokens from summary text (>= 3 chars, lowercased)."""
    return {t.lower() for t in _TOKEN_RE.findall(summary or "")}


def jaccard_similarity(a: set[str], b: set[str]) -> float:
    """Standard Jaccard: |A ∩ B| / |A ∪ B|. Returns 0 for empty union."""
    if not a and not b:
        return 0.0
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def find_dedup_candidates(
    learnings: list[dict],
) -> list[dict]:
    """Find learnings with same component + 3+ shared tags.

    Returns list of {
        "files": [str], "component": str, "shared_tags": [str],
        "summary_jaccard": float,
        "merge_strong": bool,  # Hippo-inspired: high overlap → strong merge candidate
    }

    A pair is `merge_strong` (warrants automatic soft-sunset → merged learning)
    when Jaccard summary token overlap >= 0.5 AND both confidence > 0.5. The actual
    merge content synthesis is deferred to /dreams skill (LLM-aware).
    Ref: kitfunso/hippo-memory src/consolidate.ts:414 — clusters with Jaccard
    textOverlap >= 0.35 are merged; STOPA uses 0.5 threshold (more conservative).
    """
    # Group by component
    by_component: dict[str, list[dict]] = {}
    for lr in learnings:
        comp = lr.get("component", "unknown")
        by_component.setdefault(comp, []).append(lr)

    candidates = []
    for comp, group in by_component.items():
        if len(group) < 2:
            continue
        # Check all pairs
        for i, a in enumerate(group):
            for b in group[i + 1:]:
                shared = set(a.get("tags_list", [])) & set(b.get("tags_list", []))
                if len(shared) < 3:
                    continue

                tokens_a = _summary_tokens(a.get("summary", ""))
                tokens_b = _summary_tokens(b.get("summary", ""))
                jaccard = round(jaccard_similarity(tokens_a, tokens_b), 3)

                merge_strong = (
                    jaccard >= 0.5
                    and a.get("confidence", 0) > 0.5
                    and b.get("confidence", 0) > 0.5
                )

                candidates.append({
                    "files": [a["filename"], b["filename"]],
                    "component": comp,
                    "shared_tags": sorted(shared),
                    "summary_jaccard": jaccard,
                    "merge_strong": merge_strong,
                })
    return candidates


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    today = date.today()

    if not LEARNINGS_DIR.is_dir():
        print("No learnings directory found.")
        return

    # Collect all learning files
    learning_files = sorted(LEARNINGS_DIR.glob("202*.md"))
    if not learning_files:
        print("No learning files found.")
        return

    # Report accumulators
    maintained: list[dict] = []  # confidence updated
    archived: list[dict] = []    # moved to archive
    stale: list[dict] = []       # 90+ days, low confidence
    graduation: list[dict] = []  # meets graduation criteria
    all_learnings: list[dict] = []  # for dedup detection

    for filepath in learning_files:
        try:
            content = filepath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        fields, raw_yaml, body = parse_frontmatter(content)
        if not fields:
            continue

        filename = filepath.name
        date_str = fields.get("date", "")
        source = fields.get("source", "auto_pattern")
        tags_list = parse_tags(fields.get("tags", ""))

        # Get current values (with defaults)
        old_confidence = safe_float(
            fields.get("confidence", ""),
            SOURCE_DEFAULTS.get(source, DEFAULT_CONFIDENCE),
        )
        uses = safe_int(fields.get("uses", ""), 0)
        successful_uses = safe_int(fields.get("successful_uses", ""), 0)
        harmful_uses = safe_int(fields.get("harmful_uses", ""), 0)

        # Compute new confidence
        base = safe_float(
            fields.get("confidence", ""),
            SOURCE_DEFAULTS.get(source, DEFAULT_CONFIDENCE),
        )
        # For decay check: use original base (not already-decayed value)
        # We re-derive from source default if confidence field was missing
        new_confidence = compute_effective_confidence(
            base, date_str, uses, successful_uses, harmful_uses, today,
        )

        # Store for dedup
        lr_data = {
            "filename": filename,
            "component": fields.get("component", "unknown"),
            "tags_list": tags_list,
            "confidence": new_confidence,
            "date": date_str,
            "uses": uses,
            "successful_uses": successful_uses,
            "harmful_uses": harmful_uses,
            "summary": fields.get("summary", ""),
        }
        all_learnings.append(lr_data)

        # Check if confidence changed
        confidence_changed = abs(new_confidence - old_confidence) > 0.005

        # Auto-archive: confidence < 0.3
        if new_confidence < 0.3:
            ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
            dest = ARCHIVE_DIR / filename
            try:
                # Update confidence before archiving
                if confidence_changed:
                    updated_yaml = update_frontmatter_field(
                        raw_yaml, "confidence", str(new_confidence),
                    )
                    new_content = reassemble_file(updated_yaml, body)
                    atomic_write(filepath, new_content)
                shutil.move(str(filepath), str(dest))
                archived.append({
                    "file": filename,
                    "confidence": new_confidence,
                    "reason": "confidence below 0.3",
                })
            except OSError as e:
                print(f"  [WARN] Failed to archive {filename}: {e}", file=sys.stderr)
            continue

        # Update confidence in file if changed
        if confidence_changed:
            updated_yaml = update_frontmatter_field(
                raw_yaml, "confidence", str(new_confidence),
            )
            new_content = reassemble_file(updated_yaml, body)
            try:
                atomic_write(filepath, new_content)
                maintained.append({
                    "file": filename,
                    "old": old_confidence,
                    "new": new_confidence,
                })
            except OSError as e:
                print(f"  [WARN] Failed to update {filename}: {e}", file=sys.stderr)

        # Staleness check: 90+ days AND confidence < 0.5
        try:
            learning_date = date.fromisoformat(date_str)
            days_old = (today - learning_date).days
        except (ValueError, TypeError):
            days_old = 0

        if days_old > 90 and new_confidence < 0.5:
            stale.append({
                "file": filename,
                "days_old": days_old,
                "confidence": new_confidence,
            })

        # Graduation check: uses >= 10 AND confidence >= 0.8 AND harmful < 2
        # Skip if already graduated (maturity=core) or explicitly marked graduated_to
        already_graduated = (
            fields.get("maturity", "") == "core"
            or bool(fields.get("graduated_to", ""))
        )
        if uses >= 10 and new_confidence >= 0.8 and harmful_uses < 2 and not already_graduated:
            graduation.append({
                "file": filename,
                "uses": uses,
                "confidence": new_confidence,
                "summary": fields.get("summary", "")[:80],
            })

    # Dedup detection (with merge_strong flag for high-overlap pairs)
    dedup = find_dedup_candidates(all_learnings)

    # Persist merge candidate stubs for /dreams skill to consume
    # /dreams reads these to perform LLM-aware merge synthesis (rule-based detection
    # here, content synthesis there — Hippo consolidate.ts:414 pattern)
    merge_strong = [d for d in dedup if d.get("merge_strong")]
    if merge_strong:
        MERGE_CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
        # Lookup by filename for richer stub data
        by_filename = {lr["filename"]: lr for lr in all_learnings}
        for cand in merge_strong:
            fa, fb = cand["files"]
            stub_name = f"{fa.replace('.md', '')}__{fb.replace('.md', '')}.json"
            stub_path = MERGE_CANDIDATES_DIR / stub_name
            if stub_path.exists():
                continue  # already proposed; /dreams handles or user dismisses
            la = by_filename.get(fa, {})
            lb = by_filename.get(fb, {})
            stub_data = {
                "created": today.isoformat(),
                "component": cand["component"],
                "shared_tags": cand["shared_tags"],
                "summary_jaccard": cand["summary_jaccard"],
                "files": [
                    {
                        "name": fa,
                        "summary": la.get("summary", ""),
                        "confidence": la.get("confidence"),
                        "uses": la.get("uses", 0),
                        "successful_uses": la.get("successful_uses", 0),
                    },
                    {
                        "name": fb,
                        "summary": lb.get("summary", ""),
                        "confidence": lb.get("confidence"),
                        "uses": lb.get("uses", 0),
                        "successful_uses": lb.get("successful_uses", 0),
                    },
                ],
                "suggested_action": (
                    "Merge via /dreams Phase 2b. Synthesize unified summary, "
                    "set supersedes: [old1, old2] on merged file, set valid_until "
                    "on both originals to today (skip retrieval, keep audit trail)."
                ),
            }
            try:
                atomic_write(stub_path, json.dumps(stub_data, indent=2, ensure_ascii=False))
            except OSError as e:
                print(f"[WARN] Failed to write merge stub {stub_name}: {e}", file=sys.stderr)

    # Build report
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_scanned": len(learning_files),
        "maintained": maintained,
        "archived": archived,
        "stale": stale,
        "dedup_candidates": dedup,
        "merge_strong_count": len(merge_strong),
        "graduation_candidates": graduation,
    }

    # Write JSON report
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        atomic_write(REPORT_PATH, json.dumps(report, indent=2, ensure_ascii=False))
    except OSError as e:
        print(f"[WARN] Failed to write report: {e}", file=sys.stderr)

    # Stdout summary
    print(f"=== autoDream Report ({today.isoformat()}) ===")
    print(f"Scanned: {len(learning_files)} learnings")

    if maintained:
        print(f"\nConfidence updated: {len(maintained)}")
        for m in maintained:
            print(f"  {m['file']}: {m['old']:.2f} → {m['new']:.2f}")

    if archived:
        print(f"\nArchived (confidence < 0.3): {len(archived)}")
        for a in archived:
            print(f"  {a['file']} (confidence={a['confidence']:.2f})")

    if stale:
        print(f"\nStale (90+ days, low confidence): {len(stale)}")
        for s in stale:
            print(f"  {s['file']}: {s['days_old']}d old, confidence={s['confidence']:.2f}")

    if dedup:
        strong_count = sum(1 for d in dedup if d.get("merge_strong"))
        print(f"\nDedup candidates: {len(dedup)} ({strong_count} merge-strong)")
        for d in dedup:
            tag = " [MERGE-STRONG]" if d.get("merge_strong") else ""
            jac = f" jaccard={d['summary_jaccard']:.2f}" if "summary_jaccard" in d else ""
            print(f"  [{d['component']}]{tag} {', '.join(d['files'])} — shared: {', '.join(d['shared_tags'])}{jac}")
        if strong_count:
            print(f"  → {strong_count} merge stub(s) written to {MERGE_CANDIDATES_DIR.relative_to(_REPO_ROOT)}/")

    if graduation:
        print(f"\nGraduation candidates: {len(graduation)}")
        for g in graduation:
            print(f"  {g['file']}: uses={g['uses']}, confidence={g['confidence']:.2f}")

    if not any([maintained, archived, stale, dedup, graduation]):
        print("\nAll learnings healthy — no changes needed.")


if __name__ == "__main__":
    main()

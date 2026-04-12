#!/usr/bin/env python3
"""Auto-evolve STOPA skills from session evidence.

SkillClaw-inspired (arXiv:2604.08377) skill evolution pipeline.
Reads session summaries grouped by skill, calls Claude to produce
staged candidate diffs. Does NOT auto-apply — candidates go to
.claude/memory/candidates/ for human review via `/evolve --candidates`.

Pipeline: summarize-sessions.py → THIS → /evolve --candidates

Usage:
    python scripts/evolve-skills.py [--dry-run] [--model MODEL]
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SUMMARIES_DIR = Path(".claude/memory/summaries")
CANDIDATES_DIR = Path(".claude/memory/candidates")
SKILLS_DIR = Path(".claude/skills")
COMMANDS_DIR = Path(".claude/commands")
DEFAULT_MODEL = "claude-sonnet-4-6"

# SkillClaw-inspired system prompt for evolution decisions
EVOLVE_SYSTEM_PROMPT = """You are a skill evolution agent for STOPA — a Claude Code orchestration system.

You analyze session evidence (how a skill was actually used) and decide whether the skill file needs improvement.

## Conservative Editing Rules (non-negotiable)

1. Treat the CURRENT skill as the source of truth, not a rough draft
2. Do NOT rewrite the whole skill from scratch — make targeted edits
3. If successful sessions support a section, leave it untouched unless failure evidence explicitly contradicts
4. Not every error is a skill deficiency — separate agent mistakes from skill gaps
5. When in doubt, prefer `skip` over a speculative edit
6. description: field MUST start with "Use when..." (STOPA convention)
7. Do NOT change YAML frontmatter fields (name, tags, phase, etc.) — only content and description
8. Do NOT remove Anti-Rationalization Defense, Red Flags, or Verification Checklist sections

## Decision Options

Choose exactly ONE:

- `improve_skill` — targeted content edits where evidence shows skill is missing guidance or has a gap
- `optimize_description` — description field needs better trigger conditions (misrouted or missed invocations)
- `create_skill` — evidence reveals a distinct capability that doesn't belong in this skill (provide new skill name+content)
- `skip` — skill works adequately, evidence is weak, or changes would be speculative

## Output Format

Respond with valid JSON only (no markdown, no explanation outside JSON):

```json
{
  "action": "improve_skill|optimize_description|create_skill|skip",
  "rationale": "1-3 sentences: what evidence motivated this decision",
  "confidence": 0.0-1.0,
  "skill": {
    "name": "skill-name",
    "description": "Use when...",
    "content_patch": "ONLY the sections to add/modify (not the full skill body)",
    "edit_summary": {
      "preserved_sections": ["section names left intact"],
      "changed_sections": ["section names modified or added"],
      "notes": "what changed and why, in one sentence"
    }
  }
}
```

For `skip` action, only `action`, `rationale`, and `confidence` are required.
For `content_patch`: provide ONLY new/changed sections with their ## headings — the apply step merges them into the existing skill.
"""


def parse_args():
    """Parse CLI arguments."""
    dry_run = "--dry-run" in sys.argv
    model = DEFAULT_MODEL
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--model" and i < len(sys.argv) - 1:
            model = sys.argv[i + 1]
    return dry_run, model


def get_current_skill(skill_name: str) -> tuple[str | None, Path | None]:
    """Read current SKILL.md content. Returns (content, path)."""
    candidates = [
        SKILLS_DIR / skill_name / "SKILL.md",
        COMMANDS_DIR / f"{skill_name}.md",
    ]
    for path in candidates:
        if path.exists():
            try:
                return path.read_text(encoding="utf-8", errors="replace"), path
            except OSError:
                pass
    return None, None


def call_claude(prompt: str, model: str) -> str:
    """Call Claude via CLI subprocess."""
    try:
        result = subprocess.run(
            ["claude", "-p", "--model", model, prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
        return result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"  Error calling claude: {e}")
        return ""


def extract_json(response: str) -> dict | None:
    """Extract JSON from Claude response (may be wrapped in markdown)."""
    if not response:
        return None

    # Try direct parse
    try:
        return json.loads(response.strip())
    except json.JSONDecodeError:
        pass

    # Try extracting from markdown code block
    json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Try finding the outermost JSON object
    brace_start = response.find("{")
    if brace_start >= 0:
        depth = 0
        for i, c in enumerate(response[brace_start:], brace_start):
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(response[brace_start : i + 1])
                    except json.JSONDecodeError:
                        break
    return None


def evolve_skill(
    skill_name: str, evidence: dict, model: str, dry_run: bool
) -> dict | None:
    """Produce evolution candidate for one skill."""
    current_skill, skill_path = get_current_skill(skill_name)
    if not current_skill:
        print(f"  Skill '{skill_name}' not found — skipping")
        return None

    # Build evidence summary (compact, under 4000 chars to save tokens)
    evidence_text = json.dumps(
        {
            "session_count": evidence["session_count"],
            "avg_error_rate": evidence["avg_error_rate"],
            "sessions": [
                {
                    "id": s["session_id"],
                    "calls": s["total_calls"],
                    "err_rate": s["error_rate"],
                    "pattern": " → ".join(s["tool_sequence"][:15]),
                    "errors": s.get("errors", [])[:2],
                }
                for s in evidence["sessions"][:5]  # Cap at 5 sessions
            ],
            "top_errors": evidence.get("aggregated_errors", [])[:5],
        },
        indent=2,
        ensure_ascii=False,
    )

    # Truncate skill body if too long (keep first 3000 chars)
    skill_preview = current_skill
    if len(skill_preview) > 4000:
        skill_preview = skill_preview[:4000] + "\n\n[... truncated for token savings ...]"

    prompt = f"""{EVOLVE_SYSTEM_PROMPT}

## Current SKILL.md for '{skill_name}'

{skill_preview}

## Session Evidence ({evidence['session_count']} sessions, avg error rate {evidence['avg_error_rate']:.1%})

{evidence_text}

Analyze this evidence and decide: should this skill be improved?"""

    if dry_run:
        print(f"  [DRY RUN] Would call Claude with {len(prompt)} char prompt")
        return None

    response = call_claude(prompt, model)
    result = extract_json(response)

    if not result:
        print(f"  Failed to parse response for '{skill_name}'")
        return None

    return result


def save_candidate(skill_name: str, candidate: dict, evidence: dict) -> Path:
    """Save evolution candidate to staging directory."""
    CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)

    candidate["meta"] = {
        "skill_name": skill_name,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "session_count": evidence["session_count"],
        "avg_error_rate": evidence["avg_error_rate"],
        "pipeline": "auto-evolve (SkillClaw-inspired)",
    }

    filename = f"{skill_name}-{time.strftime('%Y-%m-%d')}.json"
    output_path = CANDIDATES_DIR / filename
    output_path.write_text(json.dumps(candidate, indent=2, ensure_ascii=False))
    return output_path


def main():
    dry_run, model = parse_args()

    # Find latest summary
    if not SUMMARIES_DIR.exists():
        print("No summaries found. Run summarize-sessions.py first.")
        sys.exit(1)

    summaries = sorted(SUMMARIES_DIR.glob("summary-*.json"), reverse=True)
    if not summaries:
        print("No summary files found. Run summarize-sessions.py first.")
        sys.exit(1)

    latest = summaries[0]
    summary = json.loads(latest.read_text(encoding="utf-8", errors="replace"))
    skill_groups = summary.get("skill_groups", {})

    if not skill_groups:
        print("No skills with sufficient evidence. Nothing to evolve.")
        sys.exit(0)

    print(f"Source: {latest.name}")
    print(f"Skills to evaluate: {len(skill_groups)}")
    print(f"Model: {model}")
    if dry_run:
        print("Mode: DRY RUN\n")
    else:
        print()

    # Process each skill group
    results: list[str] = []
    skipped: list[str] = []

    for skill_name, evidence in sorted(
        skill_groups.items(), key=lambda x: -x[1]["session_count"]
    ):
        print(f"Evaluating: {skill_name} "
              f"({evidence['session_count']} sessions, "
              f"err={evidence['avg_error_rate']:.1%})...")

        candidate = evolve_skill(skill_name, evidence, model, dry_run)

        if not candidate:
            skipped.append(skill_name)
            continue

        action = candidate.get("action", "skip")
        confidence = candidate.get("confidence", 0)
        rationale = candidate.get("rationale", "")

        if action == "skip":
            print(f"  → skip (confidence={confidence:.2f}): {rationale[:80]}")
            skipped.append(skill_name)
            continue

        # Confidence gate: don't save low-confidence candidates
        if confidence < 0.4:
            print(f"  → {action} but confidence too low ({confidence:.2f}) — skipping")
            skipped.append(skill_name)
            continue

        # Save candidate
        output_path = save_candidate(skill_name, candidate, evidence)
        print(f"  → {action} (confidence={confidence:.2f})")
        print(f"    {rationale[:100]}")
        print(f"    Saved: {output_path.name}")
        results.append(f"{skill_name}: {action} ({confidence:.2f})")

    # Report
    print(f"\n{'='*50}")
    print(f"Candidates generated: {len(results)}")
    for r in results:
        print(f"  {r}")
    if skipped:
        print(f"Skipped: {len(skipped)} ({', '.join(skipped[:10])})")
    if results:
        print(f"\nReview with: /evolve --candidates")


if __name__ == "__main__":
    main()

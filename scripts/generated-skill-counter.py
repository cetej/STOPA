"""Generated-skill invocation counter — /tool-synth graduation support.

Tracks uses / successful_uses / harmful_uses directly in the YAML frontmatter
of .claude/skills/_generated/<slug>/SKILL.md. Called by /orchestrate Phase 4
after each subtask that invoked a generated skill. Consumed by /evolve
graduation step.

Commands:
    python scripts/generated-skill-counter.py increment <slug> [--critic PASS|FAIL|NONE]
    python scripts/generated-skill-counter.py read <slug> [--json]

Semantics:
    increment --critic PASS  → uses += 1, successful_uses += 1
    increment --critic FAIL  → uses += 1, harmful_uses += 1
    increment --critic NONE  → uses += 1 (no critic signal for this run)

Missing counter fields are initialized to 0 on first increment.
Fails closed if the draft does not live under .claude/skills/_generated/.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SANDBOX_ROOT = Path(".claude/skills/_generated")
COUNTER_FIELDS = ("uses", "successful_uses", "harmful_uses")


def _skill_path(slug: str) -> Path:
    return SANDBOX_ROOT / slug / "SKILL.md"


def _split_frontmatter(text: str) -> tuple[list[str], list[str]]:
    lines = text.splitlines(keepends=True)
    if not lines or not lines[0].startswith("---"):
        raise ValueError("No YAML frontmatter (missing opening '---')")
    for i in range(1, len(lines)):
        if lines[i].startswith("---"):
            return lines[: i + 1], lines[i + 1 :]
    raise ValueError("No YAML frontmatter (missing closing '---')")


def _read_counter(fm_lines: list[str], field: str) -> int:
    pattern = re.compile(rf"^{re.escape(field)}:\s*(-?\d+)\s*$")
    for line in fm_lines:
        m = pattern.match(line)
        if m:
            return int(m.group(1))
    return 0


def _write_counter(fm_lines: list[str], field: str, value: int) -> list[str]:
    pattern = re.compile(rf"^{re.escape(field)}:\s*-?\d+\s*$")
    for i, line in enumerate(fm_lines):
        if pattern.match(line):
            fm_lines[i] = f"{field}: {value}\n"
            return fm_lines
    insert_at = len(fm_lines) - 1 if fm_lines[-1].startswith("---") else len(fm_lines)
    fm_lines.insert(insert_at, f"{field}: {value}\n")
    return fm_lines


def increment(args: argparse.Namespace) -> int:
    path = _skill_path(args.slug)
    if not path.exists():
        print(f"ERROR: no sandbox skill at {path}", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8")
    try:
        fm, body = _split_frontmatter(text)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3

    counters = {f: _read_counter(fm, f) for f in COUNTER_FIELDS}
    counters["uses"] += 1
    critic = args.critic.upper()
    if critic == "PASS":
        counters["successful_uses"] += 1
    elif critic == "FAIL":
        counters["harmful_uses"] += 1
    elif critic != "NONE":
        print(f"ERROR: --critic must be PASS|FAIL|NONE, got {args.critic}", file=sys.stderr)
        return 4

    for field, value in counters.items():
        fm = _write_counter(fm, field, value)
    path.write_text("".join(fm) + "".join(body), encoding="utf-8")
    print(
        f"{args.slug}: uses={counters['uses']} "
        f"successful={counters['successful_uses']} harmful={counters['harmful_uses']}"
    )
    return 0


def read_cmd(args: argparse.Namespace) -> int:
    path = _skill_path(args.slug)
    if not path.exists():
        print(f"ERROR: no sandbox skill at {path}", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8")
    try:
        fm, _ = _split_frontmatter(text)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3
    counters = {f: _read_counter(fm, f) for f in COUNTER_FIELDS}
    if args.json:
        print(json.dumps({"slug": args.slug, **counters}, ensure_ascii=False))
    else:
        print(
            f"{args.slug}: uses={counters['uses']} "
            f"successful={counters['successful_uses']} harmful={counters['harmful_uses']}"
        )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_inc = sub.add_parser("increment", help="Bump uses (and optional critic counter)")
    p_inc.add_argument("slug")
    p_inc.add_argument(
        "--critic",
        default="NONE",
        choices=["PASS", "FAIL", "NONE", "pass", "fail", "none"],
        help="Critic verdict for the run that invoked this skill",
    )
    p_inc.set_defaults(func=increment)

    p_read = sub.add_parser("read", help="Print current counter values")
    p_read.add_argument("slug")
    p_read.add_argument("--json", action="store_true")
    p_read.set_defaults(func=read_cmd)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

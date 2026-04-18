"""Resource version lineage manager — Autogenesis RSPL-inspired.

Append-only ledger at .claude/memory/resource-ledger.jsonl tracks every
version change to protocol-registered resources (skills, prompts, tools).

Commands:
    python scripts/resource-ledger.py log <resource> <old_v> <new_v> <trigger> [--pass-before F --pass-after F --strategy S --commit SHA]
    python scripts/resource-ledger.py history <resource> [--json]
    python scripts/resource-ledger.py rollback <resource> --to <version>  (dry-run by default)
    python scripts/resource-ledger.py rollback <resource> --to <version> --apply

Version format: semver-lite (X.Y.Z). See .claude/skills/self-evolve/SKILL.md Step 6.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LEDGER = Path(".claude/memory/resource-ledger.jsonl")


def _append(entry: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def log(args: argparse.Namespace) -> int:
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "resource": args.resource,
        "old_version": args.old_v,
        "new_version": args.new_v,
        "trigger": args.trigger,
    }
    if args.pass_before is not None:
        entry["pass_rate_before"] = args.pass_before
    if args.pass_after is not None:
        entry["pass_rate_after"] = args.pass_after
    if args.strategy:
        entry["strategy"] = args.strategy
    if args.commit:
        entry["commit"] = args.commit
    _append(entry)
    print(f"logged {args.resource}: {args.old_v} -> {args.new_v}")
    return 0


def _read_entries(resource: str | None = None) -> list[dict]:
    if not LEDGER.exists():
        return []
    out = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("resource") == "_meta":
            continue
        if resource is None or entry.get("resource") == resource:
            out.append(entry)
    return out


def history(args: argparse.Namespace) -> int:
    entries = _read_entries(args.resource)
    if args.json:
        print(json.dumps(entries, ensure_ascii=False, indent=2))
        return 0
    if not entries:
        print(f"No history for {args.resource}")
        return 1
    print(f"{len(entries)} entries for {args.resource}:")
    for e in entries:
        delta = ""
        if "pass_rate_before" in e and "pass_rate_after" in e:
            delta = f" Δ{e['pass_rate_after'] - e['pass_rate_before']:+.2f}"
        print(f"  {e['ts']}  {e['old_version']} -> {e['new_version']}  {e.get('trigger','')}{delta}")
    return 0


def rollback(args: argparse.Namespace) -> int:
    entries = _read_entries(args.resource)
    target_entry = None
    for e in entries:
        if e.get("new_version") == args.to:
            target_entry = e
    if target_entry is None:
        print(f"ERROR: version {args.to} not found in ledger for {args.resource}")
        return 2
    commit = target_entry.get("commit")
    if not commit:
        print(f"ERROR: ledger entry for {args.to} has no commit SHA — cannot rollback via git")
        return 3
    print(f"Rollback plan: {args.resource} -> v{args.to} (commit {commit})")
    print(f"  git checkout {commit} -- {args.resource}")
    if not args.apply:
        print("Dry-run. Re-run with --apply to execute.")
        return 0
    try:
        subprocess.run(
            ["git", "checkout", commit, "--", args.resource],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"git checkout failed: {exc.stderr}")
        return 4
    current = _read_version_from_file(Path(args.resource))
    _append(
        {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "resource": args.resource,
            "old_version": current or "unknown",
            "new_version": args.to,
            "trigger": f"manual rollback to {args.to}",
        }
    )
    print(f"Applied. {args.resource} restored to v{args.to} and logged.")
    return 0


def _read_version_from_file(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^version:\s*['\"]?([\d.]+)['\"]?\s*$", text, re.MULTILINE)
    return match.group(1) if match else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_log = sub.add_parser("log", help="Append a version-change entry")
    p_log.add_argument("resource")
    p_log.add_argument("old_v")
    p_log.add_argument("new_v")
    p_log.add_argument("trigger")
    p_log.add_argument("--pass-before", type=float, dest="pass_before")
    p_log.add_argument("--pass-after", type=float, dest="pass_after")
    p_log.add_argument("--strategy")
    p_log.add_argument("--commit")
    p_log.set_defaults(func=log)

    p_hist = sub.add_parser("history", help="Show version history for a resource")
    p_hist.add_argument("resource")
    p_hist.add_argument("--json", action="store_true")
    p_hist.set_defaults(func=history)

    p_rb = sub.add_parser("rollback", help="Restore resource to a prior version")
    p_rb.add_argument("resource")
    p_rb.add_argument("--to", required=True, help="Target version string")
    p_rb.add_argument("--apply", action="store_true", help="Execute (default: dry-run)")
    p_rb.set_defaults(func=rollback)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

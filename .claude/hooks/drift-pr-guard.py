#!/usr/bin/env python3
"""drift-pr-guard.py — PreToolUse guard against opening PRs for drift-only changes.

Triggered before Bash tool calls. Catches two anti-patterns:

1. `git commit` on a non-main branch where ALL staged files are drift.
   Suggestion: commit on main directly via scripts/auto-commit-drift.sh.

2. `gh pr create` for a branch whose unique commits are 100% drift.
   Suggestion: rebase the drift commits onto main and skip the PR.

Drift classification delegates to scripts/drift-classify.sh — single source
of truth shared with auto-commit-drift.sh and daily-rebalancer.

Decision: emits "ask" (warns user, lets them decide). Never silently blocks.

Activation: STOPA_DRIFT_PR_GUARD=warn (default) | enforce | off.
"""
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

MODE = os.environ.get("STOPA_DRIFT_PR_GUARD", "warn").lower()
if MODE == "off":
    sys.exit(0)

try:
    from drift_classify import classify_paths as _classify_paths  # noqa: E402
except ImportError:
    _classify_paths = None


def run(cmd: list[str], cwd: Path = REPO_ROOT) -> tuple[int, str, str]:
    """Run a subprocess; return (rc, stdout, stderr)."""
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except (subprocess.TimeoutExpired, OSError):
        return 1, "", ""


def classify_paths(paths: list[str]) -> tuple[bool, list[str]]:
    """Return (all_drift, non_drift_paths)."""
    if not paths or _classify_paths is None:
        return False, paths
    return _classify_paths(paths)


def current_branch() -> str:
    rc, out, _ = run(["git", "symbolic-ref", "--short", "HEAD"])
    return out.strip() if rc == 0 else ""


def staged_files() -> list[str]:
    rc, out, _ = run(["git", "diff", "--name-only", "--cached"])
    return [line for line in out.splitlines() if line.strip()] if rc == 0 else []


def branch_diff_files(branch: str, base: str = "main") -> list[str]:
    rc, out, _ = run(["git", "diff", "--name-only", f"{base}...{branch}"])
    return [line for line in out.splitlines() if line.strip()] if rc == 0 else []


def emit_ask(reason: str) -> None:
    """Hook protocol: print decision JSON to stdout, exit 0 (warn) or 2 (enforce)."""
    if MODE == "enforce":
        decision = "block"
    else:
        decision = "ask"
    payload = {"decision": decision, "reason": reason}
    print(json.dumps(payload, ensure_ascii=False))
    sys.exit(2 if decision == "block" else 0)


def check_git_commit(cmd: str) -> None:
    branch = current_branch()
    if not branch or branch == "main":
        return
    staged = staged_files()
    if not staged:
        return
    all_drift, _ = classify_paths(staged)
    if not all_drift:
        return
    emit_ask(
        f"git commit on branch '{branch}' with drift-only staged files "
        f"({len(staged)} paths). Drift commits should land on main directly. "
        f"Consider: git stash → git checkout main → git stash pop → "
        f"bash scripts/auto-commit-drift.sh"
    )


def check_gh_pr_create(cmd: str) -> None:
    branch = current_branch()
    if not branch or branch == "main":
        return
    files = branch_diff_files(branch, "main")
    if not files:
        return
    all_drift, _ = classify_paths(files)
    if not all_drift:
        return
    emit_ask(
        f"PR for branch '{branch}' diffs only drift paths ({len(files)} files). "
        f"Drift PRs accumulate conflicts (every drift commit on main breaks them). "
        f"Consider: rebase onto main and skip the PR — "
        f"git checkout main && git merge --ff-only {branch} && git push"
    )


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    if payload.get("tool") != "Bash":
        sys.exit(0)

    cmd = (payload.get("input") or {}).get("command", "")
    if not cmd:
        sys.exit(0)

    # Cheap regex first to avoid the cost of subprocess on unrelated commands.
    if re.search(r"\bgit\s+commit\b", cmd) and "--no-verify" not in cmd:
        check_git_commit(cmd)
    elif re.search(r"\bgh\s+pr\s+create\b", cmd):
        check_gh_pr_create(cmd)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 — hook must never break the tool call
        print(f"drift-pr-guard: internal error ({exc}), allowing", file=sys.stderr)
        sys.exit(0)

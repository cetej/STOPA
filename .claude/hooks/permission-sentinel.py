#!/usr/bin/env python
"""
Permission Sentinel — Guardian Layer 2 (LLM-based escalation handler)

Inspired by GuardAgent (arXiv:2406.09187) — knowledge-based reasoning over
session trajectory + tool input to make safety decisions for ambiguous cases.

USAGE:
    Reads PermissionRequest JSON from stdin, writes hook response JSON to stdout.
    Decision logged to .claude/memory/sentinel-log.jsonl with layer="L2".

ACTIVATION (currently OPT-IN, not wired to settings.json by default):
    Option A — separate API key:
        $env:ANTHROPIC_API_KEY="sk-..."
        Add to .claude/settings.json PermissionRequest hooks AFTER L1:
        { "type": "command",
          "command": "python C:/.../permission-sentinel.py",
          "timeout": 15 }

    Option B — native CC prompt hook (recommended for production):
        Uses CC's existing subscription auth. Add to settings.json:
        { "type": "prompt",
          "model": "claude-haiku-4",
          "prompt": "<see SENTINEL_PROMPT below>",
          "timeout": 15 }

FAIL-SAFE BEHAVIOR:
    - No API key set         -> passthrough {} (CC falls back to next hook / user prompt)
    - API call fails/times out -> deny with reason (fail-closed for unknown decisions)
    - Invalid stdin JSON     -> passthrough {}
    - Sentinel says ALLOW    -> {"hookSpecificOutput": {"permissionDecision": "allow"}}
    - Sentinel says DENY     -> {"hookSpecificOutput": {"permissionDecision": "deny",
                                                         "permissionDecisionReason": "..."}}
"""

import fnmatch
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Ensure UTF-8 for Windows
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
SENTINEL_LOG = PROJECT_ROOT / ".claude" / "memory" / "sentinel-log.jsonl"

# Routine patterns — mirror permission-auto-approve.sh L1 routing.
# When L1 has already auto-approved a routine op, L2 has no business re-evaluating it
# (and previously was emitting false DENYs like "uncertain - escalate to human" on
# the agent's own hooks/scripts). Skip these BEFORE the API call.
ROUTINE_FILE_GLOBS = (
    "*/brain/wiki/*", "*/brain/raw/processed/*", "*/brain/inbox.md",
    "*/brain/watchlist.md", "*/brain/knowledge-graph.json",
    "*/memory/concept-graph.json", "*/memory/daily-reports.md",
    "*/memory/news.md", "*/memory/radar.md", "*/memory/watchlist.md",
    "*/memory/inbox.md", "*/memory/improvement-log.md",
    "*/memory/sentinel-log.jsonl", "*/memory/permission-log*",
    "*/memory/wiki/*", "*/memory/learnings/*", "*/memory/outcomes/*",
    "*/memory/failures/*", "*/memory/dreams/*", "*/memory/optstate/*",
    "*/memory/intermediate/*", "*/memory/replay-queue.md",
    "*/outputs/*", "*/outputs/.research/*",
)

# Bash command prefixes considered routine (matches the project's own scripts and
# tools listed in settings.json allow-list).
ROUTINE_BASH_PREFIXES = (
    "python .claude/hooks/", "python .claude/scripts/", "python scripts/",
    "python3 .claude/hooks/", "python3 .claude/scripts/", "python3 scripts/",
    "python -c ", "python -m ", "python3 -c ", "python3 -m ",
    "bash .claude/hooks/", "bash .claude/scripts/", "powershell ",
    "git status", "git log", "git diff", "git show", "git add ",
    "git commit", "git push", "git pull", "git fetch", "git branch",
    "git checkout", "git stash", "git restore",
    "ls ", "cat ", "echo ", "diff ", "wc ", "head ", "tail ",
    "rtk ", "pdftotext ", "curl ",
)


def is_routine_op(tool_name: str, tool_input: dict) -> tuple[bool, str]:
    """Return (True, reason) when L1 would have already auto-allowed this.

    Mirrors permission-auto-approve.sh routing. Cheaper than calling Haiku
    and avoids LLM-induced false DENYs on the agent's own workspace.
    """
    if tool_name in ("Read", "Glob", "Grep", "WebFetch", "WebSearch",
                     "TodoWrite", "Skill", "ToolSearch", "Agent"):
        return True, f"read-only/coordination tool: {tool_name}"

    if tool_name in ("Write", "Edit", "NotebookEdit", "MultiEdit"):
        fp = (tool_input.get("file_path") or tool_input.get("path") or "")
        fp = fp.replace("\\", "/")
        if not fp:
            return False, ""
        for pat in ROUTINE_FILE_GLOBS:
            if fnmatch.fnmatch(fp, pat):
                return True, f"routine workspace path: {pat}"
        # Catch-all for anything under .claude/memory or /brain/ that the
        # explicit globs missed (subdirectories evolve over time).
        if "/.claude/memory/" in fp or "/brain/" in fp:
            return True, "claude memory/brain workspace"

    if tool_name == "Bash":
        cmd = (tool_input.get("command") or "").strip()
        if not cmd:
            return False, ""
        for prefix in ROUTINE_BASH_PREFIXES:
            if cmd.startswith(prefix):
                return True, f"routine bash: {prefix.strip()}"

    return False, ""

# Sentinel prompt — reused by both Python script and native CC prompt hook
SENTINEL_PROMPT = """You are a permission sentinel for an autonomous Claude Code agent.
Your job: decide whether a tool call is safe to auto-approve or should be blocked.

You operate AFTER a deterministic L1 pattern-matcher has already passed this
request to you, meaning routine workspace ops are already filtered out. You
only see EDGE CASES. Default to ALLOW.

DENY only when you see CONCRETE EVIDENCE of harm:
- Secrets being written to non-env files (literal "sk-…", "API_KEY=value", bearer tokens)
- Destructive flags on shared state: `rm -rf /`, `--force-push` to main, `DROP TABLE`,
  `git reset --hard origin/...`, overwriting critical configs without backup
- Privilege escalation: sudo, chmod 777 on system paths
- Network exfiltration: uploads to non-user-controlled hosts (NOT github.com / arxiv.org / jina.ai)
- Bypass safety hooks: --no-verify on commits, --no-gpg-sign

ALLOW everything else, including:
- Running the agent's own scripts under .claude/hooks/, .claude/scripts/, scripts/
- Bash flags like --apply, --all, --commit, --dry-run on local tooling (these are domain CLI flags, not hostile)
- Writes anywhere under .claude/memory/, brain/, outputs/, dreams/, learnings/
- Read-only fetches of public research (arxiv, github, jina reader)
- Git operations on the agent's own repo (status/log/diff/add/commit/push/branch)

Tool call:
TOOL: {tool_name}
INPUT: {tool_input_json}

Recent session context (last 5 tool calls, may be empty):
{session_context}

Respond with EXACTLY one of these two formats — no other text:

ALLOW: <one-sentence reason>

or

DENY: <one-sentence reason citing the specific harm evidence>

If you cannot point to concrete harm evidence from the lists above, the answer is ALLOW.
"""


def log_decision(decision: str, tool: str, reason: str, file_path: str = "", layer: str = "L2") -> None:
    """Append structured decision to sentinel-log.jsonl."""
    try:
        SENTINEL_LOG.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "layer": layer,
            "decision": decision,
            "tool": tool,
            "file_path": file_path,
            "reason": reason,
        }
        with open(SENTINEL_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass  # Logging must never block the hook


def emit_passthrough() -> None:
    """Empty {} = let CC fall through to next hook or default behavior."""
    print("{}")


def emit_allow(reason: str = "sentinel approved") -> None:
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PermissionRequest",
            "permissionDecision": "allow",
        },
        "suppressOutput": True,
    }
    print(json.dumps(out, ensure_ascii=False))


def emit_deny(reason: str) -> None:
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PermissionRequest",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        },
        "suppressOutput": False,
    }
    print(json.dumps(out, ensure_ascii=False))


def read_session_context(transcript_path: str, last_n: int = 5) -> str:
    """Extract last N tool calls from transcript for context. Best-effort, may return empty."""
    if not transcript_path or not Path(transcript_path).exists():
        return "(no transcript available)"
    try:
        # Transcript is JSONL — each line a turn
        with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        # Take last 50 lines, filter to tool_use entries
        tool_calls = []
        for line in lines[-50:]:
            try:
                entry = json.loads(line)
                # Try to extract tool name from various shapes
                content = entry.get("message", {}).get("content", [])
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get("type") == "tool_use":
                            name = c.get("name", "?")
                            tool_calls.append(name)
            except Exception:
                continue
        if not tool_calls:
            return "(no recent tool calls in transcript)"
        return ", ".join(tool_calls[-last_n:])
    except Exception:
        return "(transcript read error)"


def _load_api_key_from_secrets() -> str | None:
    """Fallback: read ANTHROPIC_API_KEY from ~/.claude/keys/secrets.env.

    Rationale: Claude Code desktop deliberately strips ANTHROPIC_API_KEY from
    child-process env (isolates subscription auth). Hooks run as children, so
    they cannot see the env var even when it's in settings.json. Fallback to
    the master secrets file — same source keys-sync.ps1 populates from.
    """
    try:
        secrets_path = Path.home() / ".claude" / "keys" / "secrets.env"
        if not secrets_path.exists():
            return None
        for line in secrets_path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line.startswith("ANTHROPIC_API_KEY="):
                value = line.split("=", 1)[1].strip()
                return value or None
    except Exception:
        return None
    return None


def call_claude_sentinel(tool_name: str, tool_input: dict, session_context: str) -> tuple[str, str]:
    """Call Claude API for sentinel decision. Returns (decision, reason).
    decision is 'ALLOW' | 'DENY' | 'ERROR'.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY") or _load_api_key_from_secrets()
    if not api_key:
        return ("ERROR", "no_api_key")

    try:
        import anthropic
    except ImportError:
        return ("ERROR", "anthropic_sdk_not_installed")

    try:
        client = anthropic.Anthropic(api_key=api_key, timeout=10.0)
        prompt = SENTINEL_PROMPT.format(
            tool_name=tool_name,
            tool_input_json=json.dumps(tool_input, ensure_ascii=False)[:1500],
            session_context=session_context,
        )
        # Haiku for fast/cheap decisions; cache the system prompt
        response = client.messages.create(
            # Model name configurable via env var; default to current Haiku
            model=os.environ.get("STOPA_SENTINEL_MODEL", "claude-haiku-4-5"),
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip() if response.content else ""
        # Parse "ALLOW: reason" or "DENY: reason"
        if text.upper().startswith("ALLOW:"):
            return ("ALLOW", text[6:].strip())
        elif text.upper().startswith("DENY:"):
            return ("DENY", text[5:].strip())
        else:
            return ("ERROR", f"unparseable_response: {text[:100]}")
    except Exception as e:
        return ("ERROR", f"api_error: {type(e).__name__}: {str(e)[:100]}")


def main() -> None:
    # Read stdin JSON
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        # Invalid JSON — passthrough so CC handles it
        emit_passthrough()
        return

    tool_name = (
        payload.get("tool_name")
        or payload.get("tool")
        or "unknown"
    )
    tool_input = payload.get("tool_input") or {}
    transcript_path = payload.get("transcript_path", "")
    file_path = tool_input.get("file_path", tool_input.get("path", ""))

    # Fast-skip: routine ops already cleared by L1 don't need a second LLM look.
    # Saves Haiku tokens + eliminates L2's false-DENY-on-uncertain failure mode
    # (e.g. "uncertain - escalate to human" on the agent's own hooks).
    is_routine, routine_reason = is_routine_op(tool_name, tool_input)
    if is_routine:
        log_decision("skip", tool_name, f"routine: {routine_reason}", file_path, layer="L2-skip")
        emit_passthrough()
        return

    # Dry-run mode: if STOPA_SENTINEL_DRYRUN=1, skip API call, log what would have been asked
    if os.environ.get("STOPA_SENTINEL_DRYRUN") == "1":
        log_decision("dryrun", tool_name, "would-call-api", file_path, layer="L2-dryrun")
        emit_passthrough()
        return

    # Get session context
    session_context = read_session_context(transcript_path, last_n=5)

    # Call sentinel
    decision, reason = call_claude_sentinel(tool_name, tool_input, session_context)

    if decision == "ALLOW":
        log_decision("allow", tool_name, reason, file_path, layer="L2")
        emit_allow(reason)
    elif decision == "DENY":
        log_decision("deny", tool_name, reason, file_path, layer="L2")
        emit_deny(f"sentinel: {reason}")
    else:  # ERROR
        log_decision("error", tool_name, reason, file_path, layer="L2-error")
        if reason == "no_api_key":
            # Graceful: no key configured -> let CC handle normally
            emit_passthrough()
        else:
            # Fail-closed for actual API errors / parse failures
            emit_deny(f"sentinel error: {reason}")


if __name__ == "__main__":
    main()

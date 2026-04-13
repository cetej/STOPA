#!/usr/bin/env python3
"""SessionStart hook: auto-retrieve relevant context from hybrid-retrieve.py.

Replaces passive memory brief with ACTIVE context injection:
1. Reads git state (branch, recent commits, modified files)
2. Reads checkpoint task if present
3. Builds query from git context → runs hybrid-retrieve.py
4. Outputs relevant learnings to stdout → injected into session context
5. Logs retrieval metrics to retrieval-log.jsonl

This is the READ side of memory — the biggest gap in STOPA's memory system.
"""
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

STOPA_ROOT = Path(__file__).resolve().parent.parent.parent
MEMORY_DIR = STOPA_ROOT / ".claude" / "memory"
LEARNINGS_DIR = MEMORY_DIR / "learnings"
RETRIEVAL_LOG = MEMORY_DIR / "retrieval-log.jsonl"
CHECKPOINT = MEMORY_DIR / "checkpoint.md"
STATE = MEMORY_DIR / "state.md"

MAX_CONTEXT_TOKENS = 2000  # ~8000 chars budget for injected context
MAX_CHARS = MAX_CONTEXT_TOKENS * 4


def run_cmd(cmd: list[str], timeout: int = 5) -> str:
    """Run shell command, return stdout or empty string."""
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            cwd=str(STOPA_ROOT), encoding="utf-8", errors="replace",
        )
        return r.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return ""


def get_git_context() -> dict:
    """Extract git context: branch, recent commits, modified files."""
    branch = run_cmd(["git", "branch", "--show-current"])
    # Last 5 commit messages (one-liners)
    log = run_cmd(["git", "log", "--oneline", "-5", "--no-decorate"])
    commits = [line.split(" ", 1)[1] if " " in line else line for line in log.splitlines()[:5]]
    # Modified files (staged + unstaged)
    diff_names = run_cmd(["git", "diff", "--name-only", "HEAD"])
    modified = [f for f in diff_names.splitlines()[:20] if f.strip()]

    return {"branch": branch, "commits": commits, "modified": modified}


def get_checkpoint_task() -> str:
    """Extract task description from checkpoint."""
    if not CHECKPOINT.exists():
        return ""
    try:
        text = CHECKPOINT.read_text(encoding="utf-8", errors="replace")[:2000]
        m = re.search(r"\*\*Task\*\*:\s*(.+)", text)
        if m and m.group(1).strip().lower() != "none":
            return m.group(1).strip()
    except OSError:
        pass
    return ""


def get_state_task() -> str:
    """Extract active task from state.md."""
    if not STATE.exists():
        return ""
    try:
        text = STATE.read_text(encoding="utf-8", errors="replace")[:1000]
        # Look for task name after "## Active Task"
        m = re.search(r"## Active Task\s*\n+(.+)", text)
        if m and "no active task" not in m.group(1).lower():
            return m.group(1).strip()
    except OSError:
        pass
    return ""


def build_query(git_ctx: dict, checkpoint_task: str, state_task: str) -> str:
    """Build hybrid search query from available context signals."""
    parts = []

    # Priority 1: active task from state.md
    if state_task:
        parts.append(state_task)

    # Priority 2: checkpoint task
    if checkpoint_task and checkpoint_task != state_task:
        parts.append(checkpoint_task)

    # Priority 3: recent commit messages (keywords)
    for commit in git_ctx.get("commits", [])[:3]:
        # Extract meaningful words from commit
        words = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{3,}", commit)
        parts.extend(w.lower() for w in words[:4])

    # Priority 4: modified file paths (extract component names)
    for fpath in git_ctx.get("modified", [])[:5]:
        # Extract meaningful parts: scripts/foo.py → "foo", .claude/hooks/bar.py → "hook bar"
        name = Path(fpath).stem
        if name not in ("__init__", "index", "main", "test"):
            parts.append(name.replace("-", " ").replace("_", " "))

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for p in parts:
        key = p.lower().strip()
        if key and key not in seen and len(key) > 2:
            seen.add(key)
            unique.append(p)

    query = " ".join(unique[:10])
    return query


def run_hybrid_retrieve(query: str) -> list[dict]:
    """Run hybrid-retrieve.py and parse JSON results."""
    if not query.strip():
        return []

    script = STOPA_ROOT / "scripts" / "hybrid-retrieve.py"
    if not script.exists():
        return []

    try:
        r = subprocess.run(
            [sys.executable, str(script), query, "--top", "5", "--json"],
            capture_output=True, text=True, timeout=10,
            cwd=str(STOPA_ROOT), encoding="utf-8", errors="replace",
        )
        if r.returncode == 0 and r.stdout.strip():
            return json.loads(r.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as e:
        print(f"[context-inject] hybrid-retrieve error: {e}", file=sys.stderr)
    return []


def read_learning_content(filename: str, max_chars: int = 600) -> str:
    """Read learning file and extract key content (summary + body)."""
    if filename.startswith("mp:"):
        return ""  # MemPalace entries have inline content
    fp = LEARNINGS_DIR / filename
    if not fp.exists():
        return ""
    try:
        text = fp.read_text(encoding="utf-8", errors="replace")
        # Extract summary from YAML
        m = re.search(r"^summary:\s*['\"]?(.+?)['\"]?\s*$", text, re.MULTILINE)
        summary = m.group(1) if m else ""
        # Extract body (after YAML frontmatter)
        body_match = re.search(r"^---\s*\n(.*)", text, re.DOTALL | re.MULTILINE)
        if body_match:
            body = body_match.group(1).strip()[:max_chars]
        else:
            body = text[:max_chars]
        return f"{summary}\n{body}" if summary else body
    except OSError:
        return ""


def log_retrieval(query: str, results: list[dict], git_ctx: dict):
    """Append retrieval metrics to JSONL log."""
    entry = {
        "ts": datetime.now().isoformat()[:19],
        "query": query[:200],
        "results": len(results),
        "sources": list({s for r in results for s in r.get("sources", [])}),
        "branch": git_ctx.get("branch", ""),
        "top_files": [r["filename"] for r in results[:3]],
    }
    try:
        with open(RETRIEVAL_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        # Rotate: keep last 200 lines
        lines = RETRIEVAL_LOG.read_text(encoding="utf-8", errors="replace").splitlines()
        if len(lines) > 200:
            RETRIEVAL_LOG.write_text("\n".join(lines[-200:]) + "\n", encoding="utf-8")
    except OSError:
        pass


def get_session_narrative() -> str:
    """Build a human-readable narrative of what happened in the last session.

    Reads checkpoint.md for: task, files touched, commits, errors, learnings.
    This is the CONVERSATIONAL context that learnings retrieval can't provide.
    """
    if not CHECKPOINT.exists():
        return ""
    try:
        text = CHECKPOINT.read_text(encoding="utf-8", errors="replace")[:3000]
    except OSError:
        return ""

    parts = []

    # Task
    m = re.search(r"\*\*Task\*\*:\s*(.+)", text)
    task = m.group(1).strip() if m else "none"

    # Last commit
    m = re.search(r"\*\*Last commit\*\*:\s*`?([^`\n]+)`?", text)
    commit = m.group(1).strip() if m else ""

    # Branch
    m = re.search(r"\*\*Branch\*\*:\s*(.+)", text)
    branch = m.group(1).strip() if m else ""

    # Session activity summary
    m = re.search(r"Session:\s*(.+?)(?:\n|$)", text)
    activity = m.group(1).strip() if m else ""

    # Files touched (top 5 from table)
    files = []
    for fm in re.finditer(r"\|\s*(\S+\.(?:py|md|sh|json|ts|js|yaml))\s*\|", text):
        f = fm.group(1)
        if f not in files and f != "File":
            files.append(f)
            if len(files) >= 5:
                break

    # Errors & corrections
    corrections = []
    for cm in re.finditer(r"\[correction\]\s*(.+)", text):
        corrections.append(cm.group(1).strip()[:80])
    frustrations = []
    for fm_match in re.finditer(r"\[frustration\]\s*(.+)", text):
        frustrations.append(fm_match.group(1).strip()[:80])

    # Learnings
    learnings = []
    for lm in re.finditer(r"- (2026-\S+)", text):
        learnings.append(lm.group(1))

    # Build narrative
    if task != "none":
        parts.append(f"Minulá session: task \"{task}\"")
    elif commit:
        parts.append(f"Minulá session: poslední commit {commit}")

    if activity:
        parts.append(f"Aktivita: {activity}")
    if files:
        parts.append(f"Hlavní soubory: {', '.join(files)}")
    if corrections:
        parts.append(f"Korekce od uživatele: {'; '.join(corrections[:3])}")
    if frustrations:
        parts.append(f"Frustrace: {'; '.join(frustrations[:2])}")
    if learnings:
        parts.append(f"Nové learnings: {len(learnings)}")

    return "\n".join(parts)


def get_state_files_summary() -> str:
    """Get short summary of files from state.md (what was being worked on)."""
    if not STATE.exists():
        return ""
    try:
        text = STATE.read_text(encoding="utf-8", errors="replace")[:1500]
    except OSError:
        return ""

    files = []
    for m in re.finditer(r"\|\s*(\S+)\s*\|\s*(\d+)\s*\|", text):
        fname = m.group(1)
        edits = m.group(2)
        if fname and fname != "File" and fname != "---":
            files.append(f"{fname} ({edits}x)")
    return ", ".join(files[:5])


def main():
    git_ctx = get_git_context()
    checkpoint_task = get_checkpoint_task()
    state_task = get_state_task()

    # === Part 1: Session narrative (what happened last time) ===
    narrative = get_session_narrative()
    state_summary = get_state_files_summary()

    # === Part 2: Relevant learnings (hybrid retrieval) ===
    query = build_query(git_ctx, checkpoint_task, state_task)
    results = []
    if query:
        results = run_hybrid_retrieve(query)
        log_retrieval(query, results, git_ctx)

    # === Build output ===
    has_narrative = bool(narrative.strip())
    has_results = len(results) > 0

    if not has_narrative and not has_results:
        sys.exit(0)

    output_parts = []
    total_chars = 0

    # Narrative section — ALWAYS first, this is what the user cares about
    if has_narrative:
        output_parts.append("=== SESSION CONTINUITY ===")
        output_parts.append(narrative)
        if state_summary:
            output_parts.append(f"State.md soubory: {state_summary}")
        output_parts.append("")
        total_chars += sum(len(p) for p in output_parts)

    # Learnings section — supplementary context
    if has_results:
        output_parts.append(f"=== RELEVANT LEARNINGS ({len(results)} matched) ===")
        for r in results:
            filename = r["filename"]
            sources = "+".join(r.get("sources", []))

            if filename.startswith("mp:") and r.get("mempalace_snippet"):
                content = r["mempalace_snippet"]
            else:
                content = read_learning_content(filename, max_chars=400)

            if not content:
                continue

            # Use just summary line, not full content — save tokens
            first_line = content.split("\n")[0].strip()
            entry = f"- [{sources}] {filename}: {first_line}"

            if total_chars + len(entry) > MAX_CHARS:
                break
            output_parts.append(entry)
            total_chars += len(entry)

    # === Explicit instruction for Claude ===
    output_parts.append("")
    output_parts.append("=== INSTRUCTION ===")
    if has_narrative:
        output_parts.append(
            "Na začátku session STRUČNĚ (2-3 věty) shrň uživateli co se dělo "
            "v minulé session a zeptej se jestli chce pokračovat nebo dělat něco jiného. "
            "Neříkej 'checkpoint říká' — prostě shrň kontext jako bys na to pamatoval."
        )
    else:
        output_parts.append(
            "Relevantní learnings byly načteny do kontextu. "
            "Použij je při práci, ale nemusíš je uživateli aktivně sdělovat."
        )

    print("\n".join(output_parts))
    sys.exit(0)


if __name__ == "__main__":
    main()

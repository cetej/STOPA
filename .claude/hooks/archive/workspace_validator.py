"""
Workspace Contract Validator for STOPA Orchestration.

Validates reads_from/writes_to contracts at three stages:
1. Subtask launch (Phase 4): readability + write disjointness
2. Wave boundary (Phase 4, inter-wave): write completion + downstream readiness
3. Task completion (Phase 5): B_ans completeness + orphan writes

Ref: workspace-schema.md (BIGMAS-aligned, arXiv:2603.15371)
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

Subtask = dict[str, Any]  # single subtask dict from state.md YAML


class ValidationError(Exception):
    """Raised when a workspace contract is violated."""


class ValidationWarning:
    """Non-fatal validation issue."""

    def __init__(self, subtask_id: str, message: str) -> None:
        self.subtask_id = subtask_id
        self.message = message

    def __repr__(self) -> str:
        return f"Warning[{self.subtask_id}]: {self.message}"


# ---------------------------------------------------------------------------
# 1. reads_from resolution
# ---------------------------------------------------------------------------

def resolve_reads(
    reads_from: list[str],
    subtasks: list[Subtask],
    project_root: Path | None = None,
) -> list[dict[str, str]]:
    """Resolve reads_from references to concrete paths/statuses.

    Args:
        reads_from: list of read references from a subtask
        subtasks: all subtasks in the plan (for st-N/output resolution)
        project_root: project root for file existence checks

    Returns:
        list of {"ref": original, "resolved": path_or_description, "status": "ok"|"error", "reason": ...}
    """
    root = project_root or Path(".")
    results = []

    for ref in reads_from:
        result: dict[str, str] = {"ref": ref, "resolved": "", "status": "ok", "reason": ""}

        # Pattern 1: st-N/output — upstream subtask artifacts
        m = re.match(r"^st-(\d+)/output$", ref)
        if m:
            st_id = f"st-{m.group(1)}"
            upstream = _find_subtask(subtasks, st_id)
            if upstream is None:
                result["status"] = "error"
                result["reason"] = f"Subtask {st_id} not found in plan"
            elif upstream.get("status") != "done":
                result["status"] = "error"
                result["reason"] = f"Subtask {st_id} status is '{upstream.get('status', 'unknown')}', expected 'done'"
            else:
                artifacts = upstream.get("artifacts", [])
                if not artifacts:
                    result["status"] = "error"
                    result["reason"] = f"Subtask {st_id} is done but has no artifacts"
                else:
                    result["resolved"] = ", ".join(str(a) for a in artifacts)
            results.append(result)
            continue

        # Pattern 2: grounding/<filename> — B_ctx zone (immutable)
        if ref.startswith("grounding/"):
            filename = ref[len("grounding/"):]
            # Check in orchestrate references directory
            candidates = [
                root / ".claude" / "skills" / "orchestrate" / "references" / filename,
                root / filename,
                root / ".claude" / filename,
            ]
            found = False
            for candidate in candidates:
                if candidate.exists():
                    result["resolved"] = str(candidate)
                    found = True
                    break
            if not found:
                result["status"] = "error"
                result["reason"] = f"Grounding file '{filename}' not found in any expected location"
            results.append(result)
            continue

        # Pattern 3: shared/<path> — cross-agent shared findings
        if ref.startswith("shared/"):
            shared_path = root / ".claude" / "memory" / "intermediate" / ref
            shared_dir = shared_path.parent
            if shared_dir.exists():
                result["resolved"] = str(shared_path)
                # shared/ directory existing is enough — file may not exist yet
            else:
                result["status"] = "error"
                result["reason"] = f"Shared directory '{shared_dir}' does not exist"
            results.append(result)
            continue

        # Unknown reference format
        result["status"] = "error"
        result["reason"] = f"Unknown reads_from format: '{ref}'"
        results.append(result)

    return results


# ---------------------------------------------------------------------------
# 2. writes_to disjointness check
# ---------------------------------------------------------------------------

def check_disjointness(subtasks: list[Subtask]) -> list[dict[str, Any]]:
    """Verify no two same-wave subtasks share write targets.

    Args:
        subtasks: all subtasks with 'wave' and 'writes_to' fields

    Returns:
        list of conflicts (empty = no conflicts). Each conflict:
        {"file": path, "subtasks": [id1, id2], "wave": N}
    """
    # Group subtasks by wave
    waves: dict[int, list[Subtask]] = {}
    for st in subtasks:
        wave = st.get("wave")
        if wave is None:
            continue
        waves.setdefault(wave, []).append(st)

    conflicts = []
    for wave_num, wave_subtasks in sorted(waves.items()):
        # Build file -> subtask_id mapping
        file_owners: dict[str, list[str]] = {}
        for st in wave_subtasks:
            st_id = st.get("id", "unknown")
            for path in st.get("writes_to", []):
                normalized = _normalize_path(path)
                file_owners.setdefault(normalized, []).append(st_id)

        # Find overlaps
        for filepath, owners in file_owners.items():
            if len(owners) > 1:
                conflicts.append({
                    "file": filepath,
                    "subtasks": owners,
                    "wave": wave_num,
                })

    return conflicts


# ---------------------------------------------------------------------------
# 3. Wave boundary validation
# ---------------------------------------------------------------------------

def validate_wave_completion(
    completed_subtasks: list[Subtask],
    next_wave_subtasks: list[Subtask] | None = None,
    all_subtasks: list[Subtask] | None = None,
    project_root: Path | None = None,
) -> dict[str, Any]:
    """Validate completed wave's outputs and next wave's readiness.

    Args:
        completed_subtasks: subtasks that just finished (current wave)
        next_wave_subtasks: subtasks to launch next (may be None if last wave)
        all_subtasks: full plan (for reads_from resolution)
        project_root: project root for file checks

    Returns:
        {"write_completion": [...], "downstream_readiness": [...], "passed": bool}
    """
    root = project_root or Path(".")
    all_sts = all_subtasks or completed_subtasks
    write_issues: list[dict[str, str]] = []
    readiness_issues: list[dict[str, str]] = []

    # 3a. Write completion — verify writes_to files exist and are non-empty
    for st in completed_subtasks:
        st_id = st.get("id", "unknown")
        if st.get("status") != "done":
            continue
        for filepath in st.get("writes_to", []):
            resolved = root / filepath
            if not resolved.exists():
                write_issues.append({
                    "subtask": st_id,
                    "file": filepath,
                    "issue": "File does not exist after subtask completion",
                })
            elif resolved.stat().st_size == 0:
                write_issues.append({
                    "subtask": st_id,
                    "file": filepath,
                    "issue": "File exists but is empty",
                })

    # 3b. Downstream readiness — verify next wave's reads_from are resolvable
    if next_wave_subtasks:
        for st in next_wave_subtasks:
            st_id = st.get("id", "unknown")
            reads = st.get("reads_from", [])
            if not reads:
                continue
            resolution = resolve_reads(reads, all_sts, root)
            for r in resolution:
                if r["status"] == "error":
                    readiness_issues.append({
                        "subtask": st_id,
                        "ref": r["ref"],
                        "issue": r["reason"],
                    })

    passed = len(write_issues) == 0 and len(readiness_issues) == 0
    return {
        "write_completion": write_issues,
        "downstream_readiness": readiness_issues,
        "passed": passed,
    }


# ---------------------------------------------------------------------------
# 4. Completion validation (B_ans)
# ---------------------------------------------------------------------------

def validate_completion(
    subtasks: list[Subtask],
    completion_contract: list[dict[str, str]] | None = None,
    project_root: Path | None = None,
) -> dict[str, Any]:
    """Validate task completion: B_ans completeness + orphan writes.

    Args:
        subtasks: all subtasks with writes_to and artifacts
        completion_contract: CC assertions from state.md (optional)
        project_root: for git diff cross-check

    Returns:
        {"orphan_writes": [...], "missing_artifacts": [...], "passed": bool}
    """
    root = project_root or Path(".")
    orphans: list[dict[str, str]] = []
    missing: list[dict[str, str]] = []

    # 4a. No orphan writes — every writes_to file was actually created
    for st in subtasks:
        st_id = st.get("id", "unknown")
        if st.get("status") not in ("done", "skipped:early_terminate"):
            continue
        if st.get("status") == "skipped:early_terminate":
            continue  # skipped subtasks don't need write validation

        for filepath in st.get("writes_to", []):
            resolved = root / filepath
            if not resolved.exists():
                orphans.append({
                    "subtask": st_id,
                    "file": filepath,
                    "issue": "Declared in writes_to but file does not exist",
                })

    # 4b. B_ans completeness — CC assertions reference existing files
    if completion_contract:
        for cc in completion_contract:
            check_method = cc.get("check_method", "")
            # Extract file paths from check methods (basic pattern matching)
            file_refs = _extract_file_refs(check_method)
            for fref in file_refs:
                fpath = root / fref
                if not fpath.exists():
                    missing.append({
                        "assertion": cc.get("id", "?"),
                        "file": fref,
                        "issue": "File referenced in CC assertion does not exist",
                    })

    # 4c. Git diff cross-check (optional, best-effort)
    git_changed = _get_git_changed_files(root)
    if git_changed is not None:
        declared_writes = set()
        for st in subtasks:
            if st.get("status") == "done":
                for fp in st.get("writes_to", []):
                    declared_writes.add(_normalize_path(fp))

        # Files changed but not declared in any writes_to
        undeclared = []
        for changed_file in git_changed:
            normalized = _normalize_path(changed_file)
            if normalized not in declared_writes:
                # Skip common non-workspace files
                if any(normalized.startswith(p) for p in (
                    ".claude/memory/state", ".claude/memory/budget",
                    ".claude/memory/intermediate/scratchpad",
                    ".claude/memory/intermediate/wave-checkpoint",
                )):
                    continue
                undeclared.append(changed_file)

        if undeclared:
            orphans.append({
                "subtask": "git-diff",
                "file": ", ".join(undeclared[:5]),
                "issue": f"Changed in git but not declared in any writes_to ({len(undeclared)} files)",
            })

    passed = len(orphans) == 0 and len(missing) == 0
    return {
        "orphan_writes": orphans,
        "missing_artifacts": missing,
        "passed": passed,
    }


# ---------------------------------------------------------------------------
# Combined validation entry points
# ---------------------------------------------------------------------------

def validate_at_launch(
    subtask: Subtask,
    all_subtasks: list[Subtask],
    same_wave_subtasks: list[Subtask],
    project_root: Path | None = None,
) -> dict[str, Any]:
    """Full validation before launching a subtask (Phase 4).

    Returns:
        {"reads_ok": bool, "disjoint_ok": bool, "issues": [...], "can_launch": bool}
    """
    root = project_root or Path(".")
    issues = []

    # Readability check
    reads = subtask.get("reads_from", [])
    if reads:
        resolution = resolve_reads(reads, all_subtasks, root)
        for r in resolution:
            if r["status"] == "error":
                issues.append(f"[reads_from] {r['ref']}: {r['reason']}")

    reads_ok = all(r["status"] == "ok" for r in resolve_reads(reads, all_subtasks, root)) if reads else True

    # Disjointness check (current subtask vs same-wave peers)
    conflicts = check_disjointness(same_wave_subtasks)
    st_id = subtask.get("id", "unknown")
    relevant_conflicts = [c for c in conflicts if st_id in c["subtasks"]]
    for c in relevant_conflicts:
        issues.append(f"[writes_to] File '{c['file']}' shared with {c['subtasks']}")

    disjoint_ok = len(relevant_conflicts) == 0

    return {
        "reads_ok": reads_ok,
        "disjoint_ok": disjoint_ok,
        "issues": issues,
        "can_launch": reads_ok and disjoint_ok,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _find_subtask(subtasks: list[Subtask], st_id: str) -> Subtask | None:
    for st in subtasks:
        if st.get("id") == st_id:
            return st
    return None


def _normalize_path(path: str) -> str:
    """Normalize path separators and remove leading ./"""
    return path.replace("\\", "/").lstrip("./")


def _extract_file_refs(check_method: str) -> list[str]:
    """Extract file paths from a CC check method string."""
    refs = []
    # Match quoted paths
    for m in re.finditer(r"['\"]([^'\"]+\.\w+)['\"]", check_method):
        refs.append(m.group(1))
    # Match path-like tokens
    for m in re.finditer(r"(?:^|\s)([\w./-]+\.\w{1,5})(?:\s|$)", check_method):
        candidate = m.group(1)
        if candidate not in refs and "/" in candidate:
            refs.append(candidate)
    return refs


def _get_git_changed_files(root: Path) -> list[str] | None:
    """Get list of files changed in working tree via git diff."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True, text=True, cwd=str(root), timeout=10,
        )
        if result.returncode == 0:
            return [f for f in result.stdout.strip().split("\n") if f]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


# ---------------------------------------------------------------------------
# CLI / quick test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Quick self-test with mock data
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    mock_subtasks: list[Subtask] = [
        {
            "id": "st-1", "wave": 1, "status": "done",
            "artifacts": ["intermediate/test/st-1.json"],
            "reads_from": [],
            "writes_to": ["src/validator.py", "intermediate/test/st-1.json"],
        },
        {
            "id": "st-2", "wave": 1, "status": "done",
            "artifacts": ["intermediate/test/st-2.json"],
            "reads_from": [],
            "writes_to": ["src/checker.py", "intermediate/test/st-2.json"],
        },
        {
            "id": "st-3", "wave": 2, "status": "pending",
            "reads_from": ["st-1/output", "grounding/workspace-schema.md"],
            "writes_to": ["src/validator.py", "intermediate/test/st-3.json"],
        },
    ]

    print("=== resolve_reads test ===")
    reads_result = resolve_reads(
        ["st-1/output", "grounding/workspace-schema.md", "shared/notes.md"],
        mock_subtasks,
    )
    for r in reads_result:
        print(f"  {r['ref']}: {r['status']} — {r.get('reason') or r.get('resolved', 'ok')}")

    print("\n=== check_disjointness test ===")
    conflicts = check_disjointness(mock_subtasks)
    print(f"  Conflicts: {conflicts if conflicts else 'none (wave 1 clean)'}")

    # Test with intentional conflict
    conflicting = [
        {"id": "st-a", "wave": 1, "writes_to": ["shared.py"]},
        {"id": "st-b", "wave": 1, "writes_to": ["shared.py", "other.py"]},
    ]
    conflicts2 = check_disjointness(conflicting)
    print(f"  Conflict test: {conflicts2}")

    print("\n=== validate_wave_completion test ===")
    wave_result = validate_wave_completion(
        completed_subtasks=[mock_subtasks[0], mock_subtasks[1]],
        next_wave_subtasks=[mock_subtasks[2]],
        all_subtasks=mock_subtasks,
    )
    print(f"  Passed: {wave_result['passed']}")
    if wave_result["write_completion"]:
        print(f"  Write issues: {wave_result['write_completion']}")
    if wave_result["downstream_readiness"]:
        print(f"  Readiness issues: {wave_result['downstream_readiness']}")

    print("\n=== validate_completion test ===")
    completion_result = validate_completion(mock_subtasks)
    print(f"  Passed: {completion_result['passed']}")
    if completion_result["orphan_writes"]:
        print(f"  Orphans: {completion_result['orphan_writes']}")

    print("\nAll tests completed.")

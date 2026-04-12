"""Integration tests for workspace-validator.py.

Tests 3 scenarios:
1. Valid orchestration trace (all contracts satisfied)
2. Invalid: write disjointness conflict in same wave
3. Invalid: reads_from referencing non-done subtask
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

# Add hooks directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / ".claude" / "hooks"))

from workspace_validator import (
    ValidationError,
    check_disjointness,
    resolve_reads,
    validate_at_launch,
    validate_completion,
    validate_wave_completion,
)


def _make_project(tmp: Path) -> Path:
    """Create a minimal project structure for testing."""
    root = tmp / "project"
    root.mkdir()
    # Create orchestrate references directory with workspace-schema.md
    refs = root / ".claude" / "skills" / "orchestrate" / "references"
    refs.mkdir(parents=True)
    (refs / "workspace-schema.md").write_text("# Workspace Schema\nTest fixture.", encoding="utf-8")
    # Create intermediate shared directory
    shared = root / ".claude" / "memory" / "intermediate" / "shared"
    shared.mkdir(parents=True)
    # Create task intermediate directory
    task_dir = root / ".claude" / "memory" / "intermediate" / "test-task"
    task_dir.mkdir(parents=True)
    return root


def _write_file(root: Path, relpath: str, content: str = "non-empty") -> None:
    p = root / relpath
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


# ─── Test 1: Valid orchestration trace ────────────────────────────────────

def test_valid_trace():
    """A complete, valid 3-wave orchestration: all reads resolve, no conflicts, writes complete."""
    with tempfile.TemporaryDirectory() as tmp:
        root = _make_project(Path(tmp))
        task_id = "test-task"
        inter = f".claude/memory/intermediate/{task_id}"

        # Simulate completed wave 1 outputs
        _write_file(root, f"{inter}/st-1.json", json.dumps({"status": "complete"}))
        _write_file(root, "src/resolver.py", "# resolver code")

        # Simulate completed wave 2 outputs
        _write_file(root, f"{inter}/st-2.json", json.dumps({"status": "complete"}))
        _write_file(root, "src/checker.py", "# checker code")

        subtasks = [
            {
                "id": "st-1", "wave": 1, "status": "done",
                "artifacts": [f"{inter}/st-1.json"],
                "reads_from": [],
                "writes_to": ["src/resolver.py", f"{inter}/st-1.json"],
            },
            {
                "id": "st-2", "wave": 1, "status": "done",
                "artifacts": [f"{inter}/st-2.json"],
                "reads_from": [],
                "writes_to": ["src/checker.py", f"{inter}/st-2.json"],
            },
            {
                "id": "st-3", "wave": 2, "status": "done",
                "artifacts": [f"{inter}/st-3.json"],
                "reads_from": ["st-1/output", "grounding/workspace-schema.md"],
                "writes_to": ["src/boundary.py", f"{inter}/st-3.json"],
            },
        ]

        # Simulate wave 2 outputs
        _write_file(root, f"{inter}/st-3.json", json.dumps({"status": "complete"}))
        _write_file(root, "src/boundary.py", "# boundary code")

        # Test 1a: No disjointness conflicts in wave 1
        conflicts = check_disjointness(subtasks)
        assert conflicts == [], f"Expected no conflicts, got: {conflicts}"

        # Test 1b: reads_from resolution works for wave 2 subtask
        reads = resolve_reads(
            ["st-1/output", "grounding/workspace-schema.md"],
            subtasks,
            root,
        )
        for r in reads:
            assert r["status"] == "ok", f"Read failed: {r}"

        # Test 1c: Wave completion validation passes
        wave1_done = [s for s in subtasks if s["wave"] == 1]
        wave2_sts = [s for s in subtasks if s["wave"] == 2]
        result = validate_wave_completion(
            completed_subtasks=wave1_done,
            next_wave_subtasks=wave2_sts,
            all_subtasks=subtasks,
            project_root=root,
        )
        assert result["passed"], f"Wave completion failed: {result}"

        # Test 1d: Full completion validation passes
        completion = validate_completion(subtasks, project_root=root)
        assert completion["passed"], f"Completion failed: {completion}"

    print("  PASS: test_valid_trace")


# ─── Test 2: Invalid — write disjointness conflict ───────────────────────

def test_invalid_conflict():
    """Two wave-1 subtasks write to the same file — must be caught."""
    subtasks = [
        {
            "id": "st-a", "wave": 1, "status": "pending",
            "reads_from": [],
            "writes_to": ["src/shared_module.py", "intermediate/st-a.json"],
        },
        {
            "id": "st-b", "wave": 1, "status": "pending",
            "reads_from": [],
            "writes_to": ["src/shared_module.py", "intermediate/st-b.json"],
        },
    ]

    conflicts = check_disjointness(subtasks)
    assert len(conflicts) == 1, f"Expected 1 conflict, got {len(conflicts)}: {conflicts}"
    assert "src/shared_module.py" in conflicts[0]["file"]
    assert set(conflicts[0]["subtasks"]) == {"st-a", "st-b"}
    assert conflicts[0]["wave"] == 1

    # Also test validate_at_launch catches it
    with tempfile.TemporaryDirectory() as tmp:
        root = _make_project(Path(tmp))
        launch_result = validate_at_launch(
            subtask=subtasks[0],
            all_subtasks=subtasks,
            same_wave_subtasks=subtasks,
            project_root=root,
        )
        assert not launch_result["can_launch"], f"Should not be launchable: {launch_result}"
        assert not launch_result["disjoint_ok"]
        assert any("shared_module.py" in issue for issue in launch_result["issues"])

    print("  PASS: test_invalid_conflict")


# ─── Test 3: Invalid — reads_from referencing non-done subtask ───────────

def test_invalid_reads():
    """Wave-2 subtask reads from wave-1 subtask that is still pending — must be caught."""
    subtasks = [
        {
            "id": "st-1", "wave": 1, "status": "pending",  # NOT done!
            "artifacts": [],
            "reads_from": [],
            "writes_to": ["src/auth.py"],
        },
        {
            "id": "st-2", "wave": 2, "status": "pending",
            "reads_from": ["st-1/output", "grounding/nonexistent-file.md"],
            "writes_to": ["src/middleware.py"],
        },
    ]

    with tempfile.TemporaryDirectory() as tmp:
        root = _make_project(Path(tmp))

        # Test reads_from resolution catches both issues
        reads = resolve_reads(subtasks[1]["reads_from"], subtasks, root)

        # st-1/output should fail (not done)
        st1_read = [r for r in reads if r["ref"] == "st-1/output"][0]
        assert st1_read["status"] == "error", f"Should fail: {st1_read}"
        assert "pending" in st1_read["reason"]

        # grounding/nonexistent-file.md should fail (doesn't exist)
        grounding_read = [r for r in reads if "nonexistent" in r["ref"]][0]
        assert grounding_read["status"] == "error", f"Should fail: {grounding_read}"

        # validate_at_launch should block
        launch_result = validate_at_launch(
            subtask=subtasks[1],
            all_subtasks=subtasks,
            same_wave_subtasks=[subtasks[1]],  # wave 2 has only st-2
            project_root=root,
        )
        assert not launch_result["can_launch"], f"Should not launch: {launch_result}"
        assert not launch_result["reads_ok"]

    print("  PASS: test_invalid_reads")


# ─── Runner ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("Running workspace validator integration tests...\n")

    test_valid_trace()
    test_invalid_conflict()
    test_invalid_reads()

    print("\nAll 3 tests PASSED.")

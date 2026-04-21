"""test_memory_backend.py — Contract tests for MemoryBackend implementations.

Both LocalMemoryAdapter and CMMemoryAdapter must pass the same test suite.
This proves the abstraction is sound and migration = adapter swap.

Run:
    cd STOPA
    python -m pytest tests/test_memory_backend.py -v
  or:
    python tests/test_memory_backend.py  (plain unittest fallback)
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

# Make .claude/lib importable
_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / ".claude" / "lib"))

from memory_backend import MemoryBackend, MemoryEntry, SearchResult
from local_memory_adapter import LocalMemoryAdapter
from cmm_memory_adapter import CMMemoryAdapter


# ── Shared contract test mixin ────────────────────────────────────────────────

class MemoryBackendContractTests:
    """Mixin that defines the shared contract test suite.

    Subclasses must define:
        self.backend: MemoryBackend   — the adapter under test
    """

    # ── write-then-read ───────────────────────────────────────────────────────

    def test_write_then_read(self):
        """write() creates a memory; read() retrieves it by ID."""
        backend: MemoryBackend = self.backend
        entry = backend.write(
            memory_id="test-write-read",
            content="Test content for write-then-read.",
            metadata={"type": "best_practice", "severity": "low",
                      "component": "general", "tags": ["test"]},
        )
        self.assertIsInstance(entry, MemoryEntry)
        self.assertEqual(entry.id, "test-write-read")
        self.assertIn("Test content", entry.content)

        fetched = backend.read("test-write-read")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.id, "test-write-read")
        self.assertIn("Test content", fetched.content)

    def test_read_missing_returns_none(self):
        """read() on unknown ID returns None (not an exception)."""
        result = self.backend.read("definitely-does-not-exist-xyz")
        self.assertIsNone(result)

    def test_write_duplicate_raises(self):
        """write() on an existing ID raises (FileExistsError or similar)."""
        self.backend.write(
            memory_id="test-dup",
            content="first write",
            metadata={"type": "best_practice", "severity": "low",
                      "component": "general"},
        )
        with self.assertRaises(Exception):
            self.backend.write(
                memory_id="test-dup",
                content="second write",
                metadata={},
            )

    # ── list-filter ───────────────────────────────────────────────────────────

    def test_list_all_returns_entries(self):
        """list() returns at least the entries we wrote."""
        self.backend.write(
            memory_id="test-list-a",
            content="Entry A",
            metadata={"type": "bug_fix", "severity": "high",
                      "component": "skill", "tags": ["alpha"]},
        )
        self.backend.write(
            memory_id="test-list-b",
            content="Entry B",
            metadata={"type": "best_practice", "severity": "low",
                      "component": "hook", "tags": ["beta"]},
        )
        entries = self.backend.list()
        ids = [e.id for e in entries]
        self.assertIn("test-list-a", ids)
        self.assertIn("test-list-b", ids)

    def test_list_filter_by_type(self):
        """list(filter={"type": "bug_fix"}) returns only bug_fix entries."""
        self.backend.write(
            memory_id="test-filter-bug",
            content="Bug fix entry",
            metadata={"type": "bug_fix", "severity": "high",
                      "component": "general", "tags": ["filter-test"]},
        )
        self.backend.write(
            memory_id="test-filter-bp",
            content="Best practice entry",
            metadata={"type": "best_practice", "severity": "low",
                      "component": "general", "tags": ["filter-test"]},
        )
        bug_entries = self.backend.list(filter={"type": "bug_fix"})
        bug_ids = [e.id for e in bug_entries]
        self.assertIn("test-filter-bug", bug_ids)
        self.assertNotIn("test-filter-bp", bug_ids)

    def test_list_filter_no_matches(self):
        """list(filter={"component": "nonexistent"}) returns empty list."""
        results = self.backend.list(filter={"component": "nonexistent_xyz"})
        self.assertEqual(results, [])

    # ── search ────────────────────────────────────────────────────────────────

    def test_search_returns_results(self):
        """search() on a known keyword returns at least one result."""
        self.backend.write(
            memory_id="test-search-unique",
            content="flibbertigibbet sentinel concept for search test",
            metadata={"type": "best_practice", "severity": "low",
                      "component": "general", "tags": ["searchtest"]},
        )
        results = self.backend.search("flibbertigibbet sentinel", k=5)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        for r in results:
            self.assertIsInstance(r, SearchResult)
            self.assertIsInstance(r.entry, MemoryEntry)
            self.assertIsInstance(r.score, float)
            self.assertGreater(r.score, 0)

    def test_search_respects_k(self):
        """search() returns at most k results."""
        results = self.backend.search("the", k=2)
        self.assertLessEqual(len(results), 2)

    def test_search_empty_query(self):
        """search() on empty string returns empty list (graceful, no crash)."""
        results = self.backend.search("", k=5)
        self.assertIsInstance(results, list)

    # ── edit-preserves-metadata ───────────────────────────────────────────────

    def test_edit_updates_content(self):
        """edit() with new content replaces old content."""
        self.backend.write(
            memory_id="test-edit-content",
            content="Original content",
            metadata={"type": "best_practice", "severity": "low",
                      "component": "general"},
        )
        updated = self.backend.edit(
            memory_id="test-edit-content",
            content="Updated content",
        )
        self.assertIn("Updated", updated.content)
        self.assertNotIn("Original", updated.content)

    def test_edit_preserves_existing_metadata(self):
        """edit(metadata=partial) merges, does not destroy other fields."""
        self.backend.write(
            memory_id="test-edit-meta",
            content="Body",
            metadata={"type": "bug_fix", "severity": "high",
                      "component": "skill", "tags": ["keep-me"]},
        )
        updated = self.backend.edit(
            memory_id="test-edit-meta",
            metadata={"severity": "low"},  # only change severity
        )
        # Original fields still present
        self.assertEqual(updated.metadata.get("type"), "bug_fix")
        self.assertEqual(updated.metadata.get("component"), "skill")
        # Updated field changed
        self.assertEqual(updated.metadata.get("severity"), "low")

    def test_edit_missing_raises(self):
        """edit() on non-existent ID raises (KeyError or similar)."""
        with self.assertRaises(Exception):
            self.backend.edit("definitely-missing-xyz", content="anything")

    def test_edit_increments_version(self):
        """edit() increments the version number."""
        self.backend.write(
            memory_id="test-version",
            content="v1",
            metadata={"type": "best_practice", "severity": "low",
                      "component": "general"},
        )
        v1 = self.backend.read("test-version")
        self.backend.edit("test-version", content="v2")
        v2 = self.backend.read("test-version")
        self.assertGreater(v2.version, v1.version)

    # ── delete-archives-not-destroys ──────────────────────────────────────────

    def test_delete_returns_true_on_success(self):
        """delete() returns True when memory existed."""
        self.backend.write(
            memory_id="test-delete-exists",
            content="Will be deleted",
            metadata={"type": "best_practice", "severity": "low",
                      "component": "general"},
        )
        result = self.backend.delete("test-delete-exists")
        self.assertTrue(result)

    def test_delete_returns_false_on_missing(self):
        """delete() returns False when memory does not exist."""
        result = self.backend.delete("never-existed-xyz-987")
        self.assertFalse(result)

    def test_delete_removes_from_list(self):
        """After delete(), the entry no longer appears in list()."""
        self.backend.write(
            memory_id="test-delete-gone",
            content="Gone",
            metadata={"type": "best_practice", "severity": "low",
                      "component": "general"},
        )
        self.backend.delete("test-delete-gone")
        ids = [e.id for e in self.backend.list()]
        self.assertNotIn("test-delete-gone", ids)

    def test_delete_removes_from_read(self):
        """After delete(), read() returns None for the deleted ID."""
        self.backend.write(
            memory_id="test-delete-read",
            content="Will vanish",
            metadata={"type": "best_practice", "severity": "low",
                      "component": "general"},
        )
        self.backend.delete("test-delete-read")
        result = self.backend.read("test-delete-read")
        self.assertIsNone(result)


# ── Concrete test cases ───────────────────────────────────────────────────────

class TestLocalMemoryAdapter(MemoryBackendContractTests, unittest.TestCase):
    """Contract tests for LocalMemoryAdapter with temp-dir isolation."""

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        learnings_dir = Path(self._tmpdir.name) / "learnings"
        learnings_dir.mkdir()
        self.backend = LocalMemoryAdapter(learnings_dir=learnings_dir)

    def tearDown(self):
        self._tmpdir.cleanup()

    def test_delete_archives_to_file(self):
        """LocalMemoryAdapter.delete() moves content to learnings-archive.md."""
        self.backend.write(
            memory_id="test-archive",
            content="Archive me",
            metadata={"type": "best_practice", "severity": "low",
                      "component": "general"},
        )
        self.backend.delete("test-archive")
        archive = self.backend._archive_path()
        self.assertTrue(archive.exists())
        archive_text = archive.read_text(encoding="utf-8")
        self.assertIn("test-archive", archive_text)


class TestCMMemoryAdapter(MemoryBackendContractTests, unittest.TestCase):
    """Contract tests for CMMemoryAdapter (mock implementation)."""

    def setUp(self):
        # Fresh instance per test (new in-memory store, no mock entries)
        self.backend = CMMemoryAdapter(store_id="test-store")
        # Clear mock entries to start clean
        self.backend._store.clear()

    def test_mock_store_id(self):
        """CMMemoryAdapter stores the provided store_id."""
        adapter = CMMemoryAdapter(store_id="my-store")
        self.assertEqual(adapter._store_id, "my-store")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main(verbosity=2)

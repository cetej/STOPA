"""memory_backend.py — Abstract base class for STOPA memory backends.

Defines a contract with 6 methods that mirror the Claude Managed Memory (CMM)
API surface. Current implementation: LocalMemoryAdapter (file-based learnings).
Future: CMMemoryAdapter (CMM GA, Q2-Q3 2026).

CMM equivalence map:
  list()   → memories.list()
  search() → memories.search()
  read()   → memories.get(memory_id)
  write()  → memories.create()
  edit()   → memories.update(memory_id)
  delete() → memories.delete(memory_id)

Ref: ADR 0017 (docs/decisions/0017-memory-backend-abstraction.md)
"""
from __future__ import annotations

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


# ── Data classes ─────────────────────────────────────────────────────────────


@dataclass
class MemoryEntry:
    """Represents a single memory item across any backend.

    CMM equivalent: a memory object with id, content, metadata fields.

    Attributes:
        id:         Stable slug identifier (filename without .md in local backend).
        content:    Full text body (after YAML frontmatter in local files).
        metadata:   YAML frontmatter fields as a dict (type, severity, tags, …).
        created_at: ISO-format string or datetime of creation.
        updated_at: ISO-format string or datetime of last modification.
        version:    Monotonic integer. Local backend uses mtime-based int.
    """
    id: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""
    version: int = 1


@dataclass
class SearchResult:
    """A ranked retrieval result from search().

    Attributes:
        entry:   The matched MemoryEntry.
        score:   Fused relevance score (RRF or backend-native).
        sources: Which signals contributed — e.g. ["grep", "bm25", "graph"].
    """
    entry: MemoryEntry
    score: float
    sources: list[str] = field(default_factory=list)


# ── Abstract backend ──────────────────────────────────────────────────────────


class MemoryBackend(ABC):
    """Abstract interface for STOPA memory storage.

    All concrete adapters must implement these 6 methods. The method
    signatures are intentionally close to the CMM API to make future
    migration a single-class swap.
    """

    @abstractmethod
    def list(self, filter: dict[str, Any] | None = None) -> list[MemoryEntry]:
        """Return all memories, optionally filtered by metadata fields.

        CMM equivalent: memories.list(filter=…)

        Args:
            filter: Dict of metadata key→value pairs. Only entries matching
                    ALL provided key-value pairs are returned. None = return all.

        Returns:
            List of MemoryEntry objects, ordered by updated_at descending.
        """
        ...

    @abstractmethod
    def search(
        self,
        query: str,
        k: int = 8,
        task_tier: str = "standard",
    ) -> list[SearchResult]:
        """Hybrid semantic + keyword search across all memories.

        CMM equivalent: memories.search(query=…, k=…)

        Args:
            query:      Natural-language search string.
            k:          Maximum number of results to return.
            task_tier:  Budget tier hint — "light" | "standard" | "deep".
                        Deep tier activates additional retrieval signals.

        Returns:
            Up to k SearchResult objects ordered by descending score.
        """
        ...

    @abstractmethod
    def read(self, memory_id: str) -> MemoryEntry | None:
        """Fetch a single memory by its stable ID.

        CMM equivalent: memories.get(memory_id)

        Args:
            memory_id: Slug identifier (filename without .md in local backend).

        Returns:
            MemoryEntry if found, None otherwise.
        """
        ...

    @abstractmethod
    def write(
        self,
        memory_id: str,
        content: str,
        metadata: dict[str, Any],
    ) -> MemoryEntry:
        """Create a new memory. Raises if memory_id already exists.

        CMM equivalent: memories.create(id=…, content=…, metadata=…)

        Args:
            memory_id: Desired slug identifier. Must be unique.
            content:   Text body of the memory.
            metadata:  Dict of YAML-frontmatter-equivalent fields.

        Returns:
            The newly created MemoryEntry.

        Raises:
            FileExistsError (local) or equivalent if memory_id already exists.
        """
        ...

    @abstractmethod
    def edit(
        self,
        memory_id: str,
        content: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> MemoryEntry:
        """Update an existing memory. Preserves fields not explicitly changed.

        CMM equivalent: memories.update(memory_id, …)

        Args:
            memory_id: Slug of the memory to update.
            content:   New text body. None = preserve existing.
            metadata:  Partial dict of fields to merge into existing metadata.
                       None = preserve existing metadata unchanged.

        Returns:
            Updated MemoryEntry.

        Raises:
            KeyError if memory_id does not exist.
        """
        ...

    @abstractmethod
    def delete(self, memory_id: str) -> bool:
        """Remove (or archive) a memory.

        Per core-invariant #5: local backend NEVER destroys — it moves to
        learnings-archive.md. CMM backend will call memories.delete().

        CMM equivalent: memories.delete(memory_id)

        Args:
            memory_id: Slug of the memory to remove.

        Returns:
            True if deletion/archival succeeded, False if memory_id not found.
        """
        ...

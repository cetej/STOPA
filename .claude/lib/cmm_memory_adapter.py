"""cmm_memory_adapter.py — Mock CMM (Claude Managed Memory) backend.

This is a MOCK adapter demonstrating the contract shape. No real Anthropic
beta API calls are made. When CMM reaches GA (Q2-Q3 2026), replace the
stub bodies with real `anthropic.beta.memory.*` calls.

TODO(cmm-ga): Replace stub implementations with real Anthropic SDK calls.
  Expected SDK surface at GA (based on Research Preview docs):
    client.beta.memory.list(store_id=…)
    client.beta.memory.search(store_id=…, query=…, k=…)
    client.beta.memory.get(store_id=…, memory_id=…)
    client.beta.memory.create(store_id=…, content=…, metadata=…)
    client.beta.memory.update(store_id=…, memory_id=…, …)
    client.beta.memory.delete(store_id=…, memory_id=…)

  Prerequisites:
    pip install anthropic>=0.30 (version with memory beta)
    ANTHROPIC_API_KEY in env or ~/.claude/keys/secrets.env
    Store created once per workspace (max 8/session, 100KB/memory)

Ref: ADR 0017 (docs/decisions/0017-memory-backend-abstraction.md)
     ADR 0016 Phase C verdict — Sub-decision 1 (B)
"""
from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from memory_backend import MemoryBackend, MemoryEntry, SearchResult


# ── API key loading (mirrors permission-sentinel.py pattern) ─────────────────

def _load_api_key() -> str | None:
    """Try env first, fall back to ~/.claude/keys/secrets.env."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key

    secrets_path = Path.home() / ".claude" / "keys" / "secrets.env"
    if secrets_path.exists():
        try:
            for line in secrets_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("ANTHROPIC_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"\'')
        except OSError:
            pass

    return None


# ── Mock data ────────────────────────────────────────────────────────────────

_MOCK_STORE: dict[str, MemoryEntry] = {
    "mock-entry-01": MemoryEntry(
        id="mock-entry-01",
        content="Example CMM memory: orchestration patterns work best with explicit handoffs.",
        metadata={
            "type": "best_practice",
            "severity": "medium",
            "component": "orchestration",
            "tags": ["orchestration", "handoff"],
            "source": "cmm_mock",
            "confidence": 0.85,
        },
        created_at="2026-04-21",
        updated_at="2026-04-21",
        version=1,
    ),
    "mock-entry-02": MemoryEntry(
        id="mock-entry-02",
        content="Example CMM memory: permission sentinel pattern reduces approval prompts.",
        metadata={
            "type": "architecture",
            "severity": "high",
            "component": "hook",
            "tags": ["permission", "sentinel", "hooks"],
            "source": "cmm_mock",
            "confidence": 0.9,
        },
        created_at="2026-04-21",
        updated_at="2026-04-21",
        version=1,
    ),
}


# ── Adapter class ────────────────────────────────────────────────────────────


class CMMemoryAdapter(MemoryBackend):
    """Mock CMM backend demonstrating the MemoryBackend contract shape.

    When CMM reaches GA, this class will be replaced with real
    `anthropic.beta.memory.*` calls. The constructor will:
      1. Load ANTHROPIC_API_KEY
      2. Create/connect to a named memory store (workspace-scoped)
      3. Pass store_id to all methods

    Current state: returns plausible fixed responses from an in-memory dict.
    No network calls. Safe to run in any environment.

    TODO(cmm-ga): implement real store management:
      self._store_id = self._get_or_create_store("stopa-learnings")
    """

    def __init__(self, store_id: str = "stopa-learnings") -> None:
        """Initialize mock CMM adapter.

        Args:
            store_id: Logical name for the CMM memory store.
                      TODO(cmm-ga): Use this to call
                      client.beta.memory_stores.create(name=store_id)
                      or retrieve existing store by name.
        """
        self._store_id = store_id
        self._api_key = _load_api_key()
        # In-memory dict simulates the CMM store for this session
        self._store: dict[str, MemoryEntry] = dict(_MOCK_STORE)

        # TODO(cmm-ga): initialize Anthropic client
        # import anthropic
        # self._client = anthropic.Anthropic(api_key=self._api_key)
        # self._store_obj = self._get_or_create_store(store_id)

    # ── list ─────────────────────────────────────────────────────────────────

    def list(self, filter: dict[str, Any] | None = None) -> list[MemoryEntry]:
        """List memories from mock store, optionally filtered.

        TODO(cmm-ga):
            results = self._client.beta.memory.list(store_id=self._store_id)
            return [self._to_entry(r) for r in results]
        """
        entries = list(self._store.values())
        if filter:
            entries = [e for e in entries if self._matches_filter(e, filter)]
        return sorted(entries, key=lambda e: e.updated_at, reverse=True)

    # ── search ────────────────────────────────────────────────────────────────

    def search(
        self,
        query: str,
        k: int = 8,
        task_tier: str = "standard",
    ) -> list[SearchResult]:
        """Mock semantic search — returns any entries whose content mentions query terms.

        TODO(cmm-ga):
            results = self._client.beta.memory.search(
                store_id=self._store_id,
                query=query,
                k=k,
            )
            return [SearchResult(entry=self._to_entry(r), score=r.score,
                                 sources=["cmm"]) for r in results]
        """
        terms = [t.lower() for t in query.split() if len(t) >= 3]
        results: list[SearchResult] = []
        for entry in self._store.values():
            text = (entry.content + " " + str(entry.metadata)).lower()
            hits = sum(1 for t in terms if t in text)
            if hits > 0:
                score = hits / max(len(terms), 1)
                results.append(SearchResult(
                    entry=entry,
                    score=score,
                    sources=["cmm_mock"],
                ))
        results.sort(key=lambda r: -r.score)
        return results[:k]

    # ── read ─────────────────────────────────────────────────────────────────

    def read(self, memory_id: str) -> MemoryEntry | None:
        """Fetch a single memory by ID from mock store.

        TODO(cmm-ga):
            result = self._client.beta.memory.get(
                store_id=self._store_id, memory_id=memory_id
            )
            return self._to_entry(result) if result else None
        """
        return self._store.get(memory_id)

    # ── write ─────────────────────────────────────────────────────────────────

    def write(
        self,
        memory_id: str,
        content: str,
        metadata: dict[str, Any],
    ) -> MemoryEntry:
        """Create a new memory in mock store. Raises if ID exists.

        TODO(cmm-ga):
            result = self._client.beta.memory.create(
                store_id=self._store_id,
                content=content,
                metadata=metadata,
            )
            return self._to_entry(result)
        """
        if memory_id in self._store:
            raise FileExistsError(f"CMM memory '{memory_id}' already exists")

        now = datetime.now().strftime("%Y-%m-%d")
        if "date" not in metadata:
            metadata = {**metadata, "date": now}

        entry = MemoryEntry(
            id=memory_id,
            content=content,
            metadata=metadata,
            created_at=now,
            updated_at=now,
            version=1,
        )
        self._store[memory_id] = entry
        return entry

    # ── edit ─────────────────────────────────────────────────────────────────

    def edit(
        self,
        memory_id: str,
        content: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> MemoryEntry:
        """Update an existing memory in mock store.

        TODO(cmm-ga):
            result = self._client.beta.memory.update(
                store_id=self._store_id,
                memory_id=memory_id,
                content=content,
                metadata=metadata,
            )
            return self._to_entry(result)
        """
        if memory_id not in self._store:
            raise KeyError(f"CMM memory '{memory_id}' not found")

        existing = self._store[memory_id]
        new_meta = {**existing.metadata, **(metadata or {})}
        new_content = content if content is not None else existing.content
        now = datetime.now().strftime("%Y-%m-%d")

        updated = MemoryEntry(
            id=memory_id,
            content=new_content,
            metadata=new_meta,
            created_at=existing.created_at,
            updated_at=now,
            version=existing.version + 1,
        )
        self._store[memory_id] = updated
        return updated

    # ── delete ────────────────────────────────────────────────────────────────

    def delete(self, memory_id: str) -> bool:
        """Remove memory from mock store.

        Note: Unlike LocalMemoryAdapter, CMM backend does a hard delete.
        The versioned audit trail is maintained by CMM's own infrastructure.

        TODO(cmm-ga):
            self._client.beta.memory.delete(
                store_id=self._store_id, memory_id=memory_id
            )
            return True
        """
        if memory_id not in self._store:
            return False
        del self._store[memory_id]
        return True

    # ── internal helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _matches_filter(entry: MemoryEntry, filter: dict[str, Any]) -> bool:
        for k, v in filter.items():
            actual = entry.metadata.get(k)
            if isinstance(actual, list):
                if v not in actual:
                    return False
            elif actual != v:
                return False
        return True

    # TODO(cmm-ga): add _to_entry() to convert CMM API response → MemoryEntry
    # @staticmethod
    # def _to_entry(api_result) -> MemoryEntry:
    #     return MemoryEntry(
    #         id=api_result.id,
    #         content=api_result.content,
    #         metadata=api_result.metadata or {},
    #         created_at=api_result.created_at.isoformat(),
    #         updated_at=api_result.updated_at.isoformat(),
    #         version=api_result.version,
    #     )

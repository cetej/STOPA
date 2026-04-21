"""local_memory_adapter.py — File-based MemoryBackend for STOPA learnings.

Backed by .claude/memory/learnings/*.md with YAML frontmatter.
search() delegates to scripts/hybrid-retrieve.py logic via direct import.
delete() archives to .claude/memory/learnings-archive.md (core-invariant #5).

Windows path safety: all paths use pathlib.Path throughout.
UTF-8 everywhere with errors='replace' on read.
"""
from __future__ import annotations

import re
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Any

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from memory_backend import MemoryBackend, MemoryEntry, SearchResult

# ── Paths ────────────────────────────────────────────────────────────────────

_HERE = Path(__file__).resolve().parent
STOPA_ROOT = _HERE.parent.parent  # .claude/lib → .claude → STOPA
LEARNINGS_DIR = STOPA_ROOT / ".claude" / "memory" / "learnings"
ARCHIVE_FILE = STOPA_ROOT / ".claude" / "memory" / "learnings-archive.md"
SCRIPTS_DIR = STOPA_ROOT / "scripts"

# Filenames to skip when scanning learnings dir
_SKIP = frozenset({"critical-patterns.md", "learnings-archive.md",
                   "block-manifest.json", ".gitkeep"})


# ── YAML frontmatter helpers ─────────────────────────────────────────────────

_FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split YAML frontmatter from body. Returns (metadata_dict, body_str).

    Uses a lightweight regex parser — avoids pyyaml dependency.
    Only parses scalar strings, ints, floats, and inline lists.
    """
    m = _FM_RE.match(text)
    if not m:
        return {}, text

    raw = m.group(1)
    body = text[m.end():]
    meta: dict[str, Any] = {}

    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if not key:
            continue

        # inline list: [a, b, c]
        if val.startswith("[") and val.endswith("]"):
            items = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
            meta[key] = items
            continue

        # strip quotes
        val = val.strip("\"'")

        # numeric coercion
        try:
            if "." in val:
                meta[key] = float(val)
            else:
                meta[key] = int(val)
            continue
        except ValueError:
            pass

        meta[key] = val if val else None

    return meta, body


def _render_frontmatter(meta: dict[str, Any]) -> str:
    """Render metadata dict back to YAML frontmatter string."""
    lines = ["---"]
    for k, v in meta.items():
        if v is None:
            continue
        if isinstance(v, list):
            lines.append(f"{k}: [{', '.join(str(i) for i in v)}]")
        elif isinstance(v, bool):
            lines.append(f"{k}: {str(v).lower()}")
        elif isinstance(v, (int, float)):
            lines.append(f"{k}: {v}")
        else:
            # Quote strings that contain special chars
            sv = str(v)
            if any(c in sv for c in ':"{}[]|>&*!,%@`'):
                lines.append(f'{k}: "{sv}"')
            else:
                lines.append(f"{k}: {sv}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def _entry_from_file(fp: Path) -> MemoryEntry:
    """Parse a learning .md file into a MemoryEntry."""
    text = fp.read_text(encoding="utf-8", errors="replace")
    meta, body = _parse_frontmatter(text)
    stat = fp.stat()
    created_at = meta.get("date", "")
    updated_at = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d")
    # Use _version field stored in frontmatter; fall back to 1 for existing files
    version = int(meta.get("_version", 1))
    return MemoryEntry(
        id=fp.stem,  # filename without .md
        content=body.strip(),
        metadata=meta,
        created_at=str(created_at),
        updated_at=updated_at,
        version=version,
    )


def _matches_filter(entry: MemoryEntry, filter: dict[str, Any]) -> bool:
    """Return True if entry metadata contains ALL key-value pairs in filter."""
    for k, v in filter.items():
        actual = entry.metadata.get(k)
        if isinstance(actual, list):
            # Filter value must appear in list
            if v not in actual:
                return False
        elif actual != v:
            return False
    return True


# ── Hybrid search bridge ─────────────────────────────────────────────────────

def _import_hybrid_search():
    """Import hybrid-retrieve.py functions. Returns (grep_search, bm25_search,
    graph_search, fuse_rrf, load_superseded_set) or None on failure."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "hybrid_retrieve",
            str(SCRIPTS_DIR / "hybrid-retrieve.py"),
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception as e:
        print(f"[WARN] hybrid-retrieve.py not importable: {e}", file=sys.stderr)
        return None


# ── Adapter class ────────────────────────────────────────────────────────────


class LocalMemoryAdapter(MemoryBackend):
    """File-based MemoryBackend backed by .claude/memory/learnings/*.md.

    Thread-safety: single-writer assumed (same as existing hook architecture).
    No file locking beyond what the OS provides — Windows antivirus retry
    is handled at write time only.
    """

    def __init__(self, learnings_dir: Path | None = None) -> None:
        """Initialize adapter.

        Args:
            learnings_dir: Override the default learnings directory.
                           Used by tests for temp-dir isolation.
        """
        self._dir = learnings_dir or LEARNINGS_DIR
        self._dir.mkdir(parents=True, exist_ok=True)

    # ── list ─────────────────────────────────────────────────────────────────

    def list(self, filter: dict[str, Any] | None = None) -> list[MemoryEntry]:
        """List all learning files, optionally filtered by metadata fields."""
        entries: list[MemoryEntry] = []
        for fp in sorted(self._dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True):
            if fp.name in _SKIP or fp.name.startswith("index-"):
                continue
            try:
                entry = _entry_from_file(fp)
            except OSError:
                continue
            if filter and not _matches_filter(entry, filter):
                continue
            entries.append(entry)
        return entries

    # ── search ────────────────────────────────────────────────────────────────

    def search(
        self,
        query: str,
        k: int = 8,
        task_tier: str = "standard",
    ) -> list[SearchResult]:
        """Hybrid search: delegates to hybrid-retrieve.py grep+BM25+graph+RRF.

        Falls back to grep-only if hybrid-retrieve.py is not importable.
        """
        mod = _import_hybrid_search()

        if mod is not None:
            try:
                return self._hybrid_search(mod, query, k, task_tier)
            except Exception as e:
                print(f"[WARN] hybrid search failed, falling back to grep: {e}", file=sys.stderr)

        return self._grep_search(query, k)

    def _hybrid_search(self, mod, query: str, k: int, task_tier: str) -> list[SearchResult]:
        """Use hybrid-retrieve.py signals and fuse results."""
        # Override LEARNINGS_DIR if we're using a custom dir (tests)
        orig_dir = getattr(mod, "LEARNINGS_DIR", None)
        if self._dir != LEARNINGS_DIR and orig_dir is not None:
            mod.LEARNINGS_DIR = self._dir

        try:
            grep_hits = mod.grep_search(query, max_results=15)
            bm25_hits = mod.bm25_search(query, max_results=15)
            graph_hits = mod.graph_search(grep_hits, max_results=10) if grep_hits else []
            superseded = mod.load_superseded_set()
            ranked = mod.fuse_rrf(grep_hits, bm25_hits, graph_hits, superseded, top_n=k)
        finally:
            if self._dir != LEARNINGS_DIR and orig_dir is not None:
                mod.LEARNINGS_DIR = orig_dir

        results: list[SearchResult] = []
        for rf in ranked:
            # Skip virtual MemPalace entries (mp: prefix)
            if rf.filename.startswith("mp:"):
                continue
            fp = self._dir / rf.filename
            if not fp.exists():
                continue
            try:
                entry = _entry_from_file(fp)
            except OSError:
                continue
            results.append(SearchResult(
                entry=entry,
                score=rf.rrf_score,
                sources=list(rf.sources),
            ))
        return results[:k]

    def _grep_search(self, query: str, k: int) -> list[SearchResult]:
        """Simple grep fallback: scan frontmatter for query terms."""
        terms = [t.lower() for t in re.findall(r"[a-zA-Z0-9_-]{3,}", query)]
        if not terms:
            return []

        scored: list[tuple[float, Path]] = []
        for fp in self._dir.glob("*.md"):
            if fp.name in _SKIP:
                continue
            try:
                head = fp.read_text(encoding="utf-8", errors="replace")[:1500]
            except OSError:
                continue
            hits = sum(1 for t in terms if t in head.lower())
            if hits > 0:
                scored.append((hits / len(terms), fp))

        scored.sort(key=lambda x: -x[0])
        results: list[SearchResult] = []
        for score, fp in scored[:k]:
            try:
                entry = _entry_from_file(fp)
                results.append(SearchResult(entry=entry, score=score, sources=["grep"]))
            except OSError:
                continue
        return results

    # ── read ─────────────────────────────────────────────────────────────────

    def read(self, memory_id: str) -> MemoryEntry | None:
        """Read learning by slug (filename without .md)."""
        # Handle .md extension if provided
        slug = memory_id.removesuffix(".md")
        fp = self._dir / f"{slug}.md"
        if not fp.exists():
            return None
        try:
            return _entry_from_file(fp)
        except OSError:
            return None

    # ── write ─────────────────────────────────────────────────────────────────

    def write(
        self,
        memory_id: str,
        content: str,
        metadata: dict[str, Any],
    ) -> MemoryEntry:
        """Create a new learning file. Raises FileExistsError if slug exists."""
        slug = memory_id.removesuffix(".md")
        fp = self._dir / f"{slug}.md"
        if fp.exists():
            raise FileExistsError(f"Memory '{slug}' already exists at {fp}")

        # Ensure date field exists
        if "date" not in metadata:
            metadata = {**metadata, "date": datetime.now().strftime("%Y-%m-%d")}
        # Store version counter in frontmatter for reliable versioning
        metadata = {**metadata, "_version": 1}

        fm = _render_frontmatter(metadata)
        body = content.strip()
        text = f"{fm}\n{body}\n" if body else fm

        self._write_file(fp, text)
        return _entry_from_file(fp)

    def _write_file(self, fp: Path, text: str, retries: int = 3) -> None:
        """Write file with retry logic for Windows antivirus locking."""
        import time
        for attempt in range(retries):
            try:
                fp.write_text(text, encoding="utf-8")
                return
            except PermissionError:
                if attempt < retries - 1:
                    time.sleep(0.2)
                else:
                    raise

    # ── edit ─────────────────────────────────────────────────────────────────

    def edit(
        self,
        memory_id: str,
        content: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> MemoryEntry:
        """Update an existing learning. Preserves fields not provided."""
        slug = memory_id.removesuffix(".md")
        fp = self._dir / f"{slug}.md"
        if not fp.exists():
            raise KeyError(f"Memory '{slug}' not found at {fp}")

        existing_text = fp.read_text(encoding="utf-8", errors="replace")
        existing_meta, existing_body = _parse_frontmatter(existing_text)

        # Merge metadata and increment version counter
        new_meta = {**existing_meta, **(metadata or {})}
        new_meta["_version"] = int(existing_meta.get("_version", 1)) + 1
        new_body = content.strip() if content is not None else existing_body.strip()

        fm = _render_frontmatter(new_meta)
        text = f"{fm}\n{new_body}\n" if new_body else fm
        self._write_file(fp, text)
        return _entry_from_file(fp)

    # ── delete ────────────────────────────────────────────────────────────────

    def delete(self, memory_id: str) -> bool:
        """Archive learning to learnings-archive.md (never destroys — core-invariant #5)."""
        slug = memory_id.removesuffix(".md")
        fp = self._dir / f"{slug}.md"
        if not fp.exists():
            return False

        try:
            content = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return False

        archive = self._archive_path()
        header = f"\n\n## Archived: {slug} ({datetime.now().strftime('%Y-%m-%d')})\n\n"
        with archive.open("a", encoding="utf-8") as af:
            af.write(header)
            af.write(content)

        fp.unlink()
        return True

    def _archive_path(self) -> Path:
        """Return the archive file path. Creates it if it doesn't exist."""
        # When using a custom dir (tests), put archive alongside it
        if self._dir != LEARNINGS_DIR:
            archive = self._dir.parent / "learnings-archive.md"
        else:
            archive = ARCHIVE_FILE
        if not archive.exists():
            archive.write_text("# Learnings Archive\n\nArchived entries below.\n",
                               encoding="utf-8")
        return archive

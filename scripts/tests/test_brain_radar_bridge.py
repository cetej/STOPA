#!/usr/bin/env python3
"""Tests for brain-ingest → STOPA radar/news bridge (issue #24, G7).

Covers acceptance criteria from issue #24:
- Tool discovery: action_class=tool/library/mcp-server/cli → radar-proposals.md
- Paper routing: action_class=paper → news-proposals.md
- False positive skip: action_class=none → no proposal written
- Dedup: existing URL/name in radar.md → skipped with reason
- Audit trail: every entry has source: brain-watch
- Circuit breaker: bridge never writes to brain/* (verified by import contract)

Run: python -m pytest scripts/tests/test_brain_radar_bridge.py -v
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

# Load brain-ingest.py as a module despite hyphen in filename
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("brain_ingest", SCRIPTS_DIR / "brain-ingest.py")
brain_ingest = importlib.util.module_from_spec(spec)
sys.modules["brain_ingest"] = brain_ingest
# Add scripts/ for relative imports inside brain-ingest (lib.keyring)
sys.path.insert(0, str(SCRIPTS_DIR))
spec.loader.exec_module(brain_ingest)


@pytest.fixture
def tmp_memory(tmp_path, monkeypatch):
    """Redirect bridge file paths to a tmp dir so tests don't touch real memory."""
    radar = tmp_path / "radar.md"
    proposals = tmp_path / "radar-proposals.md"
    news_proposals = tmp_path / "news-proposals.md"
    log_file = tmp_path / "brain-ingest.log"

    monkeypatch.setattr(brain_ingest, "RADAR_FILE", radar)
    monkeypatch.setattr(brain_ingest, "RADAR_PROPOSALS", proposals)
    monkeypatch.setattr(brain_ingest, "NEWS_PROPOSALS", news_proposals)
    monkeypatch.setattr(brain_ingest, "LOG_FILE", log_file)

    return {
        "radar": radar,
        "proposals": proposals,
        "news_proposals": news_proposals,
        "log": log_file,
        "root": tmp_path,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Scenario 1: tool discovery — action_class=mcp-server lands in radar-proposals
# ─────────────────────────────────────────────────────────────────────────────

def test_tool_discovery_creates_radar_proposal(tmp_memory):
    summary = {
        "title": "context-mode — FTS5 intent-driven MCP filter",
        "key_idea": "Sandboxed BM25+Porter indexing returns only matching sections; raw output never enters context.",
        "primary_url": "https://github.com/mksglu/context-mode",
        "action_class": "mcp-server",
        "tool_name": "context-mode",
    }
    result = brain_ingest.propose_to_radar(
        action_class="mcp-server",
        tool_name="context-mode",
        url="https://github.com/mksglu/context-mode",
        summary=summary,
    )
    assert result == "proposed"

    text = tmp_memory["proposals"].read_text(encoding="utf-8")
    # Audit trail invariant
    assert "source: brain-watch" in text or "| brain-watch |" in text, "missing brain-watch source field"
    # Action class recorded
    assert "mcp-server" in text
    # Tool name + URL
    assert "context-mode" in text
    assert "https://github.com/mksglu/context-mode" in text
    # Status pending until reviewed
    assert "pending" in text


def test_library_action_class_routes_to_radar(tmp_memory):
    """Library should also go to radar (not news)."""
    result = brain_ingest.propose_to_radar(
        action_class="library",
        tool_name="hippo-memory",
        url="https://github.com/kitfunso/hippo-memory",
        summary={
            "title": "hippo-memory — biological memory for AI",
            "key_idea": "TS+SQLite library with retrieval strengthening + decay.",
        },
    )
    assert result == "proposed"
    assert tmp_memory["proposals"].exists()
    assert not tmp_memory["news_proposals"].exists(), "library must NOT land in news-proposals"


# ─────────────────────────────────────────────────────────────────────────────
# Scenario 2: paper routing — action_class=paper lands in news-proposals
# ─────────────────────────────────────────────────────────────────────────────

def test_paper_routes_to_news_proposals(tmp_memory):
    result = brain_ingest.propose_to_radar(
        action_class="paper",
        tool_name="TACO: Self-Evolving Context Compression",
        url="https://arxiv.org/abs/2604.19572",
        summary={
            "title": "TACO — Self-Evolving Context Compression",
            "key_idea": "Plug-and-play framework that auto-discovers compression rules from trajectories. 10% token reduction.",
            "primary_url": "https://arxiv.org/abs/2604.19572",
        },
    )
    assert result == "proposed"

    # Paper goes to news-proposals, NOT radar-proposals
    assert tmp_memory["news_proposals"].exists(), "paper must land in news-proposals"
    assert not tmp_memory["proposals"].exists(), "paper must NOT land in radar-proposals"

    text = tmp_memory["news_proposals"].read_text(encoding="utf-8")
    assert "TACO" in text
    assert "arxiv.org/abs/2604.19572" in text
    assert "brain-watch" in text
    assert "pending" in text


# ─────────────────────────────────────────────────────────────────────────────
# Scenario 3: false positive skip — action_class=none does nothing
# ─────────────────────────────────────────────────────────────────────────────

def test_action_class_none_writes_nothing(tmp_memory):
    """A blog post or unrelated article (action_class=none) must not pollute proposals."""
    result = brain_ingest.propose_to_radar(
        action_class="none",
        tool_name="some-mention",
        url="https://example.com/blog/post-about-llms",
        summary={"title": "Random LLM blog post", "key_idea": "Opinion piece, no tool."},
    )
    assert result == "skipped"
    assert not tmp_memory["proposals"].exists()
    assert not tmp_memory["news_proposals"].exists()


def test_empty_tool_name_skipped(tmp_memory):
    """Even with valid action_class, missing tool_name skips (defensive)."""
    result = brain_ingest.propose_to_radar(
        action_class="tool",
        tool_name="",  # extractor failed to identify name
        url="https://example.com/something",
        summary={"title": "Something", "key_idea": "Idk"},
    )
    assert result == "skipped"
    assert not tmp_memory["proposals"].exists()


def test_unknown_action_class_skipped(tmp_memory):
    """Garbage values in action_class don't accidentally promote to radar."""
    result = brain_ingest.propose_to_radar(
        action_class="rambling-prose",  # not in any whitelist
        tool_name="MysteryTool",
        url="https://example.com/x",
        summary={"title": "X", "key_idea": "Y"},
    )
    assert result == "skipped"


# ─────────────────────────────────────────────────────────────────────────────
# Scenario 4: dedup — existing tool/URL in radar.md is skipped
# ─────────────────────────────────────────────────────────────────────────────

def test_dedup_against_existing_radar_url(tmp_memory):
    tmp_memory["radar"].write_text(
        "# Radar\n\n"
        "| Tool | Score |\n|------|-------|\n"
        "| [context-mode](https://github.com/mksglu/context-mode) | 9 |\n",
        encoding="utf-8",
    )
    result = brain_ingest.propose_to_radar(
        action_class="mcp-server",
        tool_name="context-mode",
        url="https://github.com/mksglu/context-mode",
        summary={"title": "context-mode", "key_idea": "Already known.", "primary_url": "https://github.com/mksglu/context-mode"},
    )
    assert result == "deduplicated"
    assert not tmp_memory["proposals"].exists(), "dedup must not create proposals file"


def test_dedup_against_canonical_url_variant(tmp_memory):
    """www. prefix and trailing slash should still be detected as the same URL."""
    tmp_memory["radar"].write_text(
        "# Radar\n| Tool | URL |\n|---|---|\n"
        "| Foo | https://github.com/owner/repo |\n",
        encoding="utf-8",
    )
    # Different surface form, same canonical URL
    result = brain_ingest.propose_to_radar(
        action_class="tool",
        tool_name="foo-tool",
        url="https://www.github.com/owner/repo/",
        summary={
            "title": "Foo",
            "key_idea": "...",
            "primary_url": "https://www.github.com/owner/repo/",
        },
    )
    assert result == "deduplicated"


def test_dedup_against_existing_proposal_name(tmp_memory):
    """Even if URL differs, if name already proposed, skip."""
    # Manually pre-seed a proposal
    tmp_memory["proposals"].write_text(
        brain_ingest.PROPOSAL_HEADER
        + "| 2026-04-25 | [hyperframes](https://example.com/old) | tool | https://example.com/old | brain-watch | ... | pending |\n",
        encoding="utf-8",
    )
    result = brain_ingest.propose_to_radar(
        action_class="tool",
        tool_name="hyperframes",
        url="https://different-mirror.example.com/heygen-hyperframes",
        summary={"title": "Hyperframes", "key_idea": "Already proposed under different URL."},
    )
    assert result == "deduplicated"


# ─────────────────────────────────────────────────────────────────────────────
# Helpers: canonicalize_url + is_already_known semantics
# ─────────────────────────────────────────────────────────────────────────────

def test_canonicalize_url_strips_trailing_slash_and_www():
    canon = brain_ingest.canonicalize_url
    assert canon("https://www.github.com/foo/bar/") == "https://github.com/foo/bar"
    assert canon("HTTPS://GitHub.com/Foo/Bar") == "https://github.com/Foo/Bar"
    assert canon("https://example.com/path#fragment") == "https://example.com/path"


def test_is_already_known_short_name_does_not_falsely_match(tmp_memory):
    """Generic 3-char names like 'cli' must not trigger spurious matches."""
    tmp_memory["radar"].write_text(
        "# Radar\n\nThis text has the word cli somewhere but no tool named cli.\n",
        encoding="utf-8",
    )
    known, _ = brain_ingest.is_already_known("cli", "https://nowhere.example/x")
    assert known is False


# ─────────────────────────────────────────────────────────────────────────────
# Circuit breaker: bridge MUST NOT write to brain/* paths
# ─────────────────────────────────────────────────────────────────────────────

def test_bridge_never_writes_to_brain_paths(tmp_memory, monkeypatch):
    """The bridge code path must only write to RADAR_PROPOSALS / NEWS_PROPOSALS / LOG_FILE.

    This guards against accidental recursion: if propose_to_radar ever wrote to
    brain/inbox.md, the next brain-ingest run could re-process the entry.
    """
    writes: list[str] = []
    real_write = Path.write_text

    def tracking_write(self, *args, **kwargs):
        writes.append(str(self))
        return real_write(self, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", tracking_write)

    brain_ingest.propose_to_radar(
        action_class="tool",
        tool_name="watcher-test",
        url="https://example.com/watcher",
        summary={"title": "Watcher", "key_idea": "Testing recursion guard."},
    )

    for path in writes:
        assert "brain" not in Path(path).as_posix().lower().split("/"), (
            f"Bridge wrote to a brain/* path — recursion risk: {path}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Idempotency under exception: bridge errors must not break ingest
# ─────────────────────────────────────────────────────────────────────────────

def test_bridge_exception_returns_skipped(tmp_memory, monkeypatch):
    """If a write fails partway, propose_to_radar swallows the exception."""

    def raising_write(self, *args, **kwargs):
        raise OSError("simulated disk failure")

    monkeypatch.setattr(Path, "write_text", raising_write)
    result = brain_ingest.propose_to_radar(
        action_class="tool",
        tool_name="will-fail",
        url="https://example.com/x",
        summary={"title": "X", "key_idea": "Y"},
    )
    assert result in {"skipped", "deduplicated"}, "bridge must not propagate exceptions"

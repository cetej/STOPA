"""Screening-based learning embedder for STOPA memory retrieval.

Loads pretrained LearningEmbedder + RetrievalScreener from checkpoint,
provides simple API for scoring queries against learnings.

Usage:
    from lib.learning_embedder import ScreeningScorer

    scorer = ScreeningScorer.load()
    if scorer:
        results = scorer.score_keywords(["validation", "skill"], max_results=5)
"""

import json
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

# Paths
STOPA_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CHECKPOINT_DIR = STOPA_ROOT / "experiments" / "multiscreen" / "checkpoints"
MODEL_PATH = CHECKPOINT_DIR / "retrieval_screener.pt"
VOCAB_PATH = CHECKPOINT_DIR / "screening-vocab.json"
LEARNINGS_DIR = STOPA_ROOT / ".claude" / "memory" / "learnings"
EMBEDDINGS_CACHE = STOPA_ROOT / ".claude" / "memory" / "intermediate" / "learning-embeddings.pt"

STOPWORDS = {
    "the", "and", "for", "this", "that", "with", "from", "are", "was",
    "has", "have", "had", "not", "but", "can", "will", "use", "using",
    "when", "all", "pro", "při", "aby", "jako", "nebo", "ale", "pod",
}


def tokenize(text: str) -> list[str]:
    text = text.lower()
    text = re.sub(r"[^a-z0-9áčďéěíňóřšťúůýž_-]", " ", text)
    return [t for t in text.split() if len(t) > 2]


def parse_tags(tags_str: str) -> list[str]:
    tags_str = tags_str.strip("[] ")
    return [t.strip().strip("\"'") for t in tags_str.split(",") if t.strip()]


def parse_yaml_frontmatter(content: str) -> dict:
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    result = {}
    for line in content[3:end].strip().split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip().strip("\"'")
    return result


if HAS_TORCH:
    # Import model classes (must match training code)
    sys.path.insert(0, str(STOPA_ROOT / "experiments"))
    from multiscreen.retrieval import RetrievalScreener

    class LearningEmbedder(nn.Module):
        """Weighted bag-of-words embedder (must match train_retrieval.py)."""

        def __init__(self, vocab_size: int, d_embed: int = 128):
            super().__init__()
            self.d_embed = d_embed
            self.token_embedding = nn.Embedding(vocab_size, d_embed, padding_idx=0)
            self.field_weights = nn.Parameter(torch.tensor([3.0, 2.0, 2.0, 1.0]))

        def _tokens_to_ids(self, tokens: list[str], vocab: dict[str, int]) -> torch.Tensor:
            ids = [vocab.get(t, 1) for t in tokens]
            if not ids:
                ids = [0]
            return torch.tensor(ids, dtype=torch.long)

        def embed_field(self, tokens: list[str], vocab: dict[str, int], weight_idx: int) -> torch.Tensor:
            ids = self._tokens_to_ids(tokens, vocab)
            embeds = self.token_embedding(ids)
            pooled = embeds.mean(dim=0)
            return pooled * self.field_weights[weight_idx]

        def embed_learning(self, meta: dict, body: str, vocab: dict[str, int]) -> torch.Tensor:
            tags_tokens = []
            for tag in parse_tags(meta.get("tags", "")):
                tags_tokens.extend(tokenize(tag))
            component_tokens = tokenize(meta.get("component", ""))
            summary_tokens = [t for t in tokenize(meta.get("summary", "")) if t not in STOPWORDS]
            body_tokens = [t for t in tokenize(body)[:100] if t not in STOPWORDS]

            e = (
                self.embed_field(tags_tokens, vocab, 0)
                + self.embed_field(component_tokens, vocab, 1)
                + self.embed_field(summary_tokens, vocab, 2)
                + self.embed_field(body_tokens, vocab, 3)
            )
            return F.normalize(e, dim=0)

        def embed_query(self, keywords: list[str], vocab: dict[str, int]) -> torch.Tensor:
            tokens = []
            for kw in keywords:
                tokens.extend(tokenize(kw))
            ids = self._tokens_to_ids(tokens, vocab)
            embeds = self.token_embedding(ids)
            pooled = embeds.mean(dim=0)
            return F.normalize(pooled, dim=0)


class ScreeningScorer:
    """High-level API for screening-based learning retrieval."""

    def __init__(self, embedder, screener, vocab, learnings_data):
        self.embedder = embedder
        self.screener = screener
        self.vocab = vocab
        self.learnings_data = learnings_data  # list of (filename, meta, body)
        self._embeddings_cache = None
        self._cache_mtime = None

    @classmethod
    def load(cls, timeout_ms: float = 500) -> "ScreeningScorer | None":
        """Load pretrained model. Returns None if unavailable or too slow."""
        if not HAS_TORCH:
            return None
        if not MODEL_PATH.exists():
            return None

        start = time.perf_counter()
        try:
            state = torch.load(MODEL_PATH, weights_only=False, map_location="cpu")
            vocab = state["vocab"]

            embedder = LearningEmbedder(len(vocab), state["d_embed"])
            screener = RetrievalScreener(state["d_embed"], state["d_k"], state["n_tiles"])
            embedder.load_state_dict(state["embedder"])
            screener.load_state_dict(state["screener"])
            embedder.eval()
            screener.eval()

            # Load learnings
            learnings_data = []
            for f in sorted(LEARNINGS_DIR.glob("*.md"), reverse=True):
                if f.name in ("critical-patterns.md", "index-general.md",
                              "block-manifest.json", "ecosystem-scan.md"):
                    continue
                try:
                    content = f.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                meta = parse_yaml_frontmatter(content)
                body_start = content.find("---", 3)
                body = content[body_start + 3:].strip() if body_start != -1 else ""
                learnings_data.append((f.name, meta, body))

            elapsed_ms = (time.perf_counter() - start) * 1000
            if elapsed_ms > timeout_ms:
                return None  # too slow for hook context

            return cls(embedder, screener, vocab, learnings_data)

        except Exception:
            return None

    def _get_embeddings(self) -> "torch.Tensor":
        """Get learning embeddings with caching."""
        # Check cache freshness
        try:
            current_mtime = max(
                f.stat().st_mtime for f in LEARNINGS_DIR.glob("*.md")
            )
        except (ValueError, OSError):
            current_mtime = 0

        if self._embeddings_cache is not None and self._cache_mtime == current_mtime:
            return self._embeddings_cache

        with torch.no_grad():
            embeds = torch.stack([
                self.embedder.embed_learning(meta, body, self.vocab)
                for _, meta, body in self.learnings_data
            ])

        self._embeddings_cache = embeds
        self._cache_mtime = current_mtime
        return embeds

    def score_keywords(
        self, keywords: list[str], max_results: int = 5
    ) -> list[dict]:
        """Score keywords against all learnings.

        Returns list of {filename, score, meta} sorted by score descending.
        Only non-zero scores included.
        """
        if not self.learnings_data:
            return []

        all_embeds = self._get_embeddings()

        with torch.no_grad():
            q_emb = self.embedder.embed_query(keywords, self.vocab).unsqueeze(0)
            scores = self.screener(q_emb, all_embeds)  # (1, N)

        results = []
        for i, (filename, meta, body) in enumerate(self.learnings_data):
            s = scores[0, i].item()
            if s > 0.0:
                results.append({
                    "filename": filename,
                    "score": round(s, 4),
                    "meta": meta,
                    "body": body[:500],
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:max_results]

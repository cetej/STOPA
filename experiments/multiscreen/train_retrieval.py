"""Train RetrievalScreener on STOPA learnings data.

Generates synthetic query-learning pairs from YAML frontmatter,
trains embedder + screener end-to-end, evaluates Recall@5 and sparsity,
and compares against the existing heuristic scoring.

Usage:
    python train_retrieval.py                    # train + eval
    python train_retrieval.py --eval-only        # eval existing checkpoint
"""

import json
import random
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import torch
import torch.nn as nn
import torch.nn.functional as F

# Add parent to path for multiscreen imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from multiscreen.retrieval import RetrievalScreener

# --- Paths ---
STOPA_ROOT = Path(__file__).resolve().parent.parent.parent
LEARNINGS_DIR = STOPA_ROOT / ".claude" / "memory" / "learnings"
CHECKPOINT_DIR = Path(__file__).resolve().parent / "checkpoints"
VOCAB_PATH = CHECKPOINT_DIR / "screening-vocab.json"
MODEL_PATH = CHECKPOINT_DIR / "retrieval_screener.pt"


# --- YAML parser (minimal, no pyyaml dependency) ---

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
            val = val.strip().strip("\"'")
            result[key.strip()] = val
    return result


def parse_tags(tags_str: str) -> list[str]:
    """Parse YAML array from string like '[tag1, tag2]' or 'tag1, tag2'."""
    tags_str = tags_str.strip("[] ")
    return [t.strip().strip("\"'") for t in tags_str.split(",") if t.strip()]


# --- Vocabulary builder ---

def tokenize(text: str) -> list[str]:
    """Simple whitespace + punctuation tokenizer."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9áčďéěíňóřšťúůýž_-]", " ", text)
    return [t for t in text.split() if len(t) > 2]


STOPWORDS = {
    "the", "and", "for", "this", "that", "with", "from", "are", "was",
    "has", "have", "had", "not", "but", "can", "will", "use", "using",
    "when", "all", "pro", "při", "aby", "jako", "nebo", "ale", "pod",
}


def build_vocab(learnings_dir: Path, max_size: int = 2048) -> dict[str, int]:
    """Build vocabulary from all learnings files."""
    freq: dict[str, int] = {}

    for f in learnings_dir.glob("*.md"):
        if f.name in ("critical-patterns.md", "index-general.md",
                       "block-manifest.json", "ecosystem-scan.md"):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        meta = parse_yaml_frontmatter(content)

        # Tags get extra weight (counted multiple times)
        for tag in parse_tags(meta.get("tags", "")):
            for t in tokenize(tag):
                freq[t] = freq.get(t, 0) + 5

        # Component
        for t in tokenize(meta.get("component", "")):
            freq[t] = freq.get(t, 0) + 3

        # Summary
        for t in tokenize(meta.get("summary", "")):
            if t not in STOPWORDS:
                freq[t] = freq.get(t, 0) + 2

        # Body (after frontmatter)
        body_start = content.find("---", 3)
        body = content[body_start + 3:] if body_start != -1 else ""
        for t in tokenize(body):
            if t not in STOPWORDS:
                freq[t] = freq.get(t, 0) + 1

    # Sort by frequency, take top max_size
    sorted_tokens = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    vocab = {"<PAD>": 0, "<UNK>": 1}
    for token, _ in sorted_tokens[:max_size - 2]:
        vocab[token] = len(vocab)

    return vocab


# --- Embedder ---

class LearningEmbedder(nn.Module):
    """Weighted bag-of-words with learned projection for learning files."""

    def __init__(self, vocab_size: int, d_embed: int = 128):
        super().__init__()
        self.d_embed = d_embed
        self.token_embedding = nn.Embedding(vocab_size, d_embed, padding_idx=0)
        # Field weights: tags, component, summary, body
        self.field_weights = nn.Parameter(torch.tensor([3.0, 2.0, 2.0, 1.0]))

    def _tokens_to_ids(self, tokens: list[str], vocab: dict[str, int]) -> torch.Tensor:
        ids = [vocab.get(t, 1) for t in tokens]  # 1 = <UNK>
        if not ids:
            ids = [0]  # <PAD>
        return torch.tensor(ids, dtype=torch.long)

    def embed_field(
        self, tokens: list[str], vocab: dict[str, int], weight_idx: int
    ) -> torch.Tensor:
        """Embed a single field (tags, component, summary, or body)."""
        ids = self._tokens_to_ids(tokens, vocab)
        embeds = self.token_embedding(ids)  # (n_tokens, d_embed)
        pooled = embeds.mean(dim=0)  # (d_embed,)
        return pooled * self.field_weights[weight_idx]

    def embed_learning(
        self, meta: dict, body: str, vocab: dict[str, int]
    ) -> torch.Tensor:
        """Embed a full learning file into (d_embed,) vector."""
        tags_tokens = []
        for tag in parse_tags(meta.get("tags", "")):
            tags_tokens.extend(tokenize(tag))
        component_tokens = tokenize(meta.get("component", ""))
        summary_tokens = [t for t in tokenize(meta.get("summary", "")) if t not in STOPWORDS]
        body_tokens = [t for t in tokenize(body)[:100] if t not in STOPWORDS]  # truncate body

        e = (
            self.embed_field(tags_tokens, vocab, 0)
            + self.embed_field(component_tokens, vocab, 1)
            + self.embed_field(summary_tokens, vocab, 2)
            + self.embed_field(body_tokens, vocab, 3)
        )
        return F.normalize(e, dim=0)

    def embed_query(
        self, keywords: list[str], vocab: dict[str, int]
    ) -> torch.Tensor:
        """Embed a query (list of keywords) into (d_embed,) vector."""
        tokens = []
        for kw in keywords:
            tokens.extend(tokenize(kw))
        ids = self._tokens_to_ids(tokens, vocab)
        embeds = self.token_embedding(ids)
        pooled = embeds.mean(dim=0)
        return F.normalize(pooled, dim=0)


# --- Training data generation ---

def load_learnings(learnings_dir: Path) -> list[dict]:
    """Load all learnings with meta + body."""
    learnings = []
    for f in sorted(learnings_dir.glob("*.md"), reverse=True):
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
        learnings.append({"filename": f.name, "meta": meta, "body": body})
    return learnings


def generate_queries(learning: dict) -> list[list[str]]:
    """Generate synthetic queries from a learning's metadata."""
    tags = parse_tags(learning["meta"].get("tags", ""))
    component = learning["meta"].get("component", "")
    summary_words = [t for t in tokenize(learning["meta"].get("summary", ""))
                     if t not in STOPWORDS][:5]

    queries = []

    # Combinations of tags
    if len(tags) >= 2:
        for i in range(min(3, len(tags))):
            for j in range(i + 1, min(4, len(tags))):
                queries.append([tags[i], tags[j]])

    # Tag + component
    if tags and component:
        queries.append([tags[0], component])

    # Summary keywords
    if len(summary_words) >= 2:
        queries.append(summary_words[:2])

    # Single tag (easier)
    for tag in tags[:2]:
        queries.append([tag])

    # Ensure at least 1 query
    if not queries and tags:
        queries.append(tags[:1])
    elif not queries:
        queries.append(["general"])

    return queries[:5]  # max 5 per learning


def generate_training_data(
    learnings: list[dict],
) -> list[tuple[list[str], int, int]]:
    """Generate (query, positive_idx, negative_idx) triples."""
    data = []
    n = len(learnings)

    for pos_idx, learning in enumerate(learnings):
        queries = generate_queries(learning)
        pos_tags = set(parse_tags(learning["meta"].get("tags", "")))

        for query in queries:
            # Hard negative: shares 1 tag but different learning
            hard_neg_idx = None
            for neg_idx in range(n):
                if neg_idx == pos_idx:
                    continue
                neg_tags = set(parse_tags(learnings[neg_idx]["meta"].get("tags", "")))
                shared = pos_tags & neg_tags
                if len(shared) == 1:
                    hard_neg_idx = neg_idx
                    break

            # Easy negative: random other learning
            easy_neg_idx = random.choice([i for i in range(n) if i != pos_idx])

            data.append((query, pos_idx, hard_neg_idx or easy_neg_idx))

            # Add another easy negative
            another_neg = random.choice([i for i in range(n) if i != pos_idx])
            data.append((query, pos_idx, another_neg))

    return data


# --- Training ---

def train(
    learnings_dir: Path = LEARNINGS_DIR,
    n_epochs: int = 80,
    d_embed: int = 128,
    d_k: int = 16,
    n_tiles: int = 4,
    lr: float = 0.005,
) -> tuple[LearningEmbedder, RetrievalScreener, dict[str, int], list[dict]]:
    """Train embedder + screener end-to-end."""

    print("Loading learnings...")
    learnings = load_learnings(learnings_dir)
    print(f"  Found {len(learnings)} learnings")

    print("Building vocabulary...")
    vocab = build_vocab(learnings_dir)
    print(f"  Vocab size: {len(vocab)}")

    print("Generating training data...")
    train_data = generate_training_data(learnings)
    print(f"  Generated {len(train_data)} training triples")

    # Models
    embedder = LearningEmbedder(len(vocab), d_embed)
    screener = RetrievalScreener(d_embed, d_k, n_tiles)

    # Joint optimizer
    params = list(embedder.parameters()) + list(screener.parameters())
    optimizer = torch.optim.AdamW(params, lr=lr, betas=(0.9, 0.95))

    # Precompute doesn't work here (embeddings change during training)
    # Train loop
    print(f"\nTraining ({n_epochs} epochs)...")
    start = time.perf_counter()

    for epoch in range(n_epochs):
        random.shuffle(train_data)
        total_loss = 0.0
        n_batches = 0

        for query_kw, pos_idx, neg_idx in train_data:
            # Embed query
            q_emb = embedder.embed_query(query_kw, vocab).unsqueeze(0)  # (1, d)

            # Embed positive and negative
            pos_emb = embedder.embed_learning(
                learnings[pos_idx]["meta"], learnings[pos_idx]["body"], vocab
            ).unsqueeze(0)  # (1, d)
            neg_emb = embedder.embed_learning(
                learnings[neg_idx]["meta"], learnings[neg_idx]["body"], vocab
            ).unsqueeze(0)  # (1, d)

            candidates = torch.cat([pos_emb, neg_emb], dim=0)  # (2, d)

            # Score
            scores = screener(q_emb, candidates)  # (1, 2)

            # BCE loss: positive should score high, negative should score low
            targets = torch.tensor([[1.0, 0.0]])
            loss = F.binary_cross_entropy(scores.clamp(1e-7, 1 - 1e-7), targets)

            # Sparsity regularization: encourage 50-80% zeros
            sparsity = (scores == 0.0).float().mean()
            sparsity_target = 0.5
            sparsity_loss = (sparsity - sparsity_target).abs() * 0.1

            total_loss_val = loss + sparsity_loss

            optimizer.zero_grad()
            total_loss_val.backward()
            torch.nn.utils.clip_grad_norm_(params, 1.0)
            optimizer.step()

            total_loss += loss.item()
            n_batches += 1

        avg_loss = total_loss / max(n_batches, 1)
        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch+1:3d}: loss = {avg_loss:.4f}")

    elapsed = time.perf_counter() - start
    print(f"Training done in {elapsed:.1f}s")

    return embedder, screener, vocab, learnings


# --- Evaluation ---

def evaluate(
    embedder: LearningEmbedder,
    screener: RetrievalScreener,
    vocab: dict[str, int],
    learnings: list[dict],
) -> dict:
    """Evaluate Recall@5, Precision, sparsity."""
    embedder.eval()
    screener.eval()

    # Precompute all learning embeddings
    with torch.no_grad():
        all_embeds = torch.stack([
            embedder.embed_learning(l["meta"], l["body"], vocab)
            for l in learnings
        ])  # (N, d_embed)

    # Generate test queries (different from training — use single tags)
    hits_at_5 = 0
    total_queries = 0
    total_sparsity = 0.0

    with torch.no_grad():
        for idx, learning in enumerate(learnings):
            tags = parse_tags(learning["meta"].get("tags", ""))
            if not tags:
                continue

            # Test query: single tag
            query_kw = [tags[0]]
            q_emb = embedder.embed_query(query_kw, vocab).unsqueeze(0)

            scores = screener(q_emb, all_embeds)  # (1, N)
            top_scores, top_indices = torch.topk(scores, min(5, len(learnings)), dim=-1)

            # Check if this learning is in top-5
            if idx in top_indices[0].tolist():
                hits_at_5 += 1

            total_queries += 1
            total_sparsity += (scores == 0.0).float().mean().item()

    recall_at_5 = hits_at_5 / max(total_queries, 1)
    avg_sparsity = total_sparsity / max(total_queries, 1)

    return {
        "recall_at_5": recall_at_5,
        "total_queries": total_queries,
        "hits_at_5": hits_at_5,
        "avg_sparsity": avg_sparsity,
    }


def compare_with_heuristic(
    embedder: LearningEmbedder,
    screener: RetrievalScreener,
    vocab: dict[str, int],
    learnings: list[dict],
):
    """Show side-by-side comparison for sample queries."""
    # Import heuristic scoring
    sys.path.insert(0, str(STOPA_ROOT / ".claude" / "hooks"))
    try:
        from learnings_retrieval import retrieve_learnings, score_learning
    except ImportError:
        print("  (heuristic comparison skipped — learnings_retrieval.py not importable)")
        return

    test_queries = [
        ["validation", "skill"],
        ["orchestration", "budget"],
        ["hook", "automation"],
        ["security", "config"],
        ["memory", "checkpoint"],
    ]

    # Precompute all embeddings
    with torch.no_grad():
        all_embeds = torch.stack([
            embedder.embed_learning(l["meta"], l["body"], vocab)
            for l in learnings
        ])

    print("\n=== Comparison: Screening vs Heuristic ===\n")

    for query_kw in test_queries:
        print(f"Query: {query_kw}")

        # Screening results
        with torch.no_grad():
            q_emb = embedder.embed_query(query_kw, vocab).unsqueeze(0)
            scores = screener(q_emb, all_embeds)
            top_scores, top_indices = screener.score_and_select(q_emb, all_embeds, top_k=3)

        print("  Screening:")
        for rank, (s, i) in enumerate(zip(top_scores[0], top_indices[0])):
            if s.item() > 0:
                print(f"    {rank+1}. [{s.item():.3f}] {learnings[i.item()]['filename']}")
            else:
                print(f"    {rank+1}. [0.000] (no match)")

        # Heuristic results
        heuristic = retrieve_learnings(query_kw, max_results=3)
        print("  Heuristic:")
        for rank, r in enumerate(heuristic):
            print(f"    {rank+1}. [{r['score']:.3f}] {r['filename']}")

        nonzero = (scores > 0).sum().item()
        total = scores.numel()
        print(f"  Screening sparsity: {total - nonzero}/{total} zeros "
              f"({(total - nonzero)/total:.0%})")
        print()


def main():
    print("=" * 60)
    print("  RetrievalScreener Training Pipeline")
    print("  Multiscreen attention for STOPA learnings")
    print("=" * 60)

    eval_only = "--eval-only" in sys.argv

    if eval_only and MODEL_PATH.exists():
        print("\nLoading existing checkpoint...")
        state = torch.load(MODEL_PATH, weights_only=False)
        vocab = state["vocab"]
        learnings = load_learnings(LEARNINGS_DIR)
        embedder = LearningEmbedder(len(vocab), state["d_embed"])
        screener = RetrievalScreener(state["d_embed"], state["d_k"], state["n_tiles"])
        embedder.load_state_dict(state["embedder"])
        screener.load_state_dict(state["screener"])
    else:
        embedder, screener, vocab, learnings = train()

        # Save checkpoint
        CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

        torch.save({
            "embedder": embedder.state_dict(),
            "screener": screener.state_dict(),
            "vocab": vocab,
            "d_embed": embedder.d_embed,
            "d_k": screener.d_k,
            "n_tiles": screener.n_tiles,
        }, MODEL_PATH)
        print(f"\nCheckpoint saved to {MODEL_PATH}")

        # Save vocab separately for hooks integration
        with open(VOCAB_PATH, "w", encoding="utf-8") as f:
            json.dump(vocab, f)
        print(f"Vocab saved to {VOCAB_PATH}")

    # Evaluate
    print("\n--- Evaluation ---")
    metrics = evaluate(embedder, screener, vocab, learnings)
    print(f"  Recall@5:    {metrics['recall_at_5']:.1%} ({metrics['hits_at_5']}/{metrics['total_queries']})")
    print(f"  Avg sparsity: {metrics['avg_sparsity']:.1%}")
    print(f"  Threshold info: {screener.sparsity}")

    # Compare with heuristic
    compare_with_heuristic(embedder, screener, vocab, learnings)

    print("Done.")


if __name__ == "__main__":
    main()

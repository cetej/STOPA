"""In-memory vector store using FAISS.

Why FAISS?
- Facebook AI Similarity Search — industry standard for vector search
- Extremely fast: millions of vectors searched in milliseconds
- Works on CPU (no GPU needed for search)
- Simple API: add vectors, search by vector, done

For this learning implementation we use IndexFlatIP (brute-force inner product).
This is exact search — perfect for small datasets (<1M vectors).
For larger datasets, you'd use IVF or HNSW indexes for approximate search.

In production RAG systems, you'd use:
- Pinecone, Weaviate, Qdrant (managed vector DBs)
- pgvector (PostgreSQL extension)
- ChromaDB (lightweight, Python-native)

We implement from scratch with FAISS to understand the mechanics.
"""

import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

from .chunker import Chunk
from .embeddings import EmbeddingModel


class VectorStore:
    """FAISS-based vector store for RAG retrieval.

    Stores document chunks alongside their vector embeddings.
    Supports add, search, save, and load operations.
    """

    def __init__(self, embedding_model: EmbeddingModel | None = None):
        self.embedding_model = embedding_model or EmbeddingModel()
        self._index = None
        self._chunks: list[Chunk] = []

    @property
    def index(self):
        """Lazy-initialize FAISS index."""
        if self._index is None:
            try:
                import faiss
                dim = self.embedding_model.dim
                # IndexFlatIP = brute-force inner product search
                # Since our embeddings are L2-normalized, IP = cosine similarity
                self._index = faiss.IndexFlatIP(dim)
            except ImportError:
                raise ImportError("faiss not installed. Run: pip install faiss-cpu")
        return self._index

    def add(self, chunks: list[Chunk]) -> int:
        """Embed and index a list of chunks.

        Args:
            chunks: List of Chunk objects to add

        Returns:
            Number of chunks added
        """
        if not chunks:
            return 0

        texts = [c.text for c in chunks]
        embeddings = self.embedding_model.embed(texts)  # (n, dim)

        self.index.add(embeddings)
        self._chunks.extend(chunks)

        return len(chunks)

    def search(self, query: str, top_k: int = 5) -> list[tuple[Chunk, float]]:
        """Search for the most similar chunks to a query.

        Args:
            query: Search query text
            top_k: Number of results to return

        Returns:
            List of (chunk, similarity_score) tuples, sorted by relevance
        """
        if len(self._chunks) == 0:
            return []

        query_embedding = self.embedding_model.embed(query)  # (1, dim)
        top_k = min(top_k, len(self._chunks))

        # FAISS search returns (distances, indices)
        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0:  # FAISS returns -1 for empty slots
                results.append((self._chunks[idx], float(score)))

        return results

    def __len__(self) -> int:
        return len(self._chunks)

    def save(self, path: str | Path) -> None:
        """Save index and chunks to disk."""
        import faiss

        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

        # Save FAISS index
        faiss.write_index(self.index, str(path / "index.faiss"))

        # Save chunks as JSON
        chunks_data = [asdict(c) for c in self._chunks]
        (path / "chunks.json").write_text(
            json.dumps(chunks_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load(self, path: str | Path) -> None:
        """Load index and chunks from disk."""
        import faiss

        path = Path(path)

        self._index = faiss.read_index(str(path / "index.faiss"))

        chunks_data = json.loads((path / "chunks.json").read_text(encoding="utf-8"))
        self._chunks = [Chunk(**d) for d in chunks_data]

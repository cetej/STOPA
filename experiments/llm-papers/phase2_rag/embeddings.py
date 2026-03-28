"""Embedding models for RAG.

Why embeddings?
- RAG needs to find "similar" text — but string matching misses synonyms/paraphrases
- Embeddings map text → dense vectors where semantic similarity = cosine similarity
- "king" and "monarch" have similar vectors; "king" and "table" don't

We use sentence-transformers (all-MiniLM-L6-v2) because:
- Small: ~80MB model, ~384-dim vectors
- Fast: runs on CPU in milliseconds
- Good quality: trained for semantic similarity tasks
- Open source / free

Alternative: OpenAI text-embedding-3-small (API-based, better quality, costs money)
"""

import numpy as np


class EmbeddingModel:
    """Wrapper around sentence-transformers for text embedding.

    Lazily loads the model on first use to avoid slow imports.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        """Lazy-load the model on first access."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                print(f"Loading embedding model: {self.model_name}...")
                self._model = SentenceTransformer(self.model_name)
                print(f"Loaded. Embedding dimension: {self.dim}")
            except ImportError:
                raise ImportError(
                    "sentence-transformers not installed. Run: pip install sentence-transformers"
                )
        return self._model

    @property
    def dim(self) -> int:
        """Embedding vector dimension."""
        return self.model.get_sentence_embedding_dimension()

    def embed(self, texts: str | list[str]) -> np.ndarray:
        """Embed one or more texts into dense vectors.

        Args:
            texts: Single string or list of strings

        Returns:
            numpy array of shape (n_texts, dim) — L2-normalized vectors
        """
        if isinstance(texts, str):
            texts = [texts]

        # sentence-transformers handles batching internally
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,  # L2 normalize → cosine sim = dot product
            show_progress_bar=False,
        )
        return np.array(embeddings, dtype=np.float32)

    def similarity(self, query: str, documents: list[str]) -> list[float]:
        """Compute cosine similarity between a query and multiple documents.

        Returns list of similarity scores (higher = more similar).
        Useful for quick testing without a full vector store.
        """
        q_emb = self.embed(query)       # (1, dim)
        d_emb = self.embed(documents)   # (n, dim)
        # Cosine similarity = dot product (vectors are already L2-normalized)
        scores = (q_emb @ d_emb.T).flatten().tolist()
        return scores

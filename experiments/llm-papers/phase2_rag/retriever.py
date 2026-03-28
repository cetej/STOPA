"""Retriever — orchestrates chunking, embedding, and search.

This is the "R" in RAG. Given a corpus of documents and a query,
it returns the most relevant passages.

The retriever is separate from the RAG pipeline because:
1. You might want retrieval without generation (search use case)
2. Different RAG strategies use retrievers differently
3. Retriever can be tested independently of the LLM
"""

from pathlib import Path

from .chunker import Chunk, chunk_fixed_size, chunk_semantic
from .embeddings import EmbeddingModel
from .vector_store import VectorStore


class Retriever:
    """Document retriever with indexing and search.

    Usage:
        retriever = Retriever()
        retriever.index_file("data/shakespeare.txt")
        results = retriever.search("What does Hamlet say about death?", top_k=3)
    """

    def __init__(
        self,
        embedding_model: EmbeddingModel | None = None,
        chunk_strategy: str = "fixed",  # "fixed" or "semantic"
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        self.embedding_model = embedding_model or EmbeddingModel()
        self.vector_store = VectorStore(self.embedding_model)
        self.chunk_strategy = chunk_strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def index_text(self, text: str, doc_id: str = "doc") -> int:
        """Chunk and index a text document.

        Returns: number of chunks indexed
        """
        if self.chunk_strategy == "semantic":
            chunks = chunk_semantic(text, max_chunk_size=self.chunk_size, doc_id=doc_id)
        else:
            chunks = chunk_fixed_size(
                text, chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap, doc_id=doc_id,
            )

        n_added = self.vector_store.add(chunks)
        return n_added

    def index_file(self, path: str | Path, doc_id: str | None = None) -> int:
        """Read and index a text file.

        Returns: number of chunks indexed
        """
        path = Path(path)
        doc_id = doc_id or path.stem
        text = path.read_text(encoding="utf-8")
        return self.index_text(text, doc_id)

    def search(self, query: str, top_k: int = 5) -> list[tuple[Chunk, float]]:
        """Search for chunks most relevant to the query.

        Returns: list of (Chunk, similarity_score) tuples
        """
        return self.vector_store.search(query, top_k)

    def search_formatted(self, query: str, top_k: int = 5) -> str:
        """Search and return formatted results as a string.

        Useful for injecting into LLM prompts.
        """
        results = self.search(query, top_k)
        if not results:
            return "No relevant documents found."

        parts = []
        for i, (chunk, score) in enumerate(results, 1):
            parts.append(f"[{i}] (score: {score:.3f}, source: {chunk.doc_id})\n{chunk.text}")

        return "\n\n".join(parts)

    @property
    def n_chunks(self) -> int:
        return len(self.vector_store)

    def save(self, path: str | Path) -> None:
        self.vector_store.save(path)

    def load(self, path: str | Path) -> None:
        self.vector_store.load(path)

"""Tests for RAG pipeline components.

Tests chunking, embedding, retrieval — no LLM needed.
Embedding model downloads on first run (~80MB).
"""

from phase2_rag.chunker import Chunk, chunk_fixed_size, chunk_semantic
from phase2_rag.llm_client import MockLLMClient
from phase2_rag.rag_pipeline import RAGPipeline


class TestChunking:
    def test_fixed_size_basic(self):
        text = "A" * 100
        chunks = chunk_fixed_size(text, chunk_size=30, chunk_overlap=10)
        assert len(chunks) >= 3
        assert all(len(c.text) <= 30 for c in chunks)

    def test_fixed_size_overlap(self):
        text = "abcdefghij" * 10  # 100 chars
        chunks = chunk_fixed_size(text, chunk_size=30, chunk_overlap=10)
        # With overlap, consecutive chunks should share some text
        if len(chunks) >= 2:
            # End of chunk[0] should overlap with start of chunk[1]
            overlap = chunks[0].text[-10:]
            assert overlap in chunks[1].text

    def test_fixed_size_empty(self):
        assert chunk_fixed_size("") == []
        assert chunk_fixed_size("   ") == []

    def test_fixed_size_metadata(self):
        chunks = chunk_fixed_size("Hello world test", chunk_size=100, doc_id="test_doc")
        assert chunks[0].doc_id == "test_doc"
        assert chunks[0].chunk_id == 0

    def test_semantic_paragraphs(self):
        text = "First paragraph with some content.\n\nSecond paragraph here.\n\nThird paragraph."
        chunks = chunk_semantic(text, max_chunk_size=1000)
        # Should keep all in one chunk since total < max_chunk_size
        assert len(chunks) >= 1
        assert "First paragraph" in chunks[0].text

    def test_semantic_split_large(self):
        text = "Short para.\n\n" + "Long paragraph. " * 100 + "\n\nAnother short."
        chunks = chunk_semantic(text, max_chunk_size=200)
        assert len(chunks) >= 2  # Should split the long paragraph


class TestEmbeddings:
    """These tests require sentence-transformers to be installed.
    Skip gracefully if not available.
    """

    def test_embedding_dimension(self):
        try:
            from phase2_rag.embeddings import EmbeddingModel
            model = EmbeddingModel()
            emb = model.embed("Hello world")
            assert emb.shape == (1, 384)  # MiniLM-L6 = 384 dims
        except ImportError:
            print("  SKIP (sentence-transformers not installed)")

    def test_similarity_ordering(self):
        try:
            from phase2_rag.embeddings import EmbeddingModel
            model = EmbeddingModel()
            scores = model.similarity(
                "king and queen of England",
                ["royal monarchy", "pizza recipe", "medieval throne"]
            )
            # "royal monarchy" should be most similar
            assert scores[0] > scores[1], "Royal monarchy should be more similar than pizza"
        except ImportError:
            print("  SKIP (sentence-transformers not installed)")


class TestRAGPipeline:
    def test_mock_pipeline(self):
        llm = MockLLMClient(responses={
            "context": "Based on the context, the answer is 42."
        })
        rag = RAGPipeline(llm_client=llm)
        rag.index_text("The meaning of life is 42. This is a well-known fact.", doc_id="test")
        answer = rag.ask("What is the meaning of life?")
        assert answer.text  # Should get some response
        assert answer.question == "What is the meaning of life?"
        assert len(answer.sources) > 0


if __name__ == "__main__":
    import traceback

    test_classes = [TestChunking, TestEmbeddings, TestRAGPipeline]
    passed = 0
    failed = 0

    for cls in test_classes:
        instance = cls()
        for method_name in sorted(dir(instance)):
            if not method_name.startswith("test_"):
                continue
            try:
                getattr(instance, method_name)()
                print(f"  PASS  {cls.__name__}.{method_name}")
                passed += 1
            except Exception as e:
                print(f"  FAIL  {cls.__name__}.{method_name}: {e}")
                traceback.print_exc()
                failed += 1

    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed")

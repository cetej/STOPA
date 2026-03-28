"""Full RAG Pipeline — Retrieve, Augment, Generate.

Paper: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
       (Lewis et al., 2020)

The RAG pipeline:
1. RETRIEVE: find relevant document chunks for the query
2. AUGMENT:  inject retrieved context into the LLM prompt
3. GENERATE: LLM produces an answer grounded in the context

Why RAG over just using a bigger model?
- Models hallucinate when they don't know something — RAG provides evidence
- Knowledge can be updated by updating the document index (no retraining)
- Answers are traceable — you can cite which documents were used
- Cheaper than training a model to memorize everything

This is the dominant pattern for enterprise AI: internal docs → vector index → RAG.
"""

from .llm_client import LLMClient, LLMResponse, MockLLMClient
from .retriever import Retriever


RAG_SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on the provided context.

Rules:
- Answer ONLY based on the provided context. If the context doesn't contain the answer, say so.
- Quote relevant parts of the context to support your answer.
- Be concise and direct.
- If the question is ambiguous, ask for clarification."""

RAG_USER_TEMPLATE = """Context (retrieved documents):
{context}

---

Question: {question}

Answer based on the context above:"""


class RAGPipeline:
    """Full RAG pipeline combining retrieval and generation.

    Usage:
        rag = RAGPipeline(llm_client=LLMClient())
        rag.index_file("data/shakespeare.txt")
        answer = rag.ask("What does Hamlet think about death?")
        print(answer.text)
        print(answer.sources)
    """

    def __init__(
        self,
        llm_client: LLMClient | MockLLMClient | None = None,
        retriever: Retriever | None = None,
        top_k: int = 3,
        system_prompt: str = RAG_SYSTEM_PROMPT,
    ):
        self.llm = llm_client or MockLLMClient()
        self.retriever = retriever or Retriever()
        self.top_k = top_k
        self.system_prompt = system_prompt

    def index_text(self, text: str, doc_id: str = "doc") -> int:
        """Index a document for retrieval."""
        return self.retriever.index_text(text, doc_id)

    def index_file(self, path: str, doc_id: str | None = None) -> int:
        """Index a file for retrieval."""
        return self.retriever.index_file(path, doc_id)

    def ask(
        self,
        question: str,
        top_k: int | None = None,
        temperature: float = 0.3,
    ) -> "RAGAnswer":
        """Ask a question using RAG.

        Steps:
        1. Retrieve top-k relevant chunks
        2. Build prompt with retrieved context
        3. Generate answer via LLM
        4. Return answer with source attribution

        Args:
            question: The question to answer
            top_k: Override default number of retrieved chunks
            temperature: LLM sampling temperature (lower = more factual)

        Returns:
            RAGAnswer with text, sources, and metadata
        """
        top_k = top_k or self.top_k

        # 1. RETRIEVE
        results = self.retriever.search(question, top_k)
        context = self.retriever.search_formatted(question, top_k)

        # 2. AUGMENT — build the prompt
        prompt = RAG_USER_TEMPLATE.format(context=context, question=question)

        # 3. GENERATE
        response = self.llm.generate(
            prompt=prompt,
            system=self.system_prompt,
            temperature=temperature,
        )

        # 4. Package result
        sources = [
            {"text": chunk.text[:200], "doc_id": chunk.doc_id, "score": score}
            for chunk, score in results
        ]

        return RAGAnswer(
            text=response.text,
            sources=sources,
            context_used=context,
            question=question,
        )


class RAGAnswer:
    """Structured RAG response with source attribution."""

    def __init__(self, text: str, sources: list[dict], context_used: str, question: str):
        self.text = text
        self.sources = sources
        self.context_used = context_used
        self.question = question

    def __str__(self) -> str:
        parts = [f"Q: {self.question}", f"A: {self.text}", "", "Sources:"]
        for i, src in enumerate(self.sources, 1):
            parts.append(f"  [{i}] {src['doc_id']} (score: {src['score']:.3f})")
            parts.append(f"      {src['text'][:100]}...")
        return "\n".join(parts)

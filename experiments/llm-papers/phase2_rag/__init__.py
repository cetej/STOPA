"""Phase 2A: Retrieval-Augmented Generation (RAG) from scratch.

Paper: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
       (Lewis et al., 2020)

RAG combines a retrieval system with a language model:
1. Index documents as vector embeddings
2. At query time, retrieve the most relevant chunks
3. Inject retrieved context into the LLM prompt
4. Generate an answer grounded in the retrieved evidence

This implementation avoids LangChain/LlamaIndex to expose the internals.
"""

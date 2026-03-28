"""Interactive RAG demo on Shakespeare data.

Usage:
    # With Ollama (local, free):
    ollama run llama3.2:3b  # In another terminal
    python -m phase2_rag.demo_rag

    # With OpenAI:
    LLM_BASE_URL=https://api.openai.com/v1 LLM_API_KEY=sk-... LLM_MODEL=gpt-4o-mini \
    python -m phase2_rag.demo_rag

    # Mock mode (no LLM needed, tests retrieval only):
    python -m phase2_rag.demo_rag --mock
"""

import argparse
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Ensure parent directory is in path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from phase2_rag.llm_client import LLMClient, MockLLMClient
from phase2_rag.rag_pipeline import RAGPipeline

DATA_DIR = Path(__file__).parent.parent / "data"


def main():
    parser = argparse.ArgumentParser(description="RAG Demo on Shakespeare")
    parser.add_argument("--mock", action="store_true", help="Use mock LLM (retrieval only)")
    parser.add_argument("--data", default=str(DATA_DIR / "shakespeare.txt"))
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    # Initialize LLM
    if args.mock:
        print("Running in MOCK mode (retrieval only, no LLM generation)")
        llm = MockLLMClient(responses={
            "context": "Based on the retrieved passages, here is what I found in the text.",
        })
    else:
        llm = LLMClient()
        print(f"LLM: {llm.model} @ {llm.base_url}")

    # Build RAG pipeline
    rag = RAGPipeline(llm_client=llm, top_k=args.top_k)

    # Index Shakespeare
    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Data file not found: {data_path}")
        print("Run training first to download: python -m phase1_transformer.train --max-steps 1")
        return

    print(f"\nIndexing {data_path.name}...")
    n_chunks = rag.index_file(str(data_path), doc_id="shakespeare")
    print(f"Indexed {n_chunks} chunks\n")

    # Interactive QA loop
    print("Shakespeare RAG — ask questions about the text. Ctrl+C to exit.\n")
    print("Example questions:")
    print("  - What does Hamlet say about death?")
    print("  - Who is Juliet in love with?")
    print("  - What happens in the final act of Macbeth?")
    print()

    while True:
        try:
            question = input("Q: ").strip()
            if not question:
                continue

            if question.lower() in ("quit", "exit", "q"):
                break

            # Show retrieval results
            print("\n--- Retrieved chunks ---")
            results = rag.retriever.search(question, args.top_k)
            for i, (chunk, score) in enumerate(results, 1):
                print(f"[{i}] score={score:.3f}: {chunk.text[:150]}...")
            print()

            # Generate answer
            answer = rag.ask(question)
            print(f"A: {answer.text}\n")

        except KeyboardInterrupt:
            print("\nBye!")
            break


if __name__ == "__main__":
    main()

"""Interactive ReAct agent demo.

Usage:
    # With Ollama:
    ollama run llama3.2:3b
    python -m phase2_react.demo_react

    # With OpenAI:
    LLM_BASE_URL=https://api.openai.com/v1 LLM_API_KEY=sk-... LLM_MODEL=gpt-4o-mini \
    python -m phase2_react.demo_react

    # Mock mode (tests ReAct parsing without real LLM):
    python -m phase2_react.demo_react --mock
"""

import argparse
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent.parent))

from phase2_rag.llm_client import LLMClient, MockLLMClient
from phase2_rag.retriever import Retriever
from phase2_react.react_agent import ReActAgent
from phase2_react.tools import get_default_tools

DATA_DIR = Path(__file__).parent.parent / "data"


def add_rag_tool(tools, retriever):
    """Add a search_docs tool backed by the RAG retriever."""
    def search_docs(query: str) -> str:
        results = retriever.search(query, top_k=3)
        if not results:
            return "No relevant documents found."
        parts = []
        for chunk, score in results:
            parts.append(f"[score={score:.2f}] {chunk.text[:300]}")
        return "\n---\n".join(parts)

    tools.register(
        "search_docs",
        "Search through indexed documents. Input: search query about the text.",
        search_docs,
    )


def main():
    parser = argparse.ArgumentParser(description="ReAct Agent Demo")
    parser.add_argument("--mock", action="store_true", help="Use mock LLM")
    parser.add_argument("--no-rag", action="store_true", help="Don't index Shakespeare for search")
    args = parser.parse_args()

    # Initialize tools
    tools = get_default_tools()

    # Optionally add RAG-backed search
    if not args.no_rag:
        shakespeare_path = DATA_DIR / "shakespeare.txt"
        if shakespeare_path.exists():
            print("Indexing Shakespeare for search_docs tool...")
            retriever = Retriever()
            n = retriever.index_file(shakespeare_path)
            add_rag_tool(tools, retriever)
            print(f"Indexed {n} chunks. Tool 'search_docs' available.\n")
        else:
            print("Shakespeare data not found. Run phase1 training first to download.\n")

    # Initialize LLM
    if args.mock:
        llm = MockLLMClient(responses={
            "square root": "Thought: I need to calculate the square root.\nAction: calculator(sqrt(144))",
            "calculator": "Thought: The calculator returned 12. Adding 13 gives 25.\nFinal Answer: 25",
            "hamlet": "Thought: I need to search for information about Hamlet.\nAction: search_docs(hamlet death)",
            "search_docs": "Thought: Based on the passages, Hamlet contemplates mortality.\nFinal Answer: Hamlet reflects on death in his famous soliloquy.",
            "default": "Thought: Let me think about this.\nFinal Answer: I need more information to answer.",
        })
        print("Running in MOCK mode\n")
    else:
        llm = LLMClient()
        print(f"LLM: {llm.model} @ {llm.base_url}\n")

    # Create agent
    agent = ReActAgent(llm=llm, tools=tools, verbose=True)

    print(f"Available tools: {', '.join(tools.names)}")
    print("\nReAct Agent — ask questions. The agent will think and use tools.")
    print("Example: 'What is sqrt(144) + 13?' or 'What does Hamlet say about death?'\n")

    while True:
        try:
            question = input("Q: ").strip()
            if not question:
                continue
            if question.lower() in ("quit", "exit", "q"):
                break

            print(f"\n--- Agent working ---")
            result = agent.run(question)
            print(f"\n>>> Answer: {result.answer}")
            print(f"    ({result.n_steps} steps, stopped: {result.stopped_reason})\n")

        except KeyboardInterrupt:
            print("\nBye!")
            break


if __name__ == "__main__":
    main()

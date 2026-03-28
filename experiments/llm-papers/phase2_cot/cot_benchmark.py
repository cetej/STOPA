"""Chain-of-Thought Prompting Benchmark.

Paper: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
       (Wei et al., 2022)

Key insight: Adding "Let's think step by step" to a prompt dramatically
improves LLM performance on reasoning tasks — NO model changes needed.

This benchmark compares three prompting strategies:
1. Direct: "What is the answer?"
2. Zero-shot CoT: "Let's think step by step" appended
3. Few-shot CoT: Examples with step-by-step reasoning provided

The results demonstrate that prompting strategy matters as much as
model capability for reasoning tasks.

Usage:
    python -m phase2_cot.cot_benchmark
    python -m phase2_cot.cot_benchmark --mock  # No LLM needed
"""

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent.parent))

from phase2_rag.llm_client import LLMClient, MockLLMClient


# === Benchmark Tasks ===

TASKS = [
    {
        "question": "If a store sells 3 types of fruits and each type has 4 varieties, how many total varieties are there?",
        "answer": "12",
        "category": "math",
    },
    {
        "question": "A farmer has 15 chickens. He buys 6 more, then sells half of all his chickens. How many does he have left?",
        "answer": "10",  # (15 + 6) / 2 = 10.5, round to 10
        "category": "math",
    },
    {
        "question": "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly?",
        "answer": "no",
        "category": "logic",
    },
    {
        "question": "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?",
        "answer": "0.05",  # Classic cognitive bias problem
        "category": "math",
    },
    {
        "question": "If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?",
        "answer": "5",  # Each machine makes 1 widget in 5 minutes
        "category": "math",
    },
    {
        "question": "John is taller than Mary. Mary is taller than Sue. Is John taller than Sue?",
        "answer": "yes",
        "category": "logic",
    },
]


# === Few-shot CoT Examples ===

FEW_SHOT_EXAMPLES = """Example 1:
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How many does he have now?
A: Roger started with 5 balls. He bought 2 cans of 3 balls each, so 2 * 3 = 6 new balls. 5 + 6 = 11.
The answer is 11.

Example 2:
Q: If all dogs are animals and some animals are pets, can we conclude all dogs are pets?
A: We know all dogs are animals. We know some animals are pets. But "some animals are pets" doesn't mean ALL animals are pets. So we cannot conclude all dogs are pets — only some dogs might be.
The answer is no.

"""


def extract_answer(response: str) -> str:
    """Extract the final answer from an LLM response.

    Looks for patterns like "The answer is X", "= X", or the last number.
    """
    text = response.lower().strip()

    # Try "the answer is X"
    match = re.search(r"the answer is[:\s]*([^\n.]+)", text)
    if match:
        return match.group(1).strip().rstrip(".")

    # Try "= X" at end
    match = re.search(r"=\s*([0-9.$]+)", text)
    if match:
        return match.group(1).strip()

    # Try last number in response
    numbers = re.findall(r"[0-9.]+", text)
    if numbers:
        return numbers[-1]

    # Try yes/no
    if "yes" in text.split()[-5:]:
        return "yes"
    if "no" in text.split()[-5:]:
        return "no"

    return text.strip()


def check_answer(extracted: str, expected: str) -> bool:
    """Fuzzy comparison of extracted vs expected answer."""
    extracted = extracted.lower().strip().replace("$", "").replace(",", "")
    expected = expected.lower().strip().replace("$", "").replace(",", "")

    if extracted == expected:
        return True

    # Try numeric comparison
    try:
        return abs(float(extracted) - float(expected)) < 0.01
    except ValueError:
        pass

    return expected in extracted


def run_benchmark(llm, verbose: bool = True):
    """Run all three prompting strategies and compare."""
    strategies = {
        "direct": lambda q: q + "\nAnswer with just the number or yes/no.",
        "zero_shot_cot": lambda q: q + "\nLet's think step by step.",
        "few_shot_cot": lambda q: FEW_SHOT_EXAMPLES + f"Q: {q}\nA:",
    }

    results = {name: {"correct": 0, "total": 0} for name in strategies}

    for task in TASKS:
        if verbose:
            print(f"\n{'='*60}")
            print(f"Q: {task['question']}")
            print(f"Expected: {task['answer']}")

        for strategy_name, prompt_fn in strategies.items():
            prompt = prompt_fn(task["question"])
            response = llm.generate(prompt, temperature=0.1, max_tokens=300)
            extracted = extract_answer(response.text)
            correct = check_answer(extracted, task["answer"])

            results[strategy_name]["total"] += 1
            if correct:
                results[strategy_name]["correct"] += 1

            if verbose:
                status = "CORRECT" if correct else "WRONG"
                print(f"  [{strategy_name}] → {extracted} ({status})")
                if strategy_name == "zero_shot_cot" and not correct:
                    print(f"    Full response: {response.text[:200]}...")

    # Summary
    print(f"\n{'='*60}")
    print("RESULTS SUMMARY")
    print(f"{'='*60}")
    for name, r in results.items():
        acc = r["correct"] / max(r["total"], 1) * 100
        print(f"  {name:20s}: {r['correct']}/{r['total']} ({acc:.0f}%)")

    print(f"\nKey takeaway from Wei et al. (2022):")
    print(f"  'Let\\'s think step by step' costs zero extra engineering")
    print(f"  but can dramatically improve reasoning accuracy.")


def main():
    parser = argparse.ArgumentParser(description="CoT Prompting Benchmark")
    parser.add_argument("--mock", action="store_true", help="Use mock LLM")
    args = parser.parse_args()

    if args.mock:
        # Mock responses that simulate typical LLM behavior
        llm = MockLLMClient(responses={
            # Direct (often gets tricked)
            "just the number": "10 cents",  # Wrong for bat/ball
            # CoT (reasoning helps)
            "step by step": "Let me work through this step by step.\n"
                           "The answer is computed by careful reasoning.\nThe answer is 5.",
            # Few-shot (examples guide format)
            "Example 1": "We need to calculate carefully.\nThe answer is 0.05.",
        })
        print("Mock mode — showing format only (use real LLM for meaningful results)\n")
    else:
        llm = LLMClient()
        print(f"LLM: {llm.model}\n")

    run_benchmark(llm)


if __name__ == "__main__":
    main()

"""Quick smoke test for TriAttention vLLM server.

Usage:
    python scripts/triattention-test.py                    # default localhost:8000
    python scripts/triattention-test.py --port 8001        # custom port
    python scripts/triattention-test.py --long             # test long reasoning (1K+ tokens)

Tests:
    1. Server health (GET /v1/models)
    2. Short reasoning (math problem)
    3. Long reasoning (optional, --long flag)
"""

import argparse
import json
import sys
import time

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def test_health(base_url: str) -> bool:
    """Check server is responding."""
    try:
        resp = requests.get(f"{base_url}/v1/models", timeout=5)
        resp.raise_for_status()
        models = resp.json()
        model_ids = [m["id"] for m in models.get("data", [])]
        print(f"  Models: {', '.join(model_ids)}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"  FAIL: Cannot connect to {base_url}")
        return False
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def test_reasoning(base_url: str, model: str, prompt: str, expected: str, label: str) -> dict:
    """Send a reasoning prompt and check response."""
    start = time.time()
    try:
        resp = requests.post(
            f"{base_url}/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2048,
                "temperature": 0.0,
            },
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        elapsed = time.time() - start

        text = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        total_tokens = usage.get("total_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)

        correct = expected.lower() in text.lower()
        tps = completion_tokens / elapsed if elapsed > 0 else 0

        print(f"  Answer correct: {'YES' if correct else 'NO'}")
        print(f"  Tokens: {total_tokens} total, {completion_tokens} completion")
        print(f"  Latency: {elapsed:.1f}s ({tps:.1f} tok/s)")

        return {"pass": correct, "tokens": total_tokens, "latency": elapsed, "tps": tps}
    except Exception as e:
        print(f"  FAIL: {e}")
        return {"pass": False, "tokens": 0, "latency": 0, "tps": 0}


def main():
    parser = argparse.ArgumentParser(description="TriAttention vLLM smoke test")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--long", action="store_true", help="Include long reasoning test")
    args = parser.parse_args()

    base_url = f"http://{args.host}:{args.port}"

    print(f"=== TriAttention Smoke Test ({base_url}) ===\n")

    # Test 1: Health
    print("[1/3] Server health...")
    if not test_health(base_url):
        print("\nServer not responding. Is vLLM running?")
        print(f"  Start with: ./scripts/triattention-serve.sh --port {args.port}")
        sys.exit(1)

    # Get model name
    models = requests.get(f"{base_url}/v1/models").json()
    model = models["data"][0]["id"]
    print(f"  Using model: {model}\n")

    # Test 2: Short reasoning
    print("[2/3] Short reasoning (27 * 43)...")
    short = test_reasoning(
        base_url, model,
        prompt="What is 27 * 43? Think step by step, then give the final answer.",
        expected="1161",
        label="short",
    )

    # Test 3: Long reasoning (optional)
    if args.long:
        print("\n[3/3] Long reasoning (combinatorics)...")
        long = test_reasoning(
            base_url, model,
            prompt=(
                "How many ways can you arrange 8 people around a circular table "
                "if 2 specific people must not sit next to each other? "
                "Show your complete reasoning step by step."
            ),
            expected="3600",
            label="long",
        )
    else:
        print("\n[3/3] Long reasoning... SKIPPED (use --long to enable)")
        long = None

    # Summary
    print("\n=== Summary ===")
    results = [("Short reasoning", short)]
    if long:
        results.append(("Long reasoning", long))

    all_pass = True
    for label, r in results:
        status = "PASS" if r["pass"] else "FAIL"
        all_pass = all_pass and r["pass"]
        print(f"  {label}: {status} ({r['latency']:.1f}s, {r['tps']:.1f} tok/s)")

    print(f"\nOverall: {'ALL PASS' if all_pass else 'SOME FAILURES'}")
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()

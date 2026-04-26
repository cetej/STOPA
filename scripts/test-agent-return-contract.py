"""Validation tests for agent-return-contract.md spec (issue #18 Phase 1).

Run: python scripts/test-agent-return-contract.py
Exit 0 = all pass, 1 = any fail. Suitable for CI.

Validates:
  1. JSON blocks in spec are syntactically valid (1 schema + 3 examples)
  2. Schema required fields, enum values, blocker types match spec text
  3. Each example conforms (required, enums, brief length, blockers rule)
  4. Orchestrator parser routes example outputs deterministically
  5. Backward compat fallbacks: free-form / malformed / missing-required / invalid-enum
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CONTRACT_PATH = Path(".claude/skills/orchestrate/references/agent-return-contract.md")


def load_blocks() -> tuple[dict, list[dict]]:
    text = CONTRACT_PATH.read_text(encoding="utf-8")
    blocks = re.findall(r"```json\s*\n(.*?)\n```", text, re.DOTALL)
    if len(blocks) != 4:
        raise SystemExit(f"FAIL: expected 4 JSON blocks, got {len(blocks)}")
    parsed = [json.loads(b) for b in blocks]
    return parsed[0], parsed[1:]


def parse_agent_output(raw: str, schema: dict) -> tuple[str, object, str]:
    """Proxy of Phase 2 orchestrator parser. Returns (status_type, parsed_or_raw, route)."""
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return ("freeform", raw, "fallback_haiku_verifier")
    for f in schema.get("required", []):
        if f not in parsed:
            return ("invalid_json", parsed, "fallback_haiku_verifier")
    if parsed.get("status") not in schema["properties"]["status"]["enum"]:
        return ("invalid_enum", parsed, "fallback_haiku_verifier")
    nas = parsed.get("next_action_signal")
    status = parsed["status"]
    if status == "complete" and nas == "ready_for_critic":
        route = "phase_5_critic"
    elif status == "blocked" and nas == "needs_user_input":
        route = "surface_to_user"
    elif status == "partial":
        route = "phase_5_critic_with_blockers_logged"
    elif status == "failed":
        route = "trigger_3fix_escalation"
    else:
        route = "default_to_critic"
    return ("contract", parsed, route)


def check_schema(schema: dict) -> list[str]:
    failures: list[str] = []
    if set(schema.get("required", [])) != {"status", "subtask_id", "brief"}:
        failures.append(f"required mismatch: {schema.get('required')}")
    if set(schema["properties"]["status"]["enum"]) != {"complete", "partial", "blocked", "failed"}:
        failures.append("status enum mismatch")
    expected_nas = {"ready_for_critic", "ready_for_next_wave", "needs_user_input", "needs_replan", "needs_retry"}
    if set(schema["properties"]["next_action_signal"]["enum"]) != expected_nas:
        failures.append("next_action_signal enum mismatch")
    expected_bt = {"missing_dep", "ambiguous_spec", "infra_error", "scope_too_big", "needs_user_input", "external_failure"}
    if set(schema["properties"]["blockers"]["items"]["properties"]["type"]["enum"]) != expected_bt:
        failures.append("blocker types mismatch")
    return failures


def check_example(idx: int, ex: dict, schema: dict) -> list[str]:
    failures: list[str] = []
    for f in schema["required"]:
        if f not in ex:
            failures.append(f"example {idx}: missing required '{f}'")
    if ex.get("status") not in schema["properties"]["status"]["enum"]:
        failures.append(f"example {idx}: bad status {ex.get('status')!r}")
    if len(ex.get("brief", "")) > 200:
        failures.append(f"example {idx}: brief exceeds 200 chars")
    needs_blockers = ex.get("status") in {"blocked", "partial", "failed"}
    if needs_blockers and not ex.get("blockers"):
        failures.append(f"example {idx}: status={ex['status']} but no blockers (spec rule)")
    nas = ex.get("next_action_signal")
    if nas is not None and nas not in schema["properties"]["next_action_signal"]["enum"]:
        failures.append(f"example {idx}: bad next_action_signal {nas!r}")
    vm = ex.get("verification_method")
    if vm is not None and vm not in schema["properties"]["verification_method"]["enum"]:
        failures.append(f"example {idx}: bad verification_method {vm!r}")
    return failures


def check_routing(examples: list[dict], schema: dict) -> list[str]:
    expected = ["phase_5_critic", "surface_to_user", "phase_5_critic_with_blockers_logged"]
    failures: list[str] = []
    for i, (ex, exp) in enumerate(zip(examples, expected), 1):
        status_type, _, route = parse_agent_output(json.dumps(ex), schema)
        if status_type != "contract" or route != exp:
            failures.append(f"example {i} routing: got ({status_type}, {route}), expected (contract, {exp})")
    return failures


def check_fallbacks(schema: dict) -> list[str]:
    cases = [
        ("free-form", "I edited 3 files and tests pass.", "freeform", "fallback_haiku_verifier"),
        ("malformed", '{"status": "complete", "brief": "missing brace"', "freeform", "fallback_haiku_verifier"),
        ("missing required", '{"status": "complete"}', "invalid_json", "fallback_haiku_verifier"),
        ("invalid enum", '{"status": "kinda", "subtask_id": "st-1", "brief": "."}', "invalid_enum", "fallback_haiku_verifier"),
    ]
    failures: list[str] = []
    for label, raw, exp_type, exp_route in cases:
        status_type, _, route = parse_agent_output(raw, schema)
        if status_type != exp_type or route != exp_route:
            failures.append(f"fallback {label}: got ({status_type}, {route}), expected ({exp_type}, {exp_route})")
    return failures


def main() -> int:
    schema, examples = load_blocks()
    print(f"Loaded {len(examples) + 1} JSON blocks (1 schema + {len(examples)} examples) -- all valid JSON")

    all_failures: list[str] = []
    for label, fn in [
        ("schema", lambda: check_schema(schema)),
        ("examples", lambda: [f for i, ex in enumerate(examples, 1) for f in check_example(i, ex, schema)]),
        ("routing", lambda: check_routing(examples, schema)),
        ("fallbacks", lambda: check_fallbacks(schema)),
    ]:
        section_failures = fn()
        if section_failures:
            print(f"\n[{label}] FAIL:")
            for f in section_failures:
                print(f"  - {f}")
            all_failures.extend(section_failures)
        else:
            print(f"[{label}] PASS")

    if all_failures:
        print(f"\n=== {len(all_failures)} FAILURE(S) ===")
        return 1
    print("\n=== ALL CHECKS PASSED ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())

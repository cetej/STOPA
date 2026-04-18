"""Unit tests for generated-skill-counter.py.

Run from project root:
    python scripts/test_generated_skill_counter.py

Creates ephemeral test drafts under .claude/skills/_generated/<test-slug>/
and deletes them after assertions. No external dependencies.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import unittest
import uuid
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT = Path(__file__).parent / "generated-skill-counter.py"
SANDBOX = Path(".claude/skills/_generated")


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def _make_draft(slug: str, with_counters: bool = False) -> Path:
    skill_dir = SANDBOX / slug
    skill_dir.mkdir(parents=True, exist_ok=True)
    path = skill_dir / "SKILL.md"
    counters = (
        "uses: 2\nsuccessful_uses: 1\nharmful_uses: 0\n" if with_counters else ""
    )
    path.write_text(
        f"""---
name: {slug}
description: "Use when testing the counter script."
maturity: draft
{counters}---

# Test body
""",
        encoding="utf-8",
    )
    return skill_dir


class CounterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.slug = f"_testctr-{uuid.uuid4().hex[:8]}"

    def tearDown(self) -> None:
        shutil.rmtree(SANDBOX / self.slug, ignore_errors=True)

    def _read_counters(self) -> dict[str, int]:
        result = _run(["read", self.slug, "--json"])
        import json
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        return json.loads(result.stdout)

    def test_init_lazy_on_first_increment_pass(self) -> None:
        _make_draft(self.slug, with_counters=False)
        result = _run(["increment", self.slug, "--critic", "PASS"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        counters = self._read_counters()
        self.assertEqual(counters["uses"], 1)
        self.assertEqual(counters["successful_uses"], 1)
        self.assertEqual(counters["harmful_uses"], 0)

    def test_increment_existing_pass(self) -> None:
        _make_draft(self.slug, with_counters=True)
        _run(["increment", self.slug, "--critic", "PASS"])
        counters = self._read_counters()
        self.assertEqual(counters["uses"], 3)
        self.assertEqual(counters["successful_uses"], 2)
        self.assertEqual(counters["harmful_uses"], 0)

    def test_fail_bumps_harmful(self) -> None:
        _make_draft(self.slug, with_counters=True)
        _run(["increment", self.slug, "--critic", "FAIL"])
        counters = self._read_counters()
        self.assertEqual(counters["uses"], 3)
        self.assertEqual(counters["successful_uses"], 1)
        self.assertEqual(counters["harmful_uses"], 1)

    def test_none_critic_no_side_counters(self) -> None:
        _make_draft(self.slug, with_counters=True)
        _run(["increment", self.slug, "--critic", "NONE"])
        counters = self._read_counters()
        self.assertEqual(counters["uses"], 3)
        self.assertEqual(counters["successful_uses"], 1)
        self.assertEqual(counters["harmful_uses"], 0)

    def test_case_insensitive_critic(self) -> None:
        _make_draft(self.slug, with_counters=False)
        _run(["increment", self.slug, "--critic", "pass"])
        counters = self._read_counters()
        self.assertEqual(counters["successful_uses"], 1)

    def test_missing_skill_fails(self) -> None:
        result = _run(["read", f"nonexistent-{uuid.uuid4().hex[:6]}"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ERROR", result.stderr)

    def test_frontmatter_preserved(self) -> None:
        skill_dir = _make_draft(self.slug, with_counters=True)
        _run(["increment", self.slug, "--critic", "PASS"])
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("description:", text)
        self.assertIn("maturity: draft", text)
        self.assertIn("# Test body", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)

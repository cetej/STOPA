# Pending Reminders

Date-gated tasks surfaced at SessionStart when `due_date <= today`.
Format: YAML entries. `pending-reminders.sh` hook parses and emits banner.
NOT auto-regenerated — only manual edits + /scribe appends.

Archive completed items to `pending-reminders-archive.md` (don't delete — audit trail).

---

- id: evolve-15-pipeline-recovery
  due_date: 2026-04-20
  priority: high
  title: "/evolve #15 — signal pipeline recovery check (48h after fix 6b425ef)"
  context: |
    Signal pipeline fix pushnut 2026-04-18 04:00 (commit `6b425ef`).
    Potřebuje 48h na akumulaci dat před /evolve re-run.
    Čekáme na: `uses-ledger.json` (byl `{}`), `corrections.jsonl` plnění,
    `panic-episodes.jsonl` růst.
  action: |
    Run /evolve (cyklus #15). Porovnej signal flow s 2026-04-18 baseline.
    Zapiš do evolution-log.md jako běh #15 s konkrétními čísly (uses deltas,
    graduation re-evaluation).
  red_flags: |
    - uses-ledger prázdný po 48h → uses-tracker stále broken
    - corrections.jsonl 0 entries (a user měl korekce) → correction-tracker broken
    - žádné nové panic episodes po high-edit session → panic-detector broken
  detail_ref: .claude/memory/handoff-2026-04-18-signal-pipeline.md (Follow-up 3)
  created: 2026-04-18

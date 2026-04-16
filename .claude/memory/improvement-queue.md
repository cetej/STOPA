# Improvement Queue

Generated: 2026-04-16 (evolve #13 cleanup)

| Priority | Type | Pattern | Count | Action |
|----------|------|---------|-------|--------|
| 3 | violation | NEVER write API keys/tokens into JSON config files. Use environment variables or | 1 | ALREADY_COVERED by core-invariants #4 |
| 3 | violation | 6. Analysis-Paralysis Guard | 1 | stale — stopa-worker.md line 28 already has rule; verify_check regex bug |
| 3 | violation | Setting CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70 triggers context compaction earlier ( | 1 | ALREADY_FIXED (verify → manual in #5) |
| 3 | violation | AutoAgent's anti-overfitting guard: ask 'if this exact eval case disappeared, wo | 1 | stale verify_check path |
| 3 | violation | Tool-Genesis (arXiv:2603.05578) prokázal cascade failure — drobné L1 chyby zesil | 1 | stale verify_check path |

<!-- Cleaned 2026-04-16 evolve #13: removed 5 stale references to runtime-created files
     (implementation-plan.md, scratchpad.md, panic-episodes.jsonl, wiki/.compile, briefings/*)
     — these files are created by skills on first run; they're in RUNTIME_CREATED set in verify-sweep.py
     but a separate writer (likely auto-scribe or improvement-router) re-adds them. Root fix needed. -->

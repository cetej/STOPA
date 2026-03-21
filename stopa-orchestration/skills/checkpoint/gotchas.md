# Checkpoint — Gotchas

Known failure modes. Add a line each time Claude trips on something.

## Content Quality
- **Mixing done work with new tasks** — checkpoint = snapshot of CURRENT state, not a TODO list for next session
- **Missing resume prompt** — without a clear "start here" prompt, next session wastes time re-discovering context
- **Stale checkpoint** — checkpoint from 3 sessions ago is misleading. Always overwrite, never append
- **Version your checkpoints** — include session number and date so it's clear how old it is

## Timing
- **Save too late** — checkpoint at 70% context usage, not at 95% when you've already lost detail
- **Not saving frequently enough** — after major milestones (feature complete, bug fixed), checkpoint immediately
- **Forgetting uncommitted changes** — list dirty files in checkpoint. Next session needs to know what's staged vs committed

## Technical
- **Checkpoint file > 200 lines** — keep it focused. Move historical context to state.md archive
- **Relative dates** — write "2026-03-21" not "today" or "yesterday". Next session won't know when "today" was
- **Branch mismatch** — record current branch name. Resume on wrong branch = confusion

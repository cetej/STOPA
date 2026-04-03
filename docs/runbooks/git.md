---
category: git
severity: medium
last_updated: 2026-04-03
---

# Git — Runbook

## Merge conflict

**Symptom:** Git reports merge conflicts during pull/merge/rebase
**Cause:** Divergent changes on same lines
**Fix:**
1. Read BOTH versions carefully
2. Choose correct resolution (don't blindly accept either side)
3. Stage resolved files and continue merge/rebase

**Prevention:** Frequent pulls, small PRs, clear ownership of files

---

## Detached HEAD

**Symptom:** `HEAD detached at <commit>` in git status
**Cause:** Checked out a specific commit instead of a branch
**Fix:**
1. To return: `git checkout main`
2. To save work: `git checkout -b <new-branch-name>`

---

## Push rejected (non-fast-forward)

**Symptom:** `! [rejected] main -> main (non-fast-forward)`
**Cause:** Remote has commits not in local branch
**Fix:**
1. `git pull --rebase`
2. Resolve any conflicts
3. Push again

**Prevention:** NEVER force-push without explicit user approval

---
name: feedback_always_diff_before_overwrite
description: NEVER overwrite a skill or config file without first comparing all existing versions across projects and git history
type: feedback
---

NEVER copy/overwrite a file without first diffing ALL existing versions across all projects and git history.

**Why:** Session 2026-03-27 — user had autoloop-optimized skills in NG-ROBOT (watch with decision tree, cross-references, negative triggers, edge cases from S15-S20 autoloop session). I blindly copied the older ADOBE-AUTOMAT version to STOPA without checking NG-ROBOT git history. Lost hours of optimization work. User rightly furious.

**How to apply:** Before ANY file copy/overwrite operation:
1. Find ALL versions (active skills, archives, git history across ALL projects)
2. Compare line counts and diff content
3. Take the BEST version as base, then merge improvements from others
4. NEVER assume the source you have is the latest — always verify
5. When user says "you have backups" — search EVERYWHERE before writing

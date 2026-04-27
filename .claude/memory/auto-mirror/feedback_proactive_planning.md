---
name: Proactive Implementation Plan Proposal
description: After radar/scan/research outputs, don't end with dry summary tables — proactively propose implementation plan with recommended order + tradeoff, and ask for approval to execute (one approval, then autonomous execution).
type: feedback
originSessionId: cd85f3fd-c054-4766-ade2-81a1186df941
---
When presenting findings (radar batch, /watch scan, /deepresearch output, /improve routing, etc.), the user expects:

1. **Findings summary** (table or list — current behavior)
2. **Implementation plan proposal** — recommended sequence, dependencies, tradeoffs (NEW — was missing)
3. **One approval gate** — "spustím takhle?" — then autonomous execution

NOT:
- Ending with bare table that user has to interpret
- Asking "co s tím?" or "chceš pokračovat?"
- Suggesting tools/skills without proposing concrete order

The system goal is **automatic functioning + self-improvement** — radar/improve findings should naturally trigger implementation proposals, not stop at the inventory step.

**Why:** User said: "kromě suchého výčtu už jsi měl navrhovat plán implementace a nechat si ho jen schválit s doporučením postupu. Což jsi udělal až na vyžádání." — proactive planning is part of autonomy, not a separate ask.

**How to apply:**
- After radar batch with 🔴 findings → propose implementation order (which first, why)
- After /improve routes to N issues → propose execution strategy (sequential pilot vs parallel cascade)
- After /deepresearch findings → propose how to apply them (which skill to update, what to test)
- After /watch ecosystem scan → propose evaluation/integration plan for relevant items
- Always include: recommended first step + tradeoff + dependencies + 1-line approval ask

Edge case: If feasibility is unclear (research-needed before implementation) → say so explicitly, propose research step as first action. Don't skip the planning just because it's uncertain.

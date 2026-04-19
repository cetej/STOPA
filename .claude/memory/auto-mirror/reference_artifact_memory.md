---
name: Artifacts as Memory Beyond Agent Boundary
description: arXiv:2604.08756 — environmental artifacts substitute for internal agent memory (Artifact Reduction Theorem), validates STOPA file-based memory design
type: reference
originSessionId: 16b10457-62ed-45b8-91c1-49616a4950d4
---
**Paper**: arXiv:2604.08756 — "Artifacts as Memory Beyond the Agent Boundary"

**Core claim**: Environment can store useful traces ("artifacts") that reduce how much history an agent needs internally. Artifact Reduction Theorem: if observing X now guarantees Y happened, storing both is redundant.

**STOPA relevance**:
- checkpoint.md, state.md, learnings/ = environmental artifacts that fresh sessions read back via perception (grep/Read)
- Even imperfect/fading traces help (tested with random, suboptimal, fading paths in 5 navigation settings)
- Design principle: "shape the workspace so useful traces persist where perception can pick them up"

**Practical implications**:
- Invest in better artifact surfaces (structured files, clear formats) over larger context windows
- grep-first retrieval = artifact perception mechanism
- File-based memory > vector DB for this pattern (artifacts must be directly observable, not buried in embeddings)
- Validates STOPA over in-context-only approaches: externalized memory is formally equivalent to internal state under artifact conditions

**How to apply**: When designing new memory surfaces or skills, prefer persistent observable files over transient context. Structure files for grep-ability (YAML frontmatter, consistent headings) to maximize artifact utility.

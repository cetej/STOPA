---
globs: "**/skills/*/SKILL.md"
---

# Pravidla pro SKILL.md soubory

- YAML frontmatter musí obsahovat: name, description, user-invocable
- `description` MUST start with "Use when..." — trigger conditions and exclusions ONLY
- `description` MUST NOT summarize the workflow, list steps, or describe internal mechanics
- Why: tested by obra/superpowers — workflow summaries cause Claude to shortcut the description instead of reading full skill body
- Bad: "Multi-persona code review — 6 expert perspectives (Developer, Security, QA...)"
- Good: "Use when reviewing a PR and /critic alone is not thorough enough. Trigger on 'review PR'..."
- `allowed-tools`: least privilege — jen tools které skill skutečně potřebuje
- Pokud skill zapisuje do memory: musí to být uvedeno v instructions
- Pokud skill spouští sub-agenty: musí specifikovat model (haiku/sonnet/opus) a důvod
- Konvence: anglicky pro technické instrukce, česky pro user-facing texty

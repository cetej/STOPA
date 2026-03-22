---
globs: "**/skills/*/SKILL.md"
---

# Pravidla pro SKILL.md soubory

- YAML frontmatter musí obsahovat: name, description, user-invocable
- `description` musí říkat KDY použít (pozitivní trigger) I KDY NEpoužít (negativní trigger)
- `description` musí být specifická — vágní "helps with tasks" nestačí
- `allowed-tools`: least privilege — jen tools které skill skutečně potřebuje
- Pokud skill zapisuje do memory: musí to být uvedeno v instructions
- Pokud skill spouští sub-agenty: musí specifikovat model (haiku/sonnet/opus) a důvod
- Konvence: anglicky pro technické instrukce, česky pro user-facing texty

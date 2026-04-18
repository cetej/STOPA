---
date: 2026-03-25
type: bug_fix
severity: high
component: skill
tags: [skill-matching, description, frontmatter, trigger-words]
summary: "Skill description MUST contain all trigger words — CC matches skills by description text, not by skill name or body."
source: auto_pattern
maturity: draft
verify_check: "Grep('description.*Use when', path='.claude/skills') → 1+ matches"
confidence: 0.7
uses: 0
successful_uses: 0
harmful_uses: 0
---

# Skill description MUSÍ obsahovat všechny trigger words

**Problém:** `/watch papers` nefungovalo v nové session — Claude hlásil "neznám".

**Root cause:** `description` ve frontmatter nezmiňoval "papers" ani "arXiv". Nová session vidí POUZE description pro skill matching — nikoli argument-hint ani tělo skillu.

**Fix:** Přidat všechny módy/argumenty jako trigger words do description.

**Pravidlo:** Když přidáš nový mód nebo argument do skillu, VŽDY přidej odpovídající trigger word do `description` pole. `argument-hint` nestačí — slouží jen jako nápověda po invokaci, ne pro matching.

**Příklad:**
- BAD: `description: Use when scanning for news. Trigger on 'watch', 'news'.`
- GOOD: `description: Use when scanning for news or arXiv papers. Trigger on 'watch', 'news', 'papers', 'arXiv'.`

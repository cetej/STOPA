# Implementační plán — MBIF/CPR vzory pro STOPA

**Date:** 2026-04-05
**Source:** outputs/mbif-cpr-research.md
**Scope:** 4 hlavní vzory + 3 sekundární

---

## Vzor 1: Call Chain Tracking (z MBIF-Crew)

### Problém v STOPA
Orchestrate spawne sub-agenty, ale ti neví kolik agentů běželo před nimi, co udělali, ani jaký je max depth. Když agent-3 potřebuje kontext z agent-1, musí ho explicitně dostat v promptu — ale orchestrate to nedělá systematicky.

### Jak to řeší MBIF
Dispatcher předá každému agentovi:
```
"Call chain so far: [scribe, architect]. You are step 3 of max 3."
```
Plus anti-recursion: max depth 3, žádný agent dvakrát.

### Implementace v STOPA

**Dotčené soubory:**
- `.claude/skills/orchestrate/SKILL.md` — Phase 4 (Execute), agent spawning logika
- `.claude/rules/core-invariants.md` — nové pravidlo #8 (nebo merge do #7)

**Změna v orchestrate Phase 4:**

Přidat do agent prompt template (tam kde orchestrate spawne sub-agenty):

```markdown
## Agent Context Injection (add to every sub-agent prompt)

When spawning an agent, prepend this context block:

EXECUTION CONTEXT:
- Task: {goal from state.md}
- Chain: [{agent-1-role}, {agent-2-role}, ...] → you ({current-agent-role})
- Position: {N} of {max for tier} (light=1, standard=4, deep=8)
- Prior outputs: {1-line summary of each prior agent's key result}
- Remaining budget: {from budget.md}

CHAIN RULES:
- Do NOT duplicate work already done by prior agents in the chain
- If you need output from a prior agent, it's in .claude/memory/intermediate/
- Signal completion clearly — next agent depends on your output
```

**Proč "Prior outputs" místo jen jmen:**
MBIF předává jen jména agentů, ale STOPA agenti jsou generičtí (ne fixed roles). "Prior outputs" dává víc kontextu za minimální token cost (1 řádek per agent).

**Anti-recursion — už existuje v STOPA:**
Core invariants #7 (3-fix escalation) + orchestrate circuit breakers (3× same agent = STOP). Není potřeba nové pravidlo — stačí chain tracking v promptu.

**Effort:** Low — edit 1 sekce v orchestrate SKILL.md
**Risk:** Minimal — additivní změna, neruší existující logiku

---

## Vzor 2: Post-it State (z MBIF-Crew)

### Problém v STOPA
Multi-turn skills (/orchestrate, /deepresearch) nemají lehký mechanismus pro uchování stavu mezi invokacemi. Checkpoint.md je příliš těžký (celá session), state.md je sdílený (kolize mezi skills).

### Jak to řeší MBIF
Každý agent/skill má `Meta/states/{name}.md` — max 30 řádků, přepsáno při každém běhu. Skill může po přerušení přečíst post-it a pokračovat.

### Implementace v STOPA

**Dotčené soubory:**
- `.claude/memory/intermediate/` — adresář už existuje (compact ho používá pro JSON)
- `.claude/rules/memory-files.md` — nová sekce "Skill State (post-it)"
- Skills které potřebují state: orchestrate, deepresearch, build-project, self-evolve

**Nový formát:**

`.claude/memory/intermediate/{skill-name}-state.md`:
```markdown
---
skill: orchestrate
updated: 2026-04-05T14:30
phase: 4
invocation: 2
---
# Post-it: orchestrate

## Current Phase
Phase 4 — Execute, wave 2 of 3

## Key State
- Subtasks 1-3: done (commits abc, def, ghi)
- Subtask 4: in_progress (agent spawned)
- Subtask 5-6: pending (wave 3)

## Resume Instruction
Continue Phase 4 at wave 2. Agent for subtask 4 may have completed — check intermediate/.
```

**Pravidla (přidat do memory-files.md):**

```markdown
## Skill State (post-it pattern)

- Uloženy v `.claude/memory/intermediate/{skill-name}-state.md`
- Max 30 řádků — force summarization
- Přepsáno při každém běhu (ne append, ale overwrite)
- YAML frontmatter: skill, updated, phase, invocation
- Skill na začátku čte svůj post-it — pokud existuje a je <1h starý, nabídne pokračování
- Post-it je privátní — ostatní skills ho nečtou (na rozdíl od state.md)
- Smaž po úspěšném dokončení tasku (ne po každé invokaci)
- Životnost: automatický cleanup při /sweep (soubory starší 24h)
```

**Rozdíl od checkpoint.md:**

| Aspekt | checkpoint.md | post-it |
|--------|--------------|---------|
| Scope | Celá session | Jedna skill invokace |
| Velikost | Neomezená | Max 30 řádků |
| Životnost | Přežije session restart | Max 24h, smazáno po dokončení |
| Kdo čte | Orchestrate, checkpoint skill | Jen vlastní skill |
| Kdy psát | Explicitně (/checkpoint) | Automaticky při každé invokaci |

**Effort:** Medium — edit memory-files.md, edit 3-4 skills
**Risk:** Low — post-it je v existing intermediate/ dir, nepřekrývá se s checkpoint

---

## Vzor 3: Truncation Boundary v checkpoint.md (z CPR)

### Problém v STOPA
Checkpoint.md obsahuje jak structured summary (potřebné pro resume), tak detailní data (git state, file lists). /checkpoint resume načte celý soubor — plýtvá tokeny na detaily které potřebuje jen audit.

### Jak to řeší CPR
Section heading `## Raw Session Log` funguje jako hard boundary — `/resume` nikdy nenačte text pod ní. Pseudokód: `summary_end = content.find("## Raw Session Log"); summary = content[:summary_end]`.

### Implementace v STOPA

**Dotčené soubory:**
- `.claude/skills/checkpoint/SKILL.md` — Save (Step 3) a Resume
- `.claude/memory/checkpoint.md` — nový formát

**Nový checkpoint.md formát:**

```markdown
---
saved: "2026-04-05"
task_ref: "state.md#task-xyz"
branch: feature/xyz
progress:
  completed: ["st-1", "st-3"]
  in_progress: ["st-2"]
---
# Session Checkpoint

**Saved**: 2026-04-05
**Task**: Implement feature XYZ
**Branch**: feature/xyz
**Progress**: 3/6 subtasks

## Resume Context

<2-3 sentences — what was done, what's next, key decisions>

Next action: Run tests for subtask 2, then start wave 2.

## What Was Done
- Subtask 1: refactored auth module (commit abc123)
- Subtask 3: added migration (commit def456)

## What Remains
| # | Subtask | Status | Method |
|---|---------|--------|--------|

## Failed Approaches
- **Approach A**: Why it failed → lesson

---
## Session Detail Log

<everything below this line is NEVER loaded by resume>

### Git State
(full git status, diff --stat, log)

### File Changes Detail
(per-file diffs, line counts)

### Budget Snapshot
(full budget breakdown)

### Learnings Written
(full learning entries created this session)
```

**Checkpoint resume logika (update):**

```python
# Pseudokód pro resume loading
content = read("checkpoint.md")
boundary = content.find("## Session Detail Log")
if boundary > 0:
    resume_content = content[:boundary]
else:
    resume_content = content  # fallback pro staré checkpointy
```

**Backward compatibility:** Staré checkpointy bez `## Session Detail Log` se načtou celé (fallback). Nové checkpointy šetří ~60% tokenů při resume.

**Effort:** Low-medium — edit checkpoint SKILL.md (save + resume sekce)
**Risk:** Minimal — fallback zajistí kompatibilitu se starými checkpointy

---

## Vzor 4: Confidence Keywords v session logách (z CPR)

### Problém v STOPA
Compact ukládá agent výstupy do `.claude/memory/intermediate/*.json` s `summary` polem, ale chybí dedikované klíčová slova pro grep-based search. Když chceš najít "session kde jsme řešili auth", musíš full-text grep přes JSON — pomalé a nepřesné.

### Jak to řeší CPR
Dedikované `Confidence keywords` pole v Quick Reference sekci session logu. Grep přes toto pole je rychlejší a přesnější než full-text.

### Implementace v STOPA

**Dotčené soubory:**
- `.claude/skills/compact/SKILL.md` — JSON format intermediate souborů
- `.claude/skills/checkpoint/SKILL.md` — checkpoint formát (session-level keywords)
- `.claude/memory/intermediate/scratchpad.md` — přidat keywords sloupec

**Změna v compact JSON:**

Přidat `keywords` pole do intermediate JSON:
```json
{
  "id": "scout-result",
  "savedAt": "2026-04-05T14:30:00Z",
  "keywords": ["auth", "JWT", "middleware", "refactor"],
  "summary": "...",
  "fullContent": "..."
}
```

Keywords extrahuje Haiku sub-agent současně se summary (zero extra cost):
```
Extend the existing Haiku prompt with:
"Also extract 3-8 confidence keywords: project names, technical terms,
action verbs, framework names, ticket IDs. Return as JSON array."
```

**Změna v checkpoint.md:**

Přidat `keywords:` do YAML frontmatter:
```yaml
---
saved: "2026-04-05"
keywords: ["auth", "JWT", "migration", "rate-limiting"]
branch: feature/xyz
---
```

**Změna v scratchpad.md:**

Aktuální formát: `| # | Time | Source | Summary |`
Nový formát: `| # | Time | Source | Keywords | Summary |`

**Search pattern:**
```bash
# Najdi session kde se řešilo auth
grep -rl "auth" .claude/memory/intermediate/*.json
# Nebo přes keywords pole specificky
grep -l '"keywords".*auth' .claude/memory/intermediate/*.json
```

**Effort:** Low — edit 2 soubory (compact, checkpoint), additivní pole
**Risk:** Minimal — nové pole, nic se neruší

---

## Sekundární vzory (lower priority)

### S1: PROTECTED/ARCHIVABLE section markers

**Co:** Inline značky v headinzích memory souborů pro kontrolu archivace.
**Kde:** `.claude/rules/memory-files.md` — nové pravidlo
**Implementace:**
```markdown
## Section Markers

- `(PROTECTED)` v nadpisu = sekce se nikdy nenavrhuje k archivaci při /sweep nebo /evolve
- `(ARCHIVABLE)` v nadpisu = sekce je safe k přesunu do archive při překročení limitu
- Default (bez markeru) = na dotaz při maintenance
```
**Effort:** Trivial — 5 řádků do memory-files.md, pak /sweep a /evolve respektují

### S2: "Suggested next skill" protocol

**Co:** MBIF agents signalizují dalšího agenta přes structured output section.
**STOPA ekvivalent:** Orchestrate `handoffs:` frontmatter — už existuje! Orchestrate má:
```yaml
handoffs:
  - skill: /critic
    when: "After implementation"
  - skill: /sweep
    auto: true
```
**Verdict:** STOPA to má lépe — deklarativní v YAML místo runtime parsování markdown sekcí. Žádná změna potřeba.

### S3: Destruktivní operace vždy poslední

**Co:** CPR pravidlo "compact is always last" — explicitní ordering.
**STOPA stav:** Compact SKILL.md nemá explicitní warning. Checkpoint + compact ordering není vynucen.
**Implementace:** Přidat do compact SKILL.md na začátek:
```markdown
## Pre-flight Check

Before compacting, verify:
1. If there's an active task in state.md: suggest /checkpoint first
2. If there are unsaved learnings from this session: suggest /scribe first
3. Compact is DESTRUCTIVE — clears context. Always run AFTER saves.
```
**Effort:** Trivial — 5 řádků do compact SKILL.md

---

## Prioritizace

| # | Vzor | Effort | Impact | Priority |
|---|------|--------|--------|----------|
| 1 | Call chain tracking | Low | High — lepší agent coordination | P1 |
| 3 | Truncation boundary | Low-Med | High — ~60% token savings na resume | P1 |
| 4 | Confidence keywords | Low | Medium — lepší searchability | P2 |
| 2 | Post-it state | Medium | Medium — skill resumption | P2 |
| S1 | PROTECTED/ARCHIVABLE | Trivial | Low — nice-to-have | P3 |
| S3 | Compact ordering | Trivial | Low — safety net | P3 |
| S2 | Suggested next skill | Zero | — | Already done (handoffs:) |

### Doporučené pořadí implementace
1. **Call chain tracking** + **Truncation boundary** — paralelně, oba P1
2. **Confidence keywords** — po #1, rozšíření compact + checkpoint
3. **Post-it state** — po #2, vyžaduje více testování
4. **Section markers** + **Compact ordering** — kdykoliv, triviální

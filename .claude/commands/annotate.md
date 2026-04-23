---
name: annotate
description: Use when retrospectively reviewing a past session trace and marking decision points as good/bad to build an eval dataset. Trigger on 'annotate', 'anotuj trace', 'Align Eval', 'projít trace', 'review past session'. Do NOT use for in-session review (/critic), real-time correction (handled by correction-tracker hook), or writing learnings from session (/handoff, /scribe).
argument-hint: "[trace-file | --list | --last]"
discovery-keywords: [align eval, trace review, post-hoc review, human annotation, label trace, flag decision, označit chybu, projít session, zpětná revize]
tags: [review, session, memory]
phase: review
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
model: sonnet
effort: auto
maxTurns: 15
disallowedTools: Agent
---

# Annotate — Retrospective Trace Annotation (Align Evals)

Proactive post-hoc review of session traces. User navštíví konkrétní decision point v minulém trace a označí ho `good` / `bad` / `skip`. Bad annotations produkují eval cases v `.claude/evals/annotated/` → feed do `/self-evolve` a `/evolve` pro graduation.

**Chase context engineering pattern #4**: Align Evals = human annotation of traces. Reactive correction loop (correction-tracker.py) už existuje, annotate doplňuje **proactive** branch: user projde co už proběhlo.

## When to Use

- User chce projít včerejší session a označit kde agent chyboval
- Build eval dataset z produkčních trace (ne syntetic)
- Po incidentu: annotate trace kdy to selhalo → pinpoint root cause rozhodnutí
- Pravidelný retrospective review (weekly, měsíčně)

## When NOT to Use

- In-session real-time review → `/critic`
- Capturing a learning bez trace review → `/scribe`
- Capturing session findings bulk → `/handoff`
- Automated quality gate → `/eval` (grades, does not solicit human verdict)

<!-- CACHE_BOUNDARY -->

## Workflow

### Phase 0: Setup

Read `$ARGUMENTS`:
- `--list` → list recent traces, exit (informational mode)
- `--last` → pick most recent trace from `.traces/sessions/`
- `<filename>` or `<path>` → use that trace directly
- empty → list recent + ask user to pick

### Phase 1: List Recent Traces

```bash
ls -lt .traces/sessions/*.jsonl | head -10
```

Pro každý trace zobraz:
- Filename (date + session slug)
- Line count (≈ tool calls)
- First/last timestamp from JSONL
- Skills mentioned (grep `"skill":` a dedupe)

Pokud user nevybral, ask: "Který trace projdeme? (číslo 1-10, nebo `--last`)"

### Phase 2: Load + Summarize Trace

Read the chosen JSONL file. Parse each line as trace record.

Produce summary before annotation:
- Total tool calls
- Time span
- Tools breakdown (e.g., "Bash 12, Write 3, Edit 8")
- Error count (`exit != 0`)
- Skills invoked (from `skill:` field)

Ask: "Projdeme všech N záznamů, jen errors (M), nebo jen non-trivial (Write/Edit/Bash)? [all | err | write]"

### Phase 3: Interactive Annotation Loop

For each selected record, show compact view:

```
[seq N/total] 2026-04-21T02:15:33 Bash (exit=0)
  cmd: git status --short
  → verdict? [g=good | b=bad | s=skip | q=quit | ?=help]
```

Collect verdict. If `bad`, ask for short note (why bad? 1 věta).

**Rate limit**: pokud user prošel 20+ záznamů, ask "Pokračovat, nebo pauza?" — prevent annotation fatigue (quality drops).

### Phase 4: Write Annotations

Append each annotation to `.claude/memory/annotations.jsonl`:

```json
{"ts": "2026-04-23T14:22:01", "trace": "2026-04-21-0206.jsonl", "seq": 15, "tool": "Bash", "verdict": "bad", "note": "Should have grepped first, ran full recursive search without scope.", "user": "cetej"}
```

Format fields:
- `ts` — annotation timestamp (not trace record ts)
- `trace` — basename of source trace file
- `seq` — line number in trace (1-indexed)
- `tool` — tool name from record
- `verdict` — `good` | `bad` | `skip`
- `note` — user's reasoning (only for `bad`)
- `user` — git config `user.name` fallback to env USER

### Phase 5: Generate Eval Cases (for `bad` only)

For each `bad` annotation, create eval case matching existing `.claude/evals/` format (compatible with correction-tracker.py auto-generator):

**Location**: `.claude/evals/annotated/case-<NNN>/`

Kde `<NNN>` = next available number (scan existing, increment).

**Files**:

`input.md`:
```markdown
---
source: annotation
trace: <trace-filename>
trace_seq: <N>
annotated_by: <user>
annotated_at: <ISO-timestamp>
---

# Context

Record z trace:
- tool: <tool-name>
- input: <truncated tool input, max 500 chars>
- exit: <exit-code>

Předchozí 3 tool calls (pro context):
- <N-3> <tool>: <truncated>
- <N-2> <tool>: <truncated>
- <N-1> <tool>: <truncated>
```

`expected.md`:
```markdown
# Expected Behavior

Human annotation: **BAD**.

Note: <user's note>

Expected corrected behavior: <derive from note, or leave placeholder "TODO: derive from note">
```

`eval.md`:
```markdown
# Eval Criteria

- [ ] Output does NOT repeat the annotated mistake
- [ ] Behavior aligns with note: <user's note>
- [ ] No regression in related tool calls nearby
```

### Phase 6: Report

```
## Annotate Complete

Trace: <filename>
Annotations: <good_count> good, <bad_count> bad, <skip_count> skip
Eval cases generated: <N> (v .claude/evals/annotated/)
Annotations appended: .claude/memory/annotations.jsonl

Next: `/self-evolve` může trénovat proti těmto cases, `/evolve` může promovat
vzor jako learning při 2+ annotations se stejným vzorem.
```

## Integration Points

- **correction-tracker.py** (real-time): auto-generuje eval cases když user opraví
  v chatu 2+× stejný vzor. Annotate je post-hoc komplement.
- **/evolve**: čte `annotations.jsonl` při graduation — bad annotation vzor (2+ výskytů)
  boost pro graduation do `critical-patterns.md`.
- **/self-evolve**: čte `.claude/evals/annotated/` jako extra eval set.
- **/eval**: může konzumovat annotations jako baseline pro harness trace grading.

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "Annotate každý záznam aby byl dataset kompletní" | Annotation fatigue degraduje kvalitu verdictů — user po 30+ klesá na autopilot. | Default: jen errors + Write/Edit/Bash. Full coverage jen když user explicitně chce. |
| "Pro `bad` verdikt stačí krátká jednoslovná note" | Eval case potřebuje actionable expected behavior. "špatně" negeneruje trénovací signál. | Note musí obsahovat CO mělo být jinak, ne jen že bylo špatně. |
| "Annotate smí přepsat existující annotation (user si to rozmyslel)" | Anotace jsou audit trail pro trend analýzu — přepis maže evidenci změny názoru. | Append-only. Nová annotation na stejný seq = nový záznam s novým ts. |
| "Trace file může chybět, vytvořím placeholder" | Annotation bez source trace je neověřitelná. | Pokud trace neexistuje, abort s chybou "trace <path> not found — list traces via --list". |
| "Eval case pro bad verdict nepotřebuje context z okolí" | Izolovaný tool call nedává obraz rozhodnutí — decision je v kontextu předchozích kroků. | input.md vždy zahrnuje předchozí 3 tool calls (nebo méně pokud jsou na začátku trace). |

## Red Flags

STOP and re-evaluate if any of these occur:
- Annotating more than 30 records in one session (fatigue threshold)
- Every verdict in a stretch is same (`good` × 15 or `bad` × 10) — auto-pilot mode
- User's notes for `bad` verdicts all say variations of "nevím" / "špatně"
- Trace file < 5 records — too short to yield meaningful annotation pattern
- Running annotate on trace from same session that is still live (mixes in-session + post-hoc)

## Verification Checklist

- [ ] Trace file existuje a parsuje (každý řádek je validní JSON)
- [ ] `annotations.jsonl` obsahuje N řádků, kde N = good + bad + skip
- [ ] Každý `bad` verdict má odpovídající adresář v `.claude/evals/annotated/`
- [ ] Eval case adresář obsahuje všechny 3 soubory (input.md, expected.md, eval.md)
- [ ] Report final zobrazuje counts, path k annotations.jsonl, next-step doporučení

## Rules

1. **Append-only annotations** — nikdy nepřepisuj existující záznam, nová annotation = nový řádek
2. **Read before write** — pokud `annotations.jsonl` existuje, načti a zkontroluj duplicitní `(trace, seq)` pár; pokud existuje, warn user (duplicitní annotation)
3. **Bad vyžaduje note** — žádný prázdný note pro bad verdict; pokud user ignoruje, použij placeholder a flag ho v reportu jako "missing notes (N)"
4. **Sync s correction-tracker format** — eval case struktura (input.md/expected.md/eval.md) musí matchovat co auto-generuje correction-tracker.py (symmetric consumers)
5. **Czech user-facing, English technical** — prompt user česky, field names v JSONL anglicky (grep-friendly cross-project)
6. **Eval case numbering scan** — před vytvořením `case-NNN` scan existující adresáře, inkrementuj od max(existing) + 1

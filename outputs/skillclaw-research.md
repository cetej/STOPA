# SkillClaw — Research Brief + STOPA Implementation Proposal

**Date:** 2026-04-12
**Question:** Jak funguje SkillClaw evolver a co konkrétně implementovat v STOPA pro automatický krok "discovered pattern → skill edit"?
**Sources consulted:** 6 (GitHub README, arXiv:2604.08377, summarizer.py, aggregation.py, execution.py — vše read directly)
**Paper:** arXiv:2604.08377

---

## Executive Summary

SkillClaw je framework pro kolektivní evoluci skills z multi-user trajektorií [VERIFIED][1,2]. Klíčový mechanismus: 3-stagový pipeline (Summarize → Aggregate → Execute) běžící jako daemon každých 300 sekund [VERIFIED][1]. Pattern detection je plně LLM-based — žádné embeddingy, clustering, ani heuristiky [VERIFIED][3]. Evolver produkuje konkrétní SKILL.md diff přes 4 možné akce (improve/optimize/create/skip) s teplotou 0.4 pro konzervativní rozhodnutí [VERIFIED][4]. Quality gate funguje na behaviorální úrovni — kandidát se testuje na reálných podmínkách, jen zlepšení vstoupí do produkce [VERIFIED][2].

STOPA má všechny potřebné komponenty rozptýlené (session-trace, /discover, /evolve, /self-evolve), ale chybí uzavřená smyčka [INFERRED][5]. Kritické mezery: žádný `skill_referenced` tag v session traces, žádný automated pipeline trajectory→diff, žádný daemon trigger [VERIFIED][5].

Minimální implementace: 3 soubory (~300 řádků kódu) + 1 scheduled task + rozšíření `/evolve`. Nevyžaduje přepsání žádné stávající komponenty.

---

## Detailed Findings

### 1. SkillClaw Pipeline: Summarize → Aggregate → Execute

**Summarize (`summarizer.py`)** [VERIFIED][3]
- Input: raw session dict s turns (prompts, responses, tool calls, skill references)
- Vybuduje strukturovaný `_trajectory` text: step#, PRM score, skills invoked, tool calls (success/error), response snippet (max 400 chars)
- LLM prompt: 8-15 věta analytický souhrn — Goal, Key trajectory, Skill effectiveness, Critical turning points, Tool usage patterns, Outcome
- Output fields: `_trajectory`, `_summary`, `_skills_referenced`, `_avg_prm`, `_has_tool_errors`
- Běží paralelně přes `asyncio.gather()`

**Aggregate (`aggregation.py`)** [VERIFIED][3]
- Pouze organizační krok — `defaultdict(list)` keyed by skill name
- Sessions bez skill reference → `NO_SKILL_KEY` (kandidáti na nový skill)
- Žádná conflict resolution v této fázi

**Execute (`execution.py`)** [VERIFIED][4]
- LLM call: temperature=0.4, max 8192 tokens
- Input: current SKILL.md + session evidence (successes + failures odděleny)
- 4 možné akce:
  - `improve_skill` — targeted edits kde evidence ukazuje chybějící guidance
  - `optimize_description` — pouze přepis YAML `description:` pole
  - `create_skill` — recurring pattern patří do nového skillu
  - `skip` — skill funguje adekvátně nebo evidence je slabá
- Output JSON: `{action, rationale, skill: {name, description, content, edit_summary}}`
- `edit_summary` obsahuje: `preserved_sections`, `changed_sections`, `notes`

### 2. Trigger a Scheduling

- Daemon: `skillclaw-evolve-server --port 8787 --interval 300` [VERIFIED][1]
- Time-based, ne threshold-based — běží každých 5 minut bez ohledu na počet nových sessions
- Daytime/nighttime split (paper): sessions se hromadí přes den; batch validation přes noc v idle prostředí [VERIFIED][2]

### 3. Quality Gates

**Strukturální gate (execution.py)** [VERIFIED][4]:
- JSON schema check
- Non-empty name validation
- Name-collision: `create_skill` se stejným jménem → forced `improve_skill`

**Behaviorální gate (arXiv paper, Algorithm 1)** [VERIFIED][2]:
- Old + new skill run pod identickými podmínkami v idle environment
- LLM porovná task success + execution stability
- Accept/Reject → monotonic deployment (jen zlepšení vstoupí)

**Prompt-level safeguards** [VERIFIED][4]:
- "Do NOT rewrite the whole skill from scratch"
- "Treat CURRENT skill as source of truth, not rough draft"
- "If a successful session supports a section, leave it untouched unless failure evidence explicitly contradicts"
- "When in doubt, prefer skip"

### 4. STOPA Gap Analysis

| SkillClaw Component | STOPA Equivalent | Coverage |
|--------------------|------------------|----------|
| Session recording | `session-trace.py` | Partial — existuje ale skill_referenced chybí |
| Session summarization | `/discover` Phase 1-2 | Partial — manuální trigger |
| Pattern extraction | `/discover` Phase 3 | Partial — report, ne diff |
| Skill update decision | `/evolve` (corrections.jsonl) | Partial — corrections, ne trajectories |
| Skill file editing | `/self-evolve` (on-demand) | Partial — synthetic evals, ne real sessions |
| Knowledge synthesis | `/compile` (wiki) | Partial — learnings, ne skill diffs |
| Quality gate | `/self-evolve` eval loop | Partial — synthetic, ne real conditions |
| Version history | Git commits | Partial — žádné per-skill evidence files |
| Autonomous daemon | **CHYBÍ** | ❌ |
| Session → skill diff (auto) | **CHYBÍ** | ❌ |
| skill_referenced tagging | **CHYBÍ** | ❌ |

### 5. SkillClaw vs STOPA — Architekturální srovnání

```
SkillClaw (closed loop):
Sessions → Client Proxy → [summarize → aggregate → execute] → candidate → validate → deploy
           (continuous)    (daemon 300s, automatic)            (auto)       (real env) (auto)

STOPA (open loop):
Sessions → session-trace → /discover (manual) → report  
corrections.jsonl → /evolve (manual) → critical-patterns.md
SKILL.md → /self-evolve (manual, on-demand) → improved SKILL.md
```

Fundamentální mezera: každý krok v STOPA je manuálně triggerovaný. SkillClaw je plně uzavřená smyčka.

---

## Disagreements & Open Questions

- SkillClaw nemá execution-based regression testing (jen prompt safeguards + behavioral gate). STOPA's `/self-evolve` s eval cases je robustnější — vhodné hybridní řešení [INFERRED][4,5]
- `agent_evolve_server/` (autonomní agent varianta) nebyla plně prozkoumána — může nabízet flexibilnější přístup než fixed pipeline [UNVERIFIED][1]

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | SkillClaw README | https://github.com/AMAP-ML/SkillClaw | Dva daemon servery, 3-stage pipeline, interval 300s | Architecture | High |
| 2 | arXiv 2604.08377 | https://arxiv.org/abs/2604.08377 | Behavioral gate: candidate runs v idle env, monotonic deployment | Quality gate | High |
| 3 | summarizer.py | https://github.com/AMAP-ML/SkillClaw/blob/main/evolve_server/summarizer.py | LLM-based trajectory summarization, _skills_referenced field | Implementation | High |
| 4 | execution.py | https://github.com/AMAP-ML/SkillClaw/blob/main/evolve_server/execution.py | 4 actions, temp=0.4, edit_summary, prompt safeguards | Implementation | High |
| 5 | STOPA skills | local | /discover, /evolve, /self-evolve existují ale nejsou propojeny | Gap analysis | High (inferred) |

---

## Sources

1. SkillClaw GitHub README — https://github.com/AMAP-ML/SkillClaw
2. arXiv paper 2604.08377 — https://arxiv.org/abs/2604.08377
3. evolve_server/summarizer.py — https://github.com/AMAP-ML/SkillClaw/blob/main/evolve_server/summarizer.py
4. evolve_server/execution.py — https://github.com/AMAP-ML/SkillClaw/blob/main/evolve_server/execution.py
5. STOPA local skills — .claude/skills/discover/, evolve/, self-evolve/

---

## Coverage Status

- **[VERIFIED]:** Pipeline architektura, 4 akce, safeguards, daemon trigger, quality gate mechanismus
- **[INFERRED]:** STOPA gap analýza (z porovnání přečteného kódu), hybridní implementační doporučení
- **[SINGLE-SOURCE]:** Daytime/nighttime split (pouze z paperu, ne z kódu)
- **[UNVERIFIED]:** agent_evolve_server/ implementace, skill_registry.py konverzní logika

---

# STOPA Implementation Proposal: Auto-Evolve Pipeline

## Design Principle

Nevytvářej nový daemon. Použij existující scheduled tasks systém.
Nenahrazuj `/evolve` — rozšiř ho o `--candidates` mode.
Udržuj humans in the loop pro apply (ale ne pro discover + diff).

## Architektura: 3 nové komponenty

```
[SessionStart/End hook]     [Scheduled daily]           [Manual review]
session-trace.py            summarize-sessions.py        /evolve --candidates
  ↓ adds skill_referenced     ↓ reads traces                ↓ shows diffs, applies
                              evolve-skills.py              candidates/ → SKILL.md
                              ↓ produces candidates
                              .claude/memory/candidates/
```

## Komponenta 1: Hook změna — skill_referenced tagging

**Soubor:** `.claude/hooks/session-trace.py` (nebo nový `skill-tagger.py`)

Přidej do PreToolUse hook (SessionStart event nebo při každém Read SKILL.md):

```python
# V session-trace.py nebo skill-tagger.py
# Detekuje kdy Claude čte SKILL.md a taguje session

import re, json, os
from pathlib import Path

def tag_skill_reference(tool_name: str, tool_input: dict, session_id: str):
    """Zaznamenej referenci na skill v aktuální session."""
    if tool_name != "Read":
        return
    
    path = tool_input.get("file_path", "")
    # Match: .claude/skills/<name>/SKILL.md nebo .claude/commands/<name>.md  
    match = re.search(r'\.claude/(?:skills/(\w[\w-]*)/SKILL|commands/([\w-]+))\.md', path)
    if not match:
        return
    
    skill_name = match.group(1) or match.group(2)
    trace_dir = Path(".claude/memory/traces")
    trace_dir.mkdir(exist_ok=True)
    
    session_file = trace_dir / f"{session_id}.json"
    data = json.loads(session_file.read_text()) if session_file.exists() else {"skills_referenced": []}
    
    if skill_name not in data["skills_referenced"]:
        data["skills_referenced"].append(skill_name)
        session_file.write_text(json.dumps(data, indent=2))
```

**Kde přidat:** `settings.json` → hooks → PreToolUse s matcher na `Read`.

## Komponenta 2: `scripts/summarize-sessions.py`

Čte session traces + outcomes, produkuje strukturované summaries.

```python
#!/usr/bin/env python3
"""
Summarize recent STOPA sessions for skill evolution.
Reads from: .claude/memory/traces/, .claude/memory/outcomes/
Writes to: .claude/memory/summaries/
"""
import json, sys, asyncio
from pathlib import Path
from datetime import datetime, timedelta

TRACES_DIR = Path(".claude/memory/traces")
OUTCOMES_DIR = Path(".claude/memory/outcomes")  
SUMMARIES_DIR = Path(".claude/memory/summaries")
DAYS_BACK = 7  # zpracuj sessions z posledních N dní

def build_session_evidence(session_id: str) -> dict | None:
    """Sestaví session evidence ze session-trace + outcomes."""
    trace_file = TRACES_DIR / f"{session_id}.json"
    if not trace_file.exists():
        return None
    
    trace = json.loads(trace_file.read_text())
    skills = trace.get("skills_referenced", [])
    if not skills:
        return None  # Přeskočit sessions bez skill referencí
    
    # Najdi outcome pro tuto session
    outcome = None
    for f in OUTCOMES_DIR.glob(f"*{session_id[:8]}*.md"):
        outcome = f.read_text()
        break
    
    return {
        "session_id": session_id,
        "skills_referenced": skills,
        "outcome_text": outcome or "(no outcome recorded)",
        "date": trace.get("date", "unknown"),
    }

def summarize_with_llm(evidence_batch: list[dict]) -> str:
    """
    Volej Claude API pro LLM summarization.
    V STOPA kontextu: volej přes subprocess `claude -p` nebo přes API.
    
    Prompt template (mirror SkillClaw summarizer):
    - Goal: co session řešila
    - Skill effectiveness: jak skill pomohl nebo selhal  
    - Critical turning points: kde se rozhodlo
    - Outcome: success/partial/failure + proč
    """
    # TODO: implementovat přes claude API nebo subprocess
    # Pro MVP: vrátit strukturovaný dict bez LLM summarization
    return {
        "skills_referenced": evidence_batch[0]["skills_referenced"],
        "session_count": len(evidence_batch),
        "has_failures": any("failure" in e.get("outcome_text", "").lower() for e in evidence_batch),
        "raw_outcomes": [e["outcome_text"][:500] for e in evidence_batch],
    }

def main():
    SUMMARIES_DIR.mkdir(exist_ok=True)
    cutoff = datetime.now() - timedelta(days=DAYS_BACK)
    
    # Skupuj evidence podle skill
    skill_evidence: dict[str, list] = {}
    
    for trace_file in TRACES_DIR.glob("*.json"):
        evidence = build_session_evidence(trace_file.stem)
        if not evidence:
            continue
        for skill in evidence["skills_referenced"]:
            skill_evidence.setdefault(skill, []).append(evidence)
    
    # Zapíš summaries
    summary = {
        "generated": datetime.now().isoformat(),
        "skill_groups": {
            skill: {
                "session_count": len(sessions),
                "sessions": sessions,
            }
            for skill, sessions in skill_evidence.items()
        }
    }
    
    output_file = SUMMARIES_DIR / f"summary-{datetime.now().strftime('%Y-%m-%d')}.json"
    output_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"Summaries written to {output_file}")
    print(f"Skills covered: {list(skill_evidence.keys())}")

if __name__ == "__main__":
    main()
```

## Komponenta 3: `scripts/evolve-skills.py`

Hlavní evolver — čte summaries, produkuje kandidáty.

```python
#!/usr/bin/env python3
"""
Auto-evolve STOPA skills from session evidence.
Reads from: .claude/memory/summaries/
Writes to: .claude/memory/candidates/

Does NOT auto-apply — produces staged diffs for human review via /evolve --candidates
"""
import json, subprocess, sys
from pathlib import Path
from datetime import datetime

SUMMARIES_DIR = Path(".claude/memory/summaries")
CANDIDATES_DIR = Path(".claude/memory/candidates")
SKILLS_DIR = Path(".claude/skills")
COMMANDS_DIR = Path(".claude/commands")

EVOLVE_SYSTEM_PROMPT = """You are a skill evolution agent for a Claude Code orchestration system (STOPA).
You analyze session evidence and decide how to improve a skill file.

CONSERVATIVE EDITING RULES (non-negotiable):
1. Treat the CURRENT skill as source of truth, not a rough draft
2. Do NOT rewrite the whole skill from scratch  
3. If a successful session supports a section, leave it untouched
4. Separate agent errors from skill deficiencies before deciding
5. When in doubt, prefer 'skip' over a speculative edit
6. description: field MUST start with "Use when..." (STOPA convention)

OUTPUT: JSON with this schema:
{
  "action": "improve_skill" | "optimize_description" | "create_skill" | "skip",
  "rationale": "1-3 sentences explaining the decision",
  "skill": {
    "name": "skill-name",
    "description": "Use when...",
    "content": "full markdown body (no YAML frontmatter)",
    "edit_summary": {
      "preserved_sections": ["section names left intact"],
      "changed_sections": ["section names modified"],
      "notes": "what changed and why"
    }
  }
}
"""

def get_current_skill(skill_name: str) -> str | None:
    """Načti aktuální SKILL.md."""
    candidates = [
        SKILLS_DIR / skill_name / "SKILL.md",
        COMMANDS_DIR / f"{skill_name}.md",
    ]
    for path in candidates:
        if path.exists():
            return path.read_text(encoding="utf-8")
    return None

def call_claude(prompt: str) -> str:
    """Volej Claude přes subprocess (claude -p)."""
    result = subprocess.run(
        ["claude", "-p", "--model", "claude-sonnet-4-6", prompt],
        capture_output=True, text=True, encoding="utf-8"
    )
    return result.stdout

def evolve_skill(skill_name: str, evidence: dict) -> dict | None:
    """Produkuj kandidáta pro jeden skill."""
    current_skill = get_current_skill(skill_name)
    if not current_skill:
        return None  # Skill neexistuje — neprodukuj kandidáta
    
    session_evidence = json.dumps(evidence, indent=2, ensure_ascii=False)
    
    prompt = f"""{EVOLVE_SYSTEM_PROMPT}

## Current SKILL.md for '{skill_name}'

{current_skill}

## Session Evidence ({evidence['session_count']} sessions)

{session_evidence}

Decide: should this skill be improved based on this evidence?
Respond with valid JSON matching the schema above."""
    
    response = call_claude(prompt)
    
    # Parse JSON z odpovědi
    try:
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except (json.JSONDecodeError, AttributeError):
        pass
    return None

def main():
    CANDIDATES_DIR.mkdir(exist_ok=True)
    
    # Načti nejnovější summary
    summaries = sorted(SUMMARIES_DIR.glob("summary-*.json"), reverse=True)
    if not summaries:
        print("No summaries found. Run summarize-sessions.py first.")
        sys.exit(1)
    
    summary = json.loads(summaries[0].read_text())
    skill_groups = summary.get("skill_groups", {})
    
    print(f"Processing {len(skill_groups)} skill groups...")
    
    results = []
    for skill_name, evidence in skill_groups.items():
        print(f"  Evolving: {skill_name} ({evidence['session_count']} sessions)...")
        candidate = evolve_skill(skill_name, evidence)
        
        if not candidate:
            print(f"    → no candidate (parse error or skill not found)")
            continue
        
        action = candidate.get("action", "skip")
        print(f"    → action: {action}")
        
        if action == "skip":
            continue
        
        # Zapiš kandidáta
        candidate_file = CANDIDATES_DIR / f"{skill_name}-{datetime.now().strftime('%Y-%m-%d')}.json"
        candidate["meta"] = {
            "skill_name": skill_name,
            "generated": datetime.now().isoformat(),
            "session_count": evidence["session_count"],
            "source_summary": str(summaries[0]),
        }
        candidate_file.write_text(json.dumps(candidate, indent=2, ensure_ascii=False))
        results.append(f"{skill_name}: {action}")
    
    print(f"\n✓ Generated {len(results)} candidates:")
    for r in results:
        print(f"  {r}")
    print(f"\nReview with: /evolve --candidates")

if __name__ == "__main__":
    main()
```

## Komponenta 4: Scheduled Task

```python
# Spustit jednou v STOPA session:
mcp__scheduled-tasks__create_scheduled_task(
    taskId="auto-evolve-skills",
    description="Denní auto-evoluce skills ze session traces",
    cronExpression="0 3 * * *",  # 3:00 AM local time
    prompt="""Run the SkillClaw-inspired auto-evolve pipeline for STOPA skills:

1. cd to C:/Users/stock/Documents/000_NGM/STOPA
2. Run: python scripts/summarize-sessions.py
3. Run: python scripts/evolve-skills.py
4. If candidates were generated, send a Telegram notification: "Auto-evolve: N skill candidates ready. Review with /evolve --candidates"

Do NOT apply candidates automatically — only generate them for human review.
Report success/failure count."""
)
```

## Komponenta 5: `/evolve --candidates` mode

Přidej do `.claude/skills/evolve/SKILL.md` novou sekci:

```markdown
## Candidates Mode (--candidates)

When invoked with `--candidates` flag:

1. Read all files in `.claude/memory/candidates/*.json`
2. For each candidate, show:
   - Skill name + action (improve/optimize/create)
   - Rationale from LLM
   - edit_summary: preserved/changed sections
   - Diff: current SKILL.md vs proposed content
3. User decides: Accept / Skip / Edit
4. On Accept:
   - Write new SKILL.md (and commands/ copy)
   - Append version entry to `.claude/memory/skill-versions.md`:
     `| 2026-04-12 | skill-name | improve_skill | "what changed" | session-evidence-link |`
   - Move candidate file to `candidates/applied/`
5. Report: N accepted, M skipped
```

## Quality Gate (hybridní přístup)

Místo SkillClaw's expensive behavioral gate navrhuju:

1. **Strukturální gate** (auto, v evolve-skills.py): JSON schema, name collision
2. **Prompt safeguards** (kopie z SkillClaw): anti-rewrite, conservative default
3. **Human review** (místo automated behavioral test): `/evolve --candidates` ukazuje diff
4. **Post-apply verification** (lazily): `/critic` na nové SKILL.md po prvním reálném použití

Proč ne behavioral gate: STOPA nemá idle environment s real sessions. Syntetické evaly ze `/self-evolve` jsou dostupné ale přidávají latenci. Human review je rychlejší a spolehlivější pro single-user setup.

## Implementační Roadmap

| Krok | Soubor | Rozsah | Priorita |
|------|--------|--------|----------|
| 1 | `hooks/skill-tagger.py` | ~50 řádků | KRITICKÝ — bez tohoto nic nefunguje |
| 2 | `settings.json` hook registrace | 5 řádků | KRITICKÝ |
| 3 | `scripts/summarize-sessions.py` | ~80 řádků | HIGH |
| 4 | `scripts/evolve-skills.py` | ~120 řádků | HIGH |
| 5 | Scheduled task creation | 1 API call | MEDIUM |
| 6 | `/evolve --candidates` mode | ~30 řádků skill edit | MEDIUM |
| 7 | `skill-versions.md` tracking | template | LOW |

**MVP (krok 1+2+3+4):** Postačí k automatické detekci patterns a produkci kandidátů. Krok 5-7 přidávají pohodlí.

**Odhad práce:** 4-6 hodin implementace včetně testování na reálných session traces.

---

## What's Different from Simply Running /evolve More Often

`/evolve` operuje na `corrections.jsonl` — explicitních korekcích od uživatele. Auto-evolve operuje na session trajectories — implicitních signálech z toho jak skills skutečně fungují. Jsou to ortogonální signály:

- `/evolve`: "uživatel řekl že tohle je špatně" → promote do rules
- auto-evolve: "skill byl použit 15×, 3× vedl k failure, tady je pattern" → navrhni edit

Obojí je potřeba. Auto-evolve přidává signal z reálného použití, ne jen z explicitní zpětné vazby.

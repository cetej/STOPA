# Next Session Brief — STOPA Audit Follow-up

**Vytvořeno**: 2026-04-16
**Předchozí session commit**: `0a73793` chore: STOPA entropy sweep
**Stav**: 4 úkoly zbývají, rozděleno do 2 kategorií (autonomní vs vyžaduje přítomnost uživatele)

---

## Kontext — co předcházelo

Předchozí session (2026-04-16) provedla audit STOPA a vyčistila entropii:
- `/evolve #13` — bigmas graduated → core, improvement-queue cleaned
- Archived 157 session captures + smazán anomaly tree (hook CWD bug)
- Fixed `raw-capture.sh` — nyní používá `SCRIPT_DIR/PROJECT_ROOT` anchor
- Reaktivovány 3 feedback hooky (graduation-check, failure-recorder, impact-tracker) — dosud sirotci
- Partitioned `permission-log-archive.md` (13 066 řádků → 27 chunks)
- Archivovány 4 staré orphan hooky (slack-notify, suggest-compact, file-read-dedup, mid-session-extract)

Klíčový objev: **Feedback subsystém byl dokumentovaný v `rules/memory-files.md` ale neimplementovaný** — hooky napsané ale nezaregistrované. To vysvětluje proč `failures/` je prázdný a graduation gap byl 1.8%. Teď běží.

---

## Zbývající úkoly

### 1. Orphan hook triage (18 zbývajících) — AUTONOMNÍ

**Priorita**: STŘEDNÍ. Tyto hooky existují ale nejsou v settings.json. Některé mohou být cenné, některé dead.

**Kandidáti (fresh, ≤14 dní, pravděpodobně cenné):**
- `trigger-engine.py` (17KB, 5d) — skill-chaining orchestrator; `trigger-state.json` je prázdný `{}`
- `workspace_validator.py` (18KB, 4d) — zřejmě scope validator
- `hebbian-consolidate.py` (9KB, 12d) — memory consolidation (2BRAIN?)
- `stagnation-detector.py` (12KB, 8d) — druhý layer k panic-detector
- `auto-relate.py` (9KB, 11d) — concept-graph relation builder
- `mempalace-archive.py` (6KB, 4d) — memory palace archiving
- `model-perf-tracker.py` (5KB, 4d) — model performance tracking
- `skill-detector.py` (10KB, 13d) — skill discovery from context
- `learnings_retrieval.py` (16KB, 3d) — LIBRARY (importované, ne hook — nech)
- `brain-telegram-capture.py` (3KB, 3d) — Telegram integration
- `generation-tracker.py` (4KB, 10d) — nano/klip output tracking
- `build-permission-registry.py` (6KB, 12d) — permission audit
- `critic-accuracy-tracker.py` (2KB, 11d) — critic self-calibration
- `auto-checkpoint.py` (2KB, 11d) — auto-save checkpoint
- `auto-compound-agent.py` (6KB, 15d) — SCHEDULED (v task-completed.sh — OK)
- `autodream.py` (13KB, 1d) — SCHEDULED (dream cycle — OK)

**Postup pro každý hook:**
1. `head -30 <hook>` — co dělá, jaký event očekává
2. Grep kde je volán (import nebo scheduled task)
3. Rozhodnutí: REACTIVATE (add to settings.json) | KEEP_AS_LIB | ARCHIVE
4. Pro REACTIVATE: přidat s `if` filter do správného event array

**Začátek**: `ls -la .claude/hooks/*.py | grep -v -f <(python -c "import json,re; print('\n'.join(re.findall(r'([a-z_-]+\.py)', open('.claude/settings.json').read())))") | head`

---

### 2. /compile run + raw/ threshold úprava — AUTONOMNÍ

**Priorita**: STŘEDNÍ. Wiki fresh, ale:
- `.claude/memory/brain/raw/` má 16 fresh captures (2026-04-13 až 2026-04-16) nevsintetizováno do wiki
- `.claude/memory/raw/` má 222 session captures (threshold 15 v `evolve-trigger.sh` — bude trigger-spamm)

**Kroky:**
1. Spustit `/compile` — process 16 brain raw captures do wiki articles
2. Zvednout threshold v `.claude/hooks/evolve-trigger.sh` line 113 z `15` na `100` (session captures hromadí přirozeně, 15 je příliš nízko)
3. Zvážit scheduled task co automaticky archivuje session captures starší 3 dny (prevent accumulation)

---

### 3. 4 GitHub issues pro radar RED tools — VYŽADUJE UŽIVATELE (destruktivní externí akce)

**Priorita**: NÍZKÁ. Tohle je tech roadmap, ne entropy cleanup. Neovlivňuje stabilitu systému.

**Missing tools z `.claude/memory/radar.md` (nejsou v `improvement-log.md`):**

| Tool | Score | Repo | Proč |
|---|---|---|---|
| **OpenHarness** | 8/10 | HKUDS/OpenHarness | Přímý architectural mirror STOPA (10 subsystem design). **NEJVYŠŠÍ PRIORITA** — studie pro STOPA evolution |
| Claw Code | 9/10 | instructkr/claw-code | Open-source CC clone (Python+Rust), architecture study |
| GitHub Copilot SDK | 8/10 | github/copilot-sdk | Multi-provider orchestration, BYOK (Anthropic/OpenAI/Foundry) |
| Google Antigravity | 8/10 | antigravity.google | Multi-agent IDE, Windows preview (new 2026-04-16) |

**Příkaz pro vytvoření (po potvrzení):**
```bash
gh issue create --repo cetej/STOPA --title "Evaluate OpenHarness — architectural mirror for STOPA evolution" --body "..."
```

**Doporučení**: Vytvořit jen OpenHarness (nejvyšší unikátní hodnota), ostatní nechat v radaru.

---

### 4. verify-sweep.py extension — AUTONOMNÍ

**Priorita**: NÍZKÁ. Enforce nedodržovaná pravidla z `rules/skill-files.md`.

**Přidat do `.claude/hooks/verify-sweep.py`:**
1. Skill frontmatter check: `description:` začíná `"Use when..."` (18/47 violates)
2. Skill frontmatter check: `max-depth:` přítomno (45/47 chybí — violation core-invariant #8)

**Location**: přidat novou section po "3. Check critical-patterns.md" (~line 308).

```python
# 4. Check SKILL.md frontmatter conventions
skills_dir = Path(".claude/skills")
if skills_dir.exists():
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        try:
            content = skill_file.read_text(encoding="utf-8", errors="replace")
            meta = parse_yaml_frontmatter(content)

            # Rule: description must start with "Use when..."
            desc = meta.get("description", "")
            if desc and not desc.strip().startswith("Use when"):
                checked += 1
                failed += 1
                violations.append({
                    "timestamp": ts,
                    "source": f"skills/{skill_dir.name}/SKILL.md",
                    "label": f"description should start 'Use when...'",
                    "check": "description starts with 'Use when'",
                    "result": f"starts with: {desc[:50]}",
                })

            # Rule: max-depth required (core-invariant #8)
            if "max-depth" not in meta:
                checked += 1
                failed += 1
                violations.append({
                    "timestamp": ts,
                    "source": f"skills/{skill_dir.name}/SKILL.md",
                    "label": "missing max-depth (core-invariant #8)",
                    "check": "max-depth field present",
                    "result": "field missing",
                })
        except Exception:
            pass
```

Po přidání očekávej ~63 violations (18 desc + 45 max-depth). Buď všechny fixnout, nebo použít jako roadmap (suppress s `--warn-only` flag).

---

## Resume Prompt (zkopíruj na začátek další session)

```
Pokračuji v STOPA audit z 2026-04-16 (commit 0a73793). Přečti si
`.claude/memory/next-session-brief.md` a dokončuj úkoly v pořadí:

1. Orphan hook triage (18 zbývajících) — AUTONOMNÍ
2. /compile run + raw/ threshold fix — AUTONOMNÍ
3. verify-sweep.py extension (frontmatter checks) — AUTONOMNÍ
4. 4 GitHub issues (OpenHarness priority) — ČEKÁ NA MŮJ SOUHLAS

Začni bodem 1 (hook triage) — postupuj autonomně, reportuj po každé trojici hooků
rozhodnutí (REACTIVATE/KEEP/ARCHIVE) s důvodem. Circuit breaker: pokud narazíš na
hook který nechápeš, flagni ho jako UNCLEAR a přeskoč.
```

---

## Relevantní soubory

**Memory**:
- `.claude/memory/evolution-log.md` — historie /evolve runs (13 záznamů)
- `.claude/memory/improvement-queue.md` — 5 annotated violations
- `.claude/memory/learnings/2026-04-16-hook-cwd-anchor-pattern.md` — dnešní learning
- `.claude/memory/permission-log-archive.md.bak` — safety net, smazat po 2026-04-23

**Rules**:
- `.claude/rules/memory-files.md` — definice HERA/outcomes/replay-queue subsystémů
- `.claude/rules/skill-files.md` — frontmatter konvence pro verify-sweep extension
- `.claude/rules/core-invariants.md` — core rules (memory limit 500, max-depth default 1)

**Hooks**:
- `.claude/hooks/raw-capture.sh` — fixed CWD bug, template pro ostatní bash hooks
- `.claude/hooks/verify-sweep.py` — k rozšíření v bodě 4
- `.claude/hooks/archive/` — nově vytvořený dir, 4 stubs přesunuty tam

**Settings**:
- `.claude/settings.json` — 33 active hooks (bylo 30)

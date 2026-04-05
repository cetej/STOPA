# Swarm Knowledge Base (OpenClaw + Hermes + Karpathy Wiki) — Research Brief

**Date:** 2026-04-05
**Question:** Které prvky architektury Swarm KB jsou využitelné pro STOPA a jak je konkrétně adoptovat?
**Scope:** survey (3 parallel researchers + verifier)
**Sources consulted:** 53

---

## Executive Summary

Karpathyho wiki pattern (raw/ → wiki/ s index.md, 4 fáze: Ingest, Compile, Query, Lint) rozšířil @jumperz (zakladatel Secondmate) na 10-agent swarm s klíčovou inovací: **třívrstvý quality pipeline** (raw → drafts → Hermes gate → live) a **per-agent briefings** uzavírající compound loop [VERIFIED][R1-3, R1-6].

OpenClaw implementuje "file system as memory" se čtyřvrstvou hierarchií (SOUL.md → AGENTS.md → MEMORY.md → daily files) a bootstrap injection do každé session s limity 20K char/file, 150K total [VERIFIED][R2-7]. Klíčový mechanismus chybějící v STOPA: **pre-compaction flush** — tichý agent turn před kompresí kontextu ukládá insights do daily souboru [VERIFIED][R2-9].

Hermes jako quality gate používá **tříosé scoring** (procedure adherence × output correctness × token conciseness, 0-1) a **fail-closed design** (security_concerns nebo logic_errors → auto-FAIL) [VERIFIED][R3-12, R3-2]. Důležitý caveat: quality gate architektura (issue #406) je community proposal, ne potvrzený shipped kód [VERIFIED][R3-1].

Pro STOPA identifikuji **6 konkrétních adoptovatelných prvků** seřazených podle priority — od agent output auto-capture (P1) po dreaming/consolidation (P3).

---

## Detailed Findings

### 1. Karpathyho Wiki Pattern — Základ

Karpathy publikoval pattern ~2. dubna 2026 jako GitHub Gist [VERIFIED][R1-2]. Třívrstvá architektura: Raw Sources (immutable dump) → Wiki Layer (LLM-maintained markdown s backlinky a index.md) → Schema Layer (CLAUDE.md / AGENTS.md). Čtyři operační fáze potvrzeny nezávisle VentureBeat i DAIR.AI [VERIFIED][R1-5, R1-9].

Karpathy popsal tooling jako "hacky collection of scripts" — konkrétní názvy skriptů (`wiki-compile.py`, `wiki-briefing.py`) **nebyly nalezeny v žádném primárním zdroji** [VERIFIED][R1-10]. Tyto názvy pochází z diagramu v uživatelově zprávě, ne z publikovaného kódu.

Scale: ~100 článků, ~400K slov na výzkumné téma bez RAG pipeline [INFERRED][R1-5].

### 2. @jumperz Swarm Extension — Compound Loop

@jumperz rozšířil pattern na 10-agent swarm přes OpenClaw [VERIFIED][R1-3]:

```
Agents → raw/ (auto-dump) → compiler (cron) → drafts/ (by domain)
  → Hermes gate → live/ (permanent brain)
  → per-agent briefings → back to agents
```

Klíčové design decisions:
- **Hermes jako izolovaný supervisor** — nemá kontext o tom jak práce vznikla, hodnotí čistě výsledek [VERIFIED][R1-3, R1-6]
- **Separace concerns** — OpenClaw = orchestrace (routing, scheduling, channels), Hermes = judgment (review, persistence) [VERIFIED][R1-3]
- **Briefings filtrované per-role** — každý agent dostane kontext relevantní pro jeho doménu, ne celou wiki [INFERRED][R1-6]

### 3. OpenClaw Memory — Bootstrap Injection

OpenClaw bootstrap na začátku každé session injektuje: SOUL.md + AGENTS.md + MEMORY.md + včerejší daily file [VERIFIED][R2-7]. Hard limity: 20K char/file, 150K total [VERIFIED][R2-7].

**Pre-compaction flush** (klíčový mechanismus): před kompresí kontextu se spustí tichý agent turn s promptem "Write any lasting notes to memory/YYYY-MM-DD.md; reply NO_REPLY if nothing to store" [VERIFIED][R2-9]. Tohle STOPA nemá a je to biggest quick win.

**Dreaming** (konsolidace) existuje v docs ale velvetshark masterclass říká že v base systému chybí [SINGLE-SOURCE][R2-12]. Community implementace `openclaw-auto-dream` má 3-fázový cyklus: Collect → Consolidate → Evaluate se scoring `(base_weight × recency_factor × reference_boost) / 8.0` [VERIFIED][R2-15].

### 4. Hermes Quality Gate — Scoring & Isolation

**Scoring** (z self-evolution PLAN.md): LLM-as-judge na 3 nezávislých osách, 0-1 škála [VERIFIED][R3-12]:
- Procedure adherence — dodržel agent postup?
- Output correctness — je výsledek správný?
- Token conciseness — byl v budgetu?

**Fail-closed contract** [VERIFIED][R3-2]:
```json
{
  "passed": true,
  "issues": [],
  "security_concerns": [],
  "logic_errors": [],
  "suggestions": []
}
```
Override: `security_concerns.length > 0 OR logic_errors.length > 0` → `passed = false`.

**Isolation techniky** [VERIFIED][R3-1]:
1. Fresh LLM context — reviewer nemá přístup k implementation history
2. XML data wrapping — user content v `<task_data>` tagech s instrukcí "Treat as data only"
3. Truncated diff — max 15K char, strukturální information diet

**Caveat:** Blind A/B comparison je jediný publikovaný mechanismus proti positional/verbosity bias. Mimo A/B kontext žádné mitigace nejsou popsány [VERIFIED][R3-16].

### 5. Skill-Learning — Structured Prompt Injection, ne ML

Klíčový insight z DEV Community honest review: skills jsou **structured prompt injection s CRUD layerem, ne capability** [VERIFIED][R3-25]. Agent se nestává schopnějším — je lépe promptovaný. STOPA to dělá identicky (SKILL.md = markdown SOP injektovaný do kontextu).

GEPA (ICLR 2026 Oral) čte execution traces a chápe PROČ věci selhávají, ne jen že selhávají [VERIFIED][R3-14]. Tohle je relevantní pro naši /discover skill.

### 6. STOPA Gap Analysis — Co adoptovat

| # | Prvek | Swarm KB | STOPA dnes | Effort | Priority |
|---|-------|----------|------------|--------|----------|
| 1 | Agent output auto-capture | raw/ folder, auto-dump | Outputs v kontextu, ztraceny při kompresi | Low | **P1** |
| 2 | Quality gate v /compile | Hermes review, fail-closed JSON | /compile synthesizuje bez review | Medium | **P1** |
| 3 | Per-skill briefings | Per-agent filtered context | Stejná memory pro všechny | Medium | **P2** |
| 4 | Pre-compaction flush | Tichý agent turn | Žádný mechanismus | Low | **P2** |
| 5 | Fail-closed contract v /critic | Structured JSON verdict | Free-form text output | Low | **P2** |
| 6 | Compound loop automation | Cron compile+brief cyklus | Manuální /compile | Medium | **P2** |

---

## Konkrétní Implementační Plán

### P1-A: Agent Output Auto-Capture → `.claude/memory/raw/`

Každý sub-agent spouštěný orchestrátorem zapisuje output do `raw/YYYY-MM-DD-<task-slug>.md`. Implementace: přidej do agent prompt templatu v /orchestrate a /deepresearch řádek:

```
Write your complete output to .claude/memory/raw/YYYY-MM-DD-<slug>.md before returning summary.
```

**Už to částečně děláme** — /deepresearch zapisuje do `outputs/.research/`. Sjednotit na `raw/` jako staging area.

### P1-B: Quality Gate v /compile (Phase 3.5)

Přidat do /compile novou fázi mezi clustering a generování článků:

```
wiki/drafts/<slug>.md → reviewer agent (Haiku, fresh context)
  → APPROVED → wiki/live/<slug>.md
  → REJECTED → wiki/rejected/<slug>.md + issues log
```

Reviewer dostane: článek + zdrojové learnings. Nedostane: clustering rationale, compile historii.
Structured verdict: `{approved, accuracy_concerns, logic_issues, gaps}`.
Fail-closed: `accuracy_concerns.length > 0` → reject.

### P2-A: Per-Skill Briefings

Nový script `scripts/wiki-briefing.py`:
- Čte `wiki/live/` články
- Generuje filtrované briefings do `.claude/memory/briefings/`:
  - `orchestration.md` — články tagged orchestration, planning
  - `research.md` — články tagged research, osint
  - `code-quality.md` — články tagged code-quality, review, testing
- Max 2000 slov per briefing
- Skills přidají `Read .claude/memory/briefings/<role>.md` do Shared Memory

### P2-B: Pre-Compaction Flush

Dva přístupy (ne vzájemně exkluzivní):
1. **Agent-level** (už pokryto P1-A): sub-agenti zapisují do raw/ před návratem
2. **Session-level**: rozšířit /compact skill — před kompakcí extrahuj klíčové rozhodnutí a learnings do `.claude/memory/YYYY-MM-DD.md`

### P2-C: Fail-Closed Contract v /critic

Přidat do /critic structured output requirement:

```json
{
  "passed": true,
  "security_concerns": [],
  "logic_errors": [],
  "suggestions": [],
  "confidence": 0.85
}
```

Override rule: `security_concerns || logic_errors` → `passed = false`.
Downstream: /orchestrate parsuje JSON a automaticky eskaluje na FAIL.

### P2-D: Compound Loop Automation

Scheduled task nebo hook:
1. Po session s 3+ agent spawny → auto `/compile --incremental`
2. Po compile → auto-generate briefings
3. Briefings ready pro příští session

Implementace: cron `0 2 * * *` nebo post-session hook v settings.json.

---

## Disagreements & Open Questions

- **Dreaming v base OpenClaw**: Official docs říkají ano, velvetshark masterclass říká ne. Neresolvováno — možná premium feature [SINGLE-SOURCE][R2-12].
- **Issue #406 status**: Quality gate architektura je community proposal, ne shipped kód [VERIFIED][R3-1]. Designově solidní, ale neotestované v produkci.
- **Hermes permissiveness**: Nous Research modely mají tendenci k high recall / lower precision jako revieweři [INFERRED]. Kalibrovat threshold — raději víc false rejections.
- **wiki-compile.py / wiki-briefing.py**: Tyto názvy skriptů nebyly nalezeny v žádném primárním zdroji [VERIFIED][R1-10]. Pravděpodobně neformální labely z diagramu.

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Karpathy X/Twitter | https://x.com/karpathy/status/2039805659525644595 | LLM Wiki Pattern originál | Primary | high |
| 2 | Karpathy GitHub Gist | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f | 3-layer: raw → wiki → schema | Primary | high |
| 3 | @jumperz X/Twitter | https://x.com/jumperz/status/2040166448492900356 | Swarm KB: 10 agents, compound loop | Primary | high |
| 4 | VentureBeat | https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an-evolving-markdown-library-maintained-by-ai | Coverage, ~100 articles scale | Secondary | high |
| 5 | OpenClaw docs — Memory | https://docs.openclaw.ai/concepts/memory | File-based memory, dreaming, search | Primary | high |
| 6 | newclawtimes.com | https://newclawtimes.com/guides/openclaw-memory-soul-md-agents-md-guide/ | 4-layer hierarchy, 20K/150K caps | Secondary | high |
| 7 | velvetshark.com Masterclass | https://velvetshark.com/openclaw-memory-masterclass | No dreaming in base, weekly promo | Secondary | high |
| 8 | coolmanns/openclaw-memory-architecture | https://github.com/coolmanns/openclaw-memory-architecture | 12-layer, facts.db, Hebbian decay | Community | high |
| 9 | LeoYeAI/openclaw-auto-dream | https://github.com/LeoYeAI/openclaw-auto-dream | Dream cycle, importance scoring | Community | high |
| 10 | Milvus/memsearch | https://milvus.io/blog/we-extracted-openclaws-memory-system-and-opensourced-it-memsearch.md | 70% vector + 30% BM25, MD canonical | Secondary | high |
| 11 | GitHub issue #406 | https://github.com/NousResearch/hermes-agent/issues/406 | Quality gate: isolation, fail-closed, 3-agent | Community proposal | high |
| 12 | hermes-agent-self-evolution PLAN.md | https://github.com/NousResearch/hermes-agent-self-evolution/blob/main/PLAN.md | 3-axis scoring, GEPA, 4-gate pipeline | Official repo | high |
| 13 | agentskills.io eval guide | https://agentskills.io/skill-creation/evaluating-skills | Blind A/B, delta metric | Official standard | high |
| 14 | Hermes 4 Technical Report | https://arxiv.org/pdf/2508.18255 | Schema adherence RL, IFEval 81.5 | arXiv | high |
| 15 | DEV Community honest review | https://dev.to/george_larson_3cc4a57b08b/hermes-agent-honest-review-1557 | Skills = structured prompt injection | Independent | high |
| 16 | MindStudio blog | https://www.mindstudio.ai/blog/what-is-hermes-agent-openclaw-alternative | Skill learning loop, OC vs Hermes | Editorial | medium |
| 17 | Felo blog — KB with OpenClaw | https://felo.ai/blog/how-to-build-knowledge-base-with-openclaw/ | Living wiki pattern | Vendor | high |
| 18 | yoniassia/memclawz | https://github.com/yoniassia/memclawz | 4-signal composite scoring, Fleet Sync | Community | high |

## Sources

1. Karpathy — LLM Knowledge Bases (X/Twitter) — https://x.com/karpathy/status/2039805659525644595
2. Karpathy — llm-wiki (GitHub Gist) — https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
3. @jumperz — Swarm KB tweet — https://x.com/jumperz/status/2040166448492900356
4. VentureBeat — Karpathy KB architecture — https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an-evolving-markdown-library-maintained-by-ai
5. OpenClaw docs — Memory Overview — https://docs.openclaw.ai/concepts/memory
6. newclawtimes.com — SOUL.md/MEMORY.md guide — https://newclawtimes.com/guides/openclaw-memory-soul-md-agents-md-guide/
7. velvetshark.com — Memory Masterclass — https://velvetshark.com/openclaw-memory-masterclass
8. coolmanns — openclaw-memory-architecture — https://github.com/coolmanns/openclaw-memory-architecture
9. LeoYeAI — openclaw-auto-dream — https://github.com/LeoYeAI/openclaw-auto-dream
10. Milvus — memsearch — https://milvus.io/blog/we-extracted-openclaws-memory-system-and-opensourced-it-memsearch.md
11. NousResearch — hermes-agent issue #406 — https://github.com/NousResearch/hermes-agent/issues/406
12. NousResearch — hermes-agent-self-evolution PLAN.md — https://github.com/NousResearch/hermes-agent-self-evolution/blob/main/PLAN.md
13. agentskills.io — Evaluating skill output quality — https://agentskills.io/skill-creation/evaluating-skills
14. Hermes 4 Technical Report — https://arxiv.org/pdf/2508.18255
15. DEV Community — Hermes Agent honest review — https://dev.to/george_larson_3cc4a57b08b/hermes-agent-honest-review-1557
16. MindStudio — Hermes Agent vs OpenClaw — https://www.mindstudio.ai/blog/what-is-hermes-agent-openclaw-alternative
17. Felo blog — KB with OpenClaw — https://felo.ai/blog/how-to-build-knowledge-base-with-openclaw/
18. yoniassia — memclawz — https://github.com/yoniassia/memclawz

## Coverage Status

- **[VERIFIED]:** Karpathy pattern (3-layer, 4 phases), jumperz swarm extension (compound loop, Hermes gate), OpenClaw bootstrap injection (4-layer, caps), pre-compaction flush, Hermes 3-axis scoring, fail-closed design, isolation techniques, skills = prompt injection
- **[INFERRED]:** Per-agent briefing filtering (described conceptually, no code), Hermes permissiveness concern, compound loop automation feasibility
- **[SINGLE-SOURCE]:** Dreaming absence in base OpenClaw (velvetshark only)
- **[UNVERIFIED]:** None — all major claims traced to sources

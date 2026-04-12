---
date: 2026-04-05
type: architecture
severity: medium
component: hook
tags: [security, orchestration, memory]
summary: "LlamaFirewall PromptGuard (BERT, 19-92ms, pip install) je ADOPT pro tool output scanning; AlignmentCheck (860ms+, Together API) je WATCH; CaMeL plná impl je SKIP (research artifact), ale capability tagging vzor je ADOPT jako STOPA konvence; TaskShield nemá veřejnou impl."
source: external_research
confidence: 0.8
uses: 1
harmful_uses: 0
verify_check: "Grep('llamafirewall', path='.claude/memory/learnings/') → 1+ matches"
origin: web_fetch
successful_uses: 0
---

# Agent Defense Frameworks — Research Verdicts (2026-04-05)

## LlamaFirewall (Meta)

| Komponenta | Verdikt | Latence | Závislosti |
|------------|---------|---------|------------|
| **PromptGuard 2** | **ADOPT** | 19-92ms | `pip install llamafirewall`, BERT model (22M/86M), local |
| **CodeShield** | **ADOPT** | ~70ms | Semgrep + regex, local, 50+ CWE patterns |
| **AlignmentCheck** | **WATCH** | 860-1490ms | Together API + Llama 4 Maverick, příliš pomalé pro sync hook |

**Integrace PromptGuard do STOPA:**
PromptGuard může běžet jako Python library volání v PostToolUse hooku.
Detekuje prompt injection v tool outputs s AUC 0.98, Recall@1%FPR 97.5%.
Kombinace PG+AC dosahuje ASR 1.75%.

**Akce:**
1. `pip install llamafirewall` + `llamafirewall configure` (stáhne HF modely)
2. Přidat do content-sanitizer.py jako fallback layer za regex patterns
3. AlignmentCheck: zvážit jako async audit (ne sync hook) při podezřelém chování

**Why:** PromptGuard je BERT classifier — rychlý, lokální, nezávislý na Claude/Llama.
Regex patterny v content-sanitizer.py pokrývají známé vzory; PromptGuard přidá ML-based
detekci pro zero-day injection patterns.

## CaMeL (DeepMind)

| Aspekt | Detail |
|--------|--------|
| Repo | `google-research/camel-prompt-injection` — existuje, uv-only, research artifact |
| Plná impl | **SKIP** — dual-LLM infrastruktura, nestabilní, nelze pip install |
| Vzor | **ADOPT** — capability tagging jako STOPA memory konvence |

**Použitelný CaMeL vzor pro STOPA (bez závislostí):**
- Tag tool outputs jako `[UNTRUSTED]` v state.md
- PreToolUse hook: blokovat přímé použití untrusted dat v privilegovaných tools
- Orchestrate: agent zpracovávající external data nesmí generovat přímé příkazy

**Akce:** Přidat `[UNTRUSTED]` tagging konvenci do orchestrate/scout skills.
Žádná nová závislost — jen prompt pattern.

## TaskShield

**SKIP** — žádný veřejný kód, žádný repo. Koncept (fuzzy scoring instrukce vs user task)
implementovatelný jako prompt pattern v /critic nebo /verify — žádné závislosti.

## Prioritizovaný implementation backlog

| # | Akce | Effort | Závislost |
|---|------|--------|-----------|
| 1 | PromptGuard do content-sanitizer.py | MED | pip install llamafirewall (~1GB model) |
| 2 | [UNTRUSTED] tagging konvence v orchestrate | LOW | žádná |
| 3 | CodeShield do security-scan.py | LOW | pip install llamafirewall |
| 4 | AlignmentCheck async audit | HIGH | Together API key + Llama model |

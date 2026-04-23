---
date: 2026-04-23
type: architecture
severity: critical
component: general
tags: [security, fetch, browse, ingest, injection, steganography, monitor]
summary: "Google DeepMind (Franklin et al., SSRN 03/2026) mapuje 6 attack vector kategorií na AI agenty. Content Injection 86% úspěch, Cognitive State (RAG poisoning) 80%+, Behavioural Control 58-93%. 'Can't sanitize a pixel' — LSB steganography je invisible ale extractable. STOPA /fetch, /browse, /deepresearch, /ingest, MONITOR OSINT mají žádný security layer."
source: external_research
uses: 0
harmful_uses: 0
successful_uses: 0
confidence: 0.9
maturity: draft
verify_check: "manual"
related: []
---

## Context

Franklin et al., Google DeepMind (SSRN March 2026) publikovali první systematický framework attack surface pro AI agenty. 6 kategorií:
1. **Content Injection** (86% úspěch) — hidden HTML/CSS, CSS-hidden text, JavaScript comments
2. **Semantic Manipulation** — subtle prompt reframing skrz context manipulation
3. **Cognitive State** (80%+ RAG poisoning) — corrupting retrieval sources
4. **Behavioural Control** (58-93%) — tool invocation hijacking
5. **Systemic** — supply chain, dependency injection
6. **Human-in-the-Loop** — social engineering při approval steps

Klíčové empirické nálezy:
- Overall injections → **29% output alteration**
- Steganography (LSB v obrázcích) → vizuálně invisible, programmatically extractable
- Dynamic cloaking — web servery detect AI agenta → servírují malicious verzi

**"Can't sanitize a pixel"** — LSB steganography nejde obrannou normalizací odstranit bez destroy image.

## STOPA Exposure

Skills s žádnou security vrstvou:
- `/fetch` — Jina Reader fetchuje external content
- `/browse` — Chrome MCP + computer-use, potenciálně renderuje malicious HTML
- `/deepresearch` — multi-source evidence aggregation = RAG poisoning target
- `/ingest` — raw source → knowledge, entity extraction, wiki/entities/
- `learning-admission.py` hook — mohl by check injected instructions v zapisovaných learnings

**Cross-project highest exposure:**
- **MONITOR** (OSINT, external content scraping)
- **NG-ROBOT** (content pipeline, external sources)

## Action (immediate + deferred)

**STOPA immediate (XS effort):**
1. Tento soubor jako critical learning — tag tags=[security, fetch, browse, ingest] pro grep-first retrieval
2. Případně rozšířit `/fetch` + `/browse` skills o "security-aware" note v description

**Cross-project (M effort):**
1. `/improve` → **MONITOR**: GitHub issue "Input sanitization layer per DeepMind 6-vector framework"
   - Priority 1: HTML comments + CSS-hidden text (86% attack vector, easy detection)
   - Priority 2: RAG source integrity (pre-ingestion validation)
   - Steganography detection deferred (complex, heavy GPU)
2. `/improve` → **NG-ROBOT**: same sanitization layer před článek ingestion
3. Upgrade `learning-admission.py` hook: check injected instructions (match patterns: "ignore previous", "reveal system prompt", "new instructions:")

## Rationale

Major lab (DeepMind), systematický framework, empirické success rates. Není hype — je to threat model. STOPA má dnes **zero security layer** nad external content. Gradual defense starting s nejlevnějšími vectors (hidden HTML/CSS) dává immediate coverage proti 86% vector.

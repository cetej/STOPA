# Second Brain

**Type:** concept
**Tags:** pkm, architecture, knowledge-management
**Related:** [[context-engineering]], [[compiler-analogy]], [[karpathy]]

---

Architektonický vzor pro osobní knowledge management augmentovaný LLM. Spojuje tři tradice:

## Tři pilíře

### 1. Karpathyho LLM Wiki (2026)
Raw sources → LLM compiler → structured markdown wiki. Tři vrstvy: raw/ (neměnný archiv), wiki/ (kompilovaný artefakt), schema (konfigurace). Bypasuje RAG při ~100-500 zdrojích díky index-first retrieval a explicitním backlinkům.

### 2. Building a Second Brain — CODE (Forte, 2022)
Capture → Organize → Distill → Express. PARA metoda (Projects/Areas/Resources/Archive) organizuje podle actionability. Progressive Summarization: highlight → bold → executive summary — bez mazání zdroje. Resonance heuristic: ukládej co rezonuje intuitivně.

### 3. Zettelkasten (Luhmann, 1960s)
Atomicity: jedna myšlenka per note, unique ID. Connectivity: explicitní linky; search nestačí. Tags > categories. Luhmann: 90K notes za 40 let. Optimalizuje pro emergence znalostí v čase.

## BASB vs Zettelkasten

Komplementární: PARA optimalizuje project completion, Zettelkasten knowledge emergence. Kombinace: PARA pro aktivní práci, atomické notes pro long-term knowledge graph.

## Akademická validace

- **EcphoryRAG** (2025): entity-centric storage, 94% token reduction
- **Cognitive Workspace** (2025): active metacognitive curation, 58.6% reuse vs 0% passive RAG
- **PersonalAI** (2025): temporal hyper-edges pro sledování kdy se belief mění

## 2BRAIN implementace

6C cyklus: Capture → Compile → Connect → Curate → Consult → Contemplate. Žije v `.claude/memory/brain/` jako rozšíření STOPA.

## Zdroje

- Karpathy LLM Wiki Gist
- Forte — BASB Overview (fortelabs.com)
- Zettelkasten.de — Overview
- EcphoryRAG (arXiv:2510.08958)
- Cognitive Workspace (arXiv:2508.13171)

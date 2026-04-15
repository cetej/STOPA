# Artifacts as Memory Beyond the Agent Boundary

**Zdroj:** Martin et al., arXiv:2604.08756 (2026-04-13)
**Typ:** Formální teorie + empirická validace

---

## Jádro

Environmentální artefakty — pozorování, která garantují minulé události — fungují jako **external memory** pro RL agenty. Agent s přístupem k artefaktům potřebuje méně interní kapacity (vah, parametrů, kontextového okna) pro ekvivalentní výkon.

**Artifact Reduction Theorem:** Historie obsahující ≥1 artefakt lze zkrátit o ≥1 pozorování při zachování mutual information s budoucností. Jinými slovy: artefakt komprimuje historii, protože jeho přítomnost *implikuje* minulé události.

## Empirické výsledky

Linear Q-learning s 16 vahami + optimal path artefakt = výkon 64-vahového agenta bez artefaktů. Redukce 4× v interní kapacitě.

Klíčový finding: agenti **spontánně generují traces** (dynamic paths), které pak sami využívají pro navigaci. Toto emergentní chování nevyžaduje explicitní design — vzniká z běžného učení.

## Tři kritéria genuine external memory

1. **Survival-relevant** — prokazatelně zlepšuje výkon
2. **Mutable** — informace lze zapsat a modifikovat
3. **Selection-based** — relevance určena implicitně přes credit assignment

## Implikace pro STOPA a agent systémy

| Paper koncept | STOPA implementace |
|---|---|
| Spatial path (artefakt) | `state.md`, `checkpoint.md`, `decisions.md` |
| Internal capacity | Context window, model reasoning budget |
| Artifact reduction | Menší kontext potřebný s dobrými memory soubory |
| Dynamic path (self-generated traces) | Post-it pattern, skill intermediate state |
| Emergent memory bez designu | Agenti zapisující do `learnings/` bez explicitní instrukce |

**Designový princip: "Artifacts first, scale second"** — optimalizuj artefakty v prostředí (memory soubory, checkpoint, knowledge graph) před škálováním modelu nebo kontextového okna. Paper formálně dokazuje, že strukturované prostředí substituuje interní kapacitu.

Toto validuje STOPA architekturu: `checkpoint.md` je artefakt umožňující session continuity bez potřeby celé konverzační historie; `knowledge-graph.json` je artefakt redukující retrieval nároky; `post-it pattern` je dynamic path generovaný a konzumovaný týmž agentem.

## Limity

- Formalizace omezena na pozorování s absolutní jistotou (ne probabilistické)
- Definice pokrývá jednotlivé minulé pozorování, ne bohatší temporální struktury
- Testováno na 2D navigaci — transfer na LLM agenty je analogie, ne přímý důkaz

---

**Related:**
- [[agent-memory-taxonomy]] — Write-Manage-Read loop jako formalizace memory operací nad artefakty
- [[memfactory]] — RL-based management artefaktů (extract/update/retrieve)
- [[context-engineering]] — artefakty = kontextový scaffolding
- [[active-metacognitive-curation]] — rozhodování co udržovat v artefaktech
- [[second-brain]] — celý second brain = soustava artefaktů pro cognitive offloading
- STOPA `memory-files.md` — pravidla pro tvorbu a údržbu artefaktů

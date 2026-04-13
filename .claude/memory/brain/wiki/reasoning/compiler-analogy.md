# Compiler Analogy

**Type:** reasoning
**Tags:** mental-model, architecture, llm
**Related:** [[context-engineering]], [[second-brain]], [[karpathy]]

---

Mentální model od Karpathyho pro pochopení jak LLM transformuje surové znalosti do strukturované wiki.

## Mapování

| Software | Knowledge |
|----------|-----------|
| Source code | Raw články, papery, poznámky, webové stránky |
| Compiler | LLM |
| Compiled binary | Wiki (syntézovaný, navigovatelný artefakt) |
| Linker | Cross-reference a backlink systém |
| Build system | Ingest workflow (capture → compile → index) |
| Linter | Maintenance/lint průchod (kontradikce, osiřelé stránky) |

## Proč je to silný model

1. **Compiled once, kept current** — znalost se nekompiluje znovu při každém dotazu (na rozdíl od RAG)
2. **Lossy compression** — LLM prioritizuje užitečnost nad věrností zdroji. Raw zůstává k dispozici pro audit.
3. **Incremental builds** — nový zdroj dotýká 10-15 existujících wiki stránek, ne všechno
4. **4-pass transformation**: Extraction → Synthesis → Structure → Refinement

## Kdy použít

- Při vysvětlování proč 2BRAIN funguje (raw → wiki → query)
- Při rozhodování co patří do raw/ vs wiki/ (surový zdroj vs kompilovaný výstup)
- Při designování ingest pipeline (= build systém)

## Kdy NEPOUŽÍVAT

- Kompilace je jednosměrná. Znalosti jsou bidirectional — wiki může generovat nové otázky zpět do raw.
- Software binaries jsou deterministické. Wiki compilation je lossy a subjektivní.

## Zdroje

- Karpathy LLM Wiki Gist
- MindStudio — Compiler Analogy Breakdown

# Provenance: Proč naive RAG selhává na agregačních dotazech

**Datum:** 2026-04-05
**Otázka:** Proč naive RAG selhává na multi-document/agregačních dotazech a jak to řeší symbolické vrstvy?
**Scale:** survey
**Rounds:** 4 parallel research + 1 verification
**Sources:** 35+ konzultováno / 28 přijato / 5+ zamítnuto (neverifikovatelné nebo nefrelvantní)
**Verification:** partial (9 VERIFIED, 1 MISMATCH opraveno, 1 WEAK opraveno, 1 UNRESOLVED)

## Research Files

| Soubor | Agent | Účel |
|--------|-------|------|
| outputs/.research/rag-failure-modes-research-1.md | researcher-1 | Failure modes a benchmark evidence |
| outputs/.research/rag-symbolic-research-2.md | researcher-2 | Symbolické/strukturované vrstvy |
| outputs/.research/rag-multidoc-sota-research-3.md | researcher-3 | SOTA přístupy 2024-2025 |
| outputs/.research/rag-frameworks-research-4.md | researcher-4 | Produkční frameworky |
| outputs/.research/rag-synthesis.md | lead | Merged evidence + consensus/gaps |
| outputs/.research/rag-verification.md | verifier | Citation audit (top 12 claims) |

## Opravené chyby (z verifikace)

1. **Weakest Link Law**: Původní popis "4.8-11.5% accuracy drop" invertoval směr — šlo o accuracy recovery z intervence. Opraveno na neutrální popis recognition bottlenecku.
2. **OLLA**: Původní popis "SQL SELECT/WHERE/GROUP BY" byl nepřesný. OLLA nepoužívá SQL syntaxi — jde o semantic stratified sampling s SQL-like sémantikou. Opraveno.
3. **DSPy 39.3% EM**: Označeno [UNVERIFIED] — číslo existuje v PDF paperu ale URL na dspy.ai tutoriály vrací 404, abstract neobsahuje toto číslo.

## Uncertainty Summary

| Marker | Count |
|--------|-------|
| [VERIFIED] | 20 |
| [INFERRED] | 4 |
| [SINGLE-SOURCE] | 2 |
| [UNVERIFIED] | 2 |

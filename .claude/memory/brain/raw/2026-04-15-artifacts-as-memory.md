---
date: 2026-04-15
source_type: url
source_url: https://arxiv.org/pdf/2604.08756
---

# Artifacts as Memory Beyond the Agent Boundary

**Authors:** John D. Martin, Fraser Mince, Esra'a Saleh, Amy Pajak
**Affiliations:** Openmind Research Institute, University of Alberta, Cohere Labs, Université de Montréal, Mila, UPenn
**Published:** 2026-04-13

## Abstract
Formalizace environmentálních artefaktů jako external memory pro RL agenty. Artifact = pozorování garantující minulou událost. Theorem 1 (Artifact Reduction): artefakty snižují informační nároky na historii. Experimentálně: linear Q-learning s 16 vahami + artefakty = 64 vah bez artefaktů. Agenti spontánně generují traces (dynamic paths) které pak využívají — emergentní external memory bez explicitního designu.

## Key Definitions
- **Artifact (Def 1):** Pozorování jehož výskyt garantuje s jistotou konkrétní minulou událost
- **Artifact Reduction (Theorem 1):** Historie s ≥1 artefaktem lze redukovat o ≥1 pozorování při zachování ekvivalentní mutual information s budoucností
- **Externalizes Memory (Def 3):** Agent externalizuje memory když ekvivalentní výkon vyžaduje méně interní kapacity v artifactual vs artifactless prostředí

## Experiments
- 2D navigace, agenti hledají cíl s různými artefakty (optimal/suboptimal/random path, landmarks, dynamic path)
- Linear Q-learning: 16-576 vah; DQN: různé architektury
- 16 vah s optimal path = 64 vah bez path (48 weight reduction)
- Dynamic path: agenti spontánně generují traces → emergent memory

## Criteria for Genuine External Memory
1. Survival-relevant (zlepšuje výkon)
2. Mutable (informace lze enkódovat/modifikovat)
3. Selection-based (learning algoritmy implicitně určují relevanci)

## Implications
- Computational sufficiency může překračovat performance requirements
- Agenti mohou dosáhnout kompetence bez škálování interních zdrojů pokud prostředí scaffolduje
- "Artifacts first, scale second"

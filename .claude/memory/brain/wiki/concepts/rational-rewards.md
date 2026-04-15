# RationalRewards — Reasoning Reward Model

**Source:** arXiv:2604.11626
**Added:** 2026-04-15

## Core Idea

Reward model, který místo skalárního čísla produkuje strukturovanou kritiku ve 4 dimenzích — a teprve z ní odvozuje skóre. Kritika funguje jako inductive bias: brání reward hackingu a vytváří interpretovatelný feedback pro RL i test-time refinement.

## PARROT Framework (Preference-Anchored Rationalization)

Tréninková metoda, kde rationales = latentní proměnné optimalizované přes Evidence Lower Bound (ELBO):

1. **Teacher generuje rationale** zakotvené v known preference labels (který obrázek je lepší a proč)
2. **Consistency filtering** — ponechá jen rationale, které predikují preferenci i BEZ labelu (filtruje post-hoc racionalizace)
3. **Student distilace** — natrénuje reward model produkovat rationale bez preference labelu

Výsledek: 10-20× méně trénovacích dat než skalární reward baselines.

## 4 Dimenze hodnocení

| Dimenze | Co měří |
|---------|---------|
| Text faithfulness | Soulad s textovým promptem |
| Image faithfulness | Soulad s referenčním obrázkem (u editace) |
| Physical/visual quality | Realistické osvětlení, anatomie, artefakty |
| Text rendering | Kvalita textu v obrázku (pokud je přítomen) |

## Dual-Space Optimization

Model škáluje dvěma komplementárními cestami:

- **Parameter space** (trénink): multi-dimenzionální skóry jako strukturovaný RL feedback → fine-tuning generátoru
- **Prompt space** (inference): Generate→Critique→Refine loop překládá kritiku na cílené revize promptu bez update vah

Test-time prompt refinement loop matches/exceeds RL-based fine-tuning na několika benchmarcích. 8B model dosahuje competitive accuracy s Gemini-2.5-Pro na preference prediction.

## Proč to funguje

Structured reasoning funguje jako inductive bias — brání reward hackingu (model nemůže exploitovat skalární číslo, protože musí vysvětlit proč). Zároveň odemyká latentní capability existujících generátorů, které suboptimální prompty nevyužijí.

## Connections

- Related: [[rlvr]] — PARROT je reward model pro vizuální domény, RLVR je broader RL paradigma
- Related: [[reinforced-reasoning]] — PRM step-level verification je analogický princip (structured > scalar)
- Applied-in: STOPA `/critic` (multi-dim hodnocení), `/autoreason` (Generate→Critique→Refine loop), `/prompt-evolve` (test-time prompt refinement)
- Enables: `/nano` a `/klip` by mohly adoptovat dual-space vzor (RL training + test-time refinement)

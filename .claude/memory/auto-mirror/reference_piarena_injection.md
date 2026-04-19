---
name: PIArena — prompt injection evaluation platform
description: arXiv:2604.08499 (ACL 2026) — adaptive attack 86% ASR vs best defense; task-alignment = undetectable injection; validates STOPA's untrusted-content approach
type: reference
---

**Paper:** arXiv:2604.08499 (ACL 2026) — Geng et al.
**Code:** github.com/sleeepeer/PIArena

Unifikovaná platforma pro hodnocení prompt injection útoků a obran. 1700 vzorků, 13 datasetů, 3 typy útoků (direct, combined, strategy), 9 obran (4 prevention, 5 detection).

**Strategy-Based Adaptive Attack (2 fáze):**
1. Candidate Generation: Attacker LLM přepíše injekci 10 strategiemi (Author's Note, System Update...)
2. Refinement: feedback-driven rewriting (stealth/imperativeness/general optimization)
- 99% ASR bez obrany, **86% ASR proti PISanitizer** (nejlepší prevence)

**Defense tradeoff:**
| Obrana | Utilita | Strategy ASR | Komentář |
|---|---|---|---|
| PISanitizer | 99% | 86% | nejlepší utilita, slabá vs adaptivní |
| SecAlign++ | 45-84% | 21% | nejsilnější obrana, ale ničí utilitu |
| PIGuard | 72% | 79% | dobrá utilita, slabá obrana |

**Closed-source modely:** Claude Sonnet 4.5 = **31% ASR** (nejodolnější), GPT-5 = 70%, GPT-4o-mini (robustness-trained) = 76%, Gemini 3 Pro = 83%.

**Task-Alignment problém (fundamentální limit):**
Když se cíl injekce shoduje s typem úkolu (dezinfo v RAG, falešné info v QA), VŠECHNY obrany selhávají (44-82% ASR). Instrukční detekce nestačí — útok je sémanticky neodlišitelný. Potřeba content-level verifikace, ne instrukční filtrů.

**Why:** Validuje STOPA přístup (external content = untrusted, vždy user confirmation). Task-alignment je konkrétní gap kde ani robustness training nepomáhá.
**How to apply:** Při security-review nebo prompt defense designu: task-alignment = neřešitelný problém pro instrukční detekci. Claude je nejodolnější z komerčních modelů, ale stále 31% ASR.

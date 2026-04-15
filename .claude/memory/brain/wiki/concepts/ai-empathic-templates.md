# AI Empathic Templates — Structural Detection of LLM Text

**Source:** arXiv:2604.08479 (Gueorguieva et al., 2026)
**Added:** 2026-04-15

## Core Idea

LLM odpovědi na emocionální situace sledují jednu vysoce konzistentní šablonu — 83-90% AI odpovědí matchuje jeden regex pattern, zatímco u lidí pouze 6.4%. Lidi hodnotí AI empatii vysoko, ale mechanismus je úzký a předvídatelný. Struktura (sekvence taktik) je silnější detection signál než slovník.

## 10 Empathic Tactics Taxonomy

1. **Emotional Expression** — komunikace empatizerových pocitů
2. **Empowerment** — pozitivní tvrzení o charakteru seekera
3. **Validation** — normalizace pocitů
4. **Information** — fakta, zdroje, data
5. **Paraphrasing** — přeformulování co seeker řekl
6. **Reappraisal** — kognitivní reframing
7. **Self-Disclosure** — sdílení vlastní zkušenosti
8. **Advice** — návrhy řešení
9. **Assistance** — nabídka přímé pomoci
10. **Questioning** — kladení otázek

## Template Pattern

```
[Emotional Expression?] → Paraphrase↔Validation → [Empowerment?] → Advice↔Paraphrase → [Validation/Reappraisal?]
```

- GPT-4 Turbo: paraphrasing 100%, validation 90%, advice 96%
- Self-disclosure: AI 0% vs lidi 17%
- Questioning: AI 6% vs lidi frequently

## Proč je to důležité

- **Detection**: struktura sekvence taktik je spolehlivější signál než jednotlivá slova — potvrzuje princip "struktura = #1 detection signál, ne slovník"
- **Homogenizace**: pokud lidi internalizují AI vzory, ztrácí se diverzita empatického vyjádření
- **Context insensitivity**: stejný template bez ohledu na situaci — AI neadaptuje taktiky
- **Absence otázek**: AI radí místo aby se ptalo — chybí explorativní fáze

## Praktické implikace

| Problém | Řešení |
|---------|--------|
| Šablonová sekvence validate→advice→validate | Variovat pořadí taktik, přerušovat pattern |
| Self-disclosure = 0% | Přidat kontextuální sdílení (v rámci role) |
| Questioning = 6% | Klást otázky PŘED radou — explorativní fáze |
| Context insensitivity | Adaptovat mix taktik podle situace |

## Connections

- Related: [[jagged-intelligence]] — šablona je projev "ghost-like" chování: plynulá ale mechanická
- Validates: STOPA behavioral-genome.md Writing Quality — "variuj délku vět a odstavců (struktura = #1 detection signál)"
- Applied-in: STOPA `/autoreason` (penalizovat šablonové sekvence), `/critic` (variovat taktiky v outputu)
- Related: [[context-engineering]] — structured critique (RationalRewards) vs structured empathy — obojí jsou naučené šablony, ale s opačným hodnocením

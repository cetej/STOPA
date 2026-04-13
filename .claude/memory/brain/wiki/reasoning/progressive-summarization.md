# Progressive Summarization

**Type:** reasoning
**Tags:** pkm, methodology, distillation, mental-model
**Related:** [[basb-code]], [[para-method]], [[compiler-analogy]]
**Source:** Tiago Forte — Building a Second Brain

---

Technika distilace znalostí ve vrstvách — bez ztráty originálu.

## Vrstvy

```
Layer 0: Originální text (uložen v raw/)
Layer 1: Highlighted passages (tučné klíčové věty)
Layer 2: Bold highlights (nejdůležitější z highlighted)
Layer 3: Executive summary (2-3 věty vlastními slovy)
```

Každá vrstva je progressivně kratší. Čtenář si vybírá hloubku:
- Rychlý scan → Layer 3 (executive summary)
- Střední hloubka → Layer 2 (bold highlights)
- Full context → Layer 0 (originál v raw/)

## Proč to funguje

1. **Nikdy nemažeš** — originál zůstává, jen přidáváš vrstvy
2. **Distilace je inkrementální** — nemusíš udělat executive summary hned, můžeš jen highlightnout
3. **Retrieval-friendly** — Layer 3 stačí pro 80% dotazů, Layer 0 pro deep dive

## Vztah ke compiler analogy

| Progressive Summarization | Compiler |
|--------------------------|----------|
| Layer 0 (originál) | Source code (raw/) |
| Layer 1-2 (highlights) | Intermediate representation |
| Layer 3 (summary) | Compiled binary (wiki/) |

Karpathyho LLM Wiki dělá totéž, ale automaticky: LLM kompiluje raw/ do wiki/ = Layer 3. Raw zůstává pro audit.

## Implementace v 2BRAIN

- **raw/** = Layer 0 (originální zdroj)
- **wiki/ článek** = Layer 3 (LLM-compiled summary s cross-references)
- **Mezivrstvy** zatím neimplementovány — budoucí vylepšení: highlight metadata v YAML

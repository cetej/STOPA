# Vibe Coding

**Type:** concept
**Tags:** ai, programming, software-development, democratization
**Related:** [[karpathy]], [[verifiability]], [[context-engineering]]
**Updated:** 2026-04-13

---

Vibe coding = programování v přirozeném jazyce bez přímého psaní kódu. Termín vytvořil Andrej Karpathy v tweetu (2025).

## Podstata

"Programování je najednou dostupné každému přes angličtinu."

- Vývojář popisuje záměr → LLM generuje kód → vývojář testuje/iteruje
- Kód je "zdarma, pomíjivý, tvárný, použitelný jen jednou"
- Není nutné rozumět kódu, který systém generuje

## Asymetrický přínos

Vibe coding prospívá **normálním lidem více než profesionálům**:
- Profesionálové: mírné zrychlení stávající práce
- Non-vývojáři: přístup k doméně, která byla dříve uzavřená

Toto je součást širšího vzoru LLM technologické difuze směrem od jednotlivců dolů (viz [[power-to-people]]).

## Příklady (Karpathy vlastní projekty)

- **MenuGen**: foto menu → LLM generuje obrázky položek → https://www.menugen.app/
  - 100% kód psán Cursor+Claude
  - Karpathy: "basically don't really know how MenuGen works"
  - Deployovaná aplikace s auth a platbami
- llm-council: víceagentní debatní systém
- reader3: osobní čtecí aplikace
- Vlastní BPE tokenizer v Rustu
- HN Time Capsule: https://karpathy.ai/hncapsule/

## Proč je to paradigmatická změna

Kód přestál být vzácným zdrojem. Bottleneck se přesouvá od *psaní kódu* k *definování záměru a ověřování výsledku*.

Analogie: Software 1.0 = specifikovatelné → Software 2.0 = trénovatelné → Software 3.0 = prompt-popsatelné

## Rizika

- Kód generovaný LLM může být správný syntakticky, ale špatný sémanticky
- "Základní opisy opisu" — nižší kvalita bez porozumění
- Security issues v kódu, kterému vývojář nerozumí

## Zdroj

Karpathy: blog posts + tweets (2025), "2025 LLM Year in Review"

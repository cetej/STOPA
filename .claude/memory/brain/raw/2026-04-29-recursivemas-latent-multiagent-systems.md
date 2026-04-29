---
title: RecursiveMAS: Rekurzivní multi-agentní systémy s latentní komunikací
url: http://arxiv.org/abs/2604.25917v1
date: 2026-04-29
concepts: ["rekurzivní jazykové modely", "multi-agentní systémy", "latentní komunikace", "gradient-based co-optimization", "iterativní rafinace"]
entities: ["Xiyuan Yang", "James Zou", "Markus J. Buehler", "Cornell University"]
source: brain-ingest-local
---

# RecursiveMAS: Rekurzivní multi-agentní systémy s latentní komunikací

**URL**: http://arxiv.org/abs/2604.25917v1

## Key Idea

RecursiveMAS rozšiřuje princip rekurzivního škálování z jednotlivých jazykových modelů na multi-agentní systémy, kde agenti spolupracují v iterativních cyklech prostřednictvím latentních stavů místo textové komunikace, což zrychluje inferenci 1.2×-2.4× a snižuje spotřebu tokenů o 35-76%.

## Claims

- RecursiveMAS dosahuje průměrného zlepšení přesnosti o 8.3% oproti pokročilým single/multi-agent baseline systémům
- Framework zajišťuje 1.2×-2.4× zrychlení end-to-end inference při snížení spotřeby tokenů o 34.6%-75.6%
- RecursiveMAS je teoreticky efektivnější než standardní textově-založené MAS a udržuje stabilní gradienty během rekurzivního tréninku
- Systém podporuje 4 reprezentativní vzory agentní spolupráce a byl úspěšně testován na 9 benchmarcích zahrnujících matematiku, vědu, medicínu, vyhledávání a generování kódu

## Relevance for STOPA

RecursiveMAS představuje nový přístup k orchestraci agentů založený na latentní komunikaci místo textové, což může inspirovat efektivnější architektury pro STOPA zejména v oblasti snížení komunikační režie a iterativní kooperace mezi agenty.

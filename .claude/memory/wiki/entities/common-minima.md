---
name: Common Minima
type: concept
first_seen: 2026-04-13
last_updated: 2026-04-13
sources: [nexus-common-minima-generalization]
tags: [optimization, generalization, loss-landscape, pretraining]
---

# Common Minima

> Oblast v loss landscape kde task-specific minimizery všech pretraining zdrojů jsou geometricky blízko konvergovanému parametru — na rozdíl od "Sum of Minima" kde celkový loss je nízký ale individual minima jsou daleko.

## Key Facts

- Dva typy minimerů při stejném pretraining lossu: "Sum of Minima" (distant) vs "Intersection of Minima" (close) — zásadně odlišná downstream generalizace (ref: sources/nexus-common-minima-generalization.md)
- Formální důkaz (Theorem 2.2): downstream error proporcionální task variance sigma^2_B — menší variance = lepší generalizace (ref: sources/nexus-common-minima-generalization.md)
- "Closeness" (vzdálenost minim) je second-order generalization bias — ortogonální k "flatness" (studovaná v SAM literature) (ref: sources/nexus-common-minima-generalization.md)
- Gradient cosine similarity je horní mez closeness — optimalizovatelný proxy (ref: sources/nexus-common-minima-generalization.md)

## Relevance to STOPA

Princip "stejný agregátní výkon, různá downstream kvalita" je přenositelný na skill evaluation v STOPA. Dva skills mohou mít stejný critic score na training taskách, ale zásadně odlišný výkon na nových/OOD úlohách. Evaluace by měla zahrnovat OOD/generalizační testy, ne jen in-distribution metriky.

## Mentioned In

- [Nexus: Common Minima Generalization](../sources/nexus-common-minima-generalization.md)

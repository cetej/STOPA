---
name: Thinking ON leakuje artefakty, thinking OFF sumarizuje
description: Sonnet 4.6 s adaptive thinking leakuje XML/CoT do výstupu. S disabled thinking sumarizuje místo reprodukce. Řešení = PATCH formát + strip.
type: feedback
---

Sonnet 4.6 (od ~2026-03-31) se chová jinak při reprodukci dlouhých textů:
- `thinking: disabled` → model sumarizuje místo reprodukce (35-42% délky)
- `thinking: adaptive` → model leakuje `<antml*>`, `<thinking>`, chain-of-thought do output textu

**Why:** API aktualizace změnila chování bez varování. Model vnímá reprodukci jako low-value a zkracuje.

**How to apply:**
1. NIKDY nespoléhej na model pro reprodukci celého textu (30K+). Požaduj PATCH/diff, aplikuj programaticky.
2. Vždy stripuj `<antml*>`, `<thinking>`, `<antThinking>` z API výstupu (obranná vrstva).
3. EFFORT parametr nemá efekt při `thinking: disabled` — posílá se jen s adaptive thinking.
4. Před batch zpracováním testuj API změny na 1 článku. Spálený kredit na 6+ neúspěšných pokusech je drahý.
5. Po restartu serveru fronta ze starého kódu běží dál — utni staré procesy pořádně.
6. **Delimiter extraction (2026-04-02):** `split_article_and_notes()` v core.py odděluje reasoning od článku STRUKTURÁLNĚ — markery `===ČLÁNEK===`/`===KONEC===` + fallback detekce preamble. Notes jdou do `logs/N_phase_notes.md`, NIKDY do `article.md`. Regex stripping (sanitize_article_text) zůstává jako defence-in-depth.

# AI Tool Prompting Reference

Extrahováno z [nidhinjs/prompt-master](https://github.com/nidhinjs/prompt-master) (v1.5.0, MIT licence).
Kompaktní reference — co funguje na kterém modelu/nástroji.

---

## LLM modely

| Model | Klíčové pravidlo | Tipy |
|-------|-----------------|------|
| **Claude 4.x** | Explicitní a specifický — Claude bere instrukce doslova | XML tagy pro složité prompty (`<context>`, `<task>`). Opus over-engineers → přidat "Only make changes directly requested." |
| **GPT-5.x / ChatGPT** | Nejmenší prompt, který splní cíl | Silný v long-context syntéze a tone adherence. Omezit verbose: "Respond in under 150 words. No preamble." |
| **o3 / o4-mini** | NIKDY CoT — reasoning modely myslí interně | Krátké čisté instrukce. System prompt pod 200 slov. Zero-shot first. |
| **Gemini 2.x / 3 Pro** | Silný v long-context, ale halucinuje citace | Přidat: "Cite only sources you are certain of. If uncertain, say [uncertain]." |
| **Qwen 2.5** | Výborný instruction following, JSON output | Kratší focused prompty > dlouhé komplexní. Jasný system prompt s rolí. |
| **Qwen 3 (thinking)** | Thinking mode = jako o3, non-thinking = jako Qwen 2.5 | V thinking mode žádný CoT, žádný scaffolding. |
| **DeepSeek-R1** | Reasoning-native jako o3 | Přidat "Output only the final answer, no reasoning." pokud nechceš `<think>` tagy. |
| **Llama / Mistral** | Kratší prompty, jednoduchá flat struktura | Slabší instruction following — být explicitnější než u Claude/GPT. |
| **MiniMax M2.7** | OpenAI-kompatibilní API, 1M context | Temperature musí být 0–1 (ne víc). Může generovat `<think>` tagy. |

### Reasoning modely — univerzální pravidlo

> **o3, o4-mini, DeepSeek-R1, Qwen3 thinking**: NIKDY nepřidávat "think step by step", CoT, nebo reasoning scaffolding. Tyto modely myslí interně — CoT aktivně degraduje výstup.

---

## Coding AI

| Nástroj | Formát promptu | Kritické |
|---------|---------------|----------|
| **Claude Code** | Starting state + target state + allowed/forbidden actions + stop conditions | Stop conditions POVINNÉ (runaway loops). Scope na konkrétní soubory. |
| **Cursor / Windsurf** | File path + function name + current → desired behavior + do-not-touch list | "Done when:" je povinné. Rozdělit složité tasky na sekvenční prompty. |
| **GitHub Copilot** | Přesný function signature + docstring + edge cases | Copilot doplňuje predikci, ne záměr — žádná ambiguita v komentáři. |
| **Devin / SWE-agent** | Explicitní starting + target state, forbidden actions list | Scope filesystem: "Only work within /src." |
| **Antigravity** | Task-based — popisovat výsledky, ne kroky | Verifikace: "verify UI at 375px and 1440px using the browser agent" |

---

## Full-stack generátory

| Nástroj | Specifika |
|---------|-----------|
| **Bolt** | Explicitně rozlišit frontend vs backend vs database části |
| **v0** | Vercel-native — specifikovat pokud nechceš Next.js |
| **Lovable** | Design-forward popisy — zahrnout vizuální/UX záměr |
| **Figma Make** | Referencovat Figma component names přímo |
| **Google Stitch** | Popisovat interface goal, ne implementaci. "Match Material Design 3." |

> Všechny: Přidat "Do not add authentication, dark mode, or features not explicitly listed" proti feature bloat.

---

## Image AI

| Nástroj | Syntax | Tipy |
|---------|--------|------|
| **Midjourney** | Comma-separated descriptors, ne próza. Subject → style → mood → lighting. Params na konci: `--ar 16:9 --v 6 --style raw` | Negative: `--no [unwanted]` |
| **DALL-E 3** | Próza OK. Popisovat foreground/midground/background zvlášť | Přidat "do not include text in the image unless specified" |
| **Stable Diffusion** | `(word:weight)` syntax. CFG 7-12 | Negative prompt POVINNÝ. Steps: 20-30 draft, 40-50 final |
| **SeeDream** | Specifikovat art style explicitně (anime, cinematic, painterly) před scene content | Negative prompt doporučen |
| **ComfyUI** | Node-based — vždy dva bloky: Positive Prompt + Negative Prompt | Zeptat se na checkpoint model |

---

## Video AI

| Nástroj | Přístup |
|---------|---------|
| **Sora** | Režírovat jako filmový záběr. Camera movement je kritický (static vs dolly vs crane). |
| **Runway Gen-3** | Reaguje na cinematic language — referencovat filmové styly. |
| **Kling** | Silný v realistickém lidském pohybu — popsat body movement explicitně, shot type. |
| **LTX Video** | Prompt-sensitive, stručné vizuální popisy. Specifikovat resolution a motion intensity. |
| **Dream Machine (Luma)** | Cinematic quality — referencovat lighting setups, lens types, color grading. |

---

## Voice AI (ElevenLabs)

- Specifikovat emotion, pacing, emphasis markers, speech rate přímo
- SSML-like markers pro důraz: které slova zdůraznit, kde pauza
- Próza popisy nefungují — specifikovat parametry přímo

---

## Workflow AI (Zapier, Make, n8n)

- Formát: Trigger app + event → Action app + action + field mapping
- Auth requirements explicitně: "assumes [app] is already connected"
- Multi-step: číslovat kroky, specifikovat co se předává mezi nimi

---

## Browser / Computer-Use agenti

Perplexity Comet, OpenAI Atlas, Claude in Chrome, OpenClaw:
- Popisovat výsledek, ne navigační kroky
- Specifikovat constraints explicitně — agent rozhoduje sám
- Permission boundaries: "Do not make any purchase. Research only."
- Stop condition pro nevratné akce: "Ask before submitting any form"

---

## Univerzální anti-patterny

Techniky které **nefungují** v single-prompt execution (vyžadují external orchestration):

| Technika | Proč nefunguje v jednom promptu |
|----------|---------------------------------|
| Mixture of Experts | Model role-playuje persony z jednoho forward pass, žádný real routing |
| Tree of Thought | Model generuje lineární text a simuluje branching |
| Graph of Thought | Vyžaduje externí graph engine |
| Universal Self-Consistency | Vyžaduje nezávislé sampling — pozdější cesty kontaminují dřívější |
| Prompt chaining (layered) | Tlačí modely do fabrikace na delších řetězcích |

---

## Diagnostic checklist (zkrácený)

Před odesláním promptu zkontroluj:

1. **Task** — vágní sloveso? → nahradit přesnou operací
2. **Format** — chybí output format? → přidat explicitní format lock
3. **Scope** — žádné file/function boundaries pro IDE AI? → přidat scope lock
4. **Stop conditions** — agent bez stop podmínky? → přidat checkpoint + human review triggers
5. **CoT** — přidáno k reasoning modelu (o3/R1/Qwen3-thinking)? → ODSTRANIT
6. **Grounding** — hrozí halucinace? → přidat "State only what you can verify"
7. **Constraints v prvních 30%** — nejdůležitější omezení na začátek promptu (attention decay)

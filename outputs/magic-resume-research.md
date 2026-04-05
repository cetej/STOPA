# Magic Resume — Rozbor a doporuceni

**Datum:** 2026-04-05
**Repo:** https://github.com/JOYCEQL/magic-resume (4 522 stars)
**Live:** https://magicv.art

## Executive Summary

Magic Resume je open-source resume builder postaveny na **TanStack Start + React 18 + Zustand + Tiptap 3**. Zajimave neni sam produkt (CV editor), ale **architektonicke vzory**, ktere jsou prenositelne do jinych projektu — zejmena template registry pattern, three-panel workbench UX, a PDF export pipeline.

---

## 1. Technicke pristupy — co stoji za pozornost

### Template Registry Pattern [VERIFIED]
Nejcistsi architektonicke rozhodnuti v celem repu. Pridani nove sablony = **jeden objekt** v `registry.ts`, zadny jiny soubor se nemeni. Kazda sablona deklaruje svou konfiguraci (colorScheme, spacing, sections) a React komponentu.

**Prenositelnost:** Vysoka. Pouzitelne pro:
- **KARTOGRAF** — registry map stylu (topographic, satellite, political)
- **NG-ROBOT** — registry sablon pro clanky/newslettery
- **STOPA skills** — uz mame podobny pattern, ale bez typed config objektu

### Zustand partialize + merge pro derived state [VERIFIED]
Store persistuje jen `{ resumes, activeResumeId }`, ale udrzuje `activeResume` jako odvozenou hodnotu. Custom `merge` funkce rekonstruuje derived state pri rehydrataci. Elegantne resi problem stale computed state po reload.

**Prenositelnost:** Stredni. Relevantni pokud pouzivame Zustand v nektorem frontendu.

### PDF Export Pipeline [VERIFIED]
Dvoustupnovy: server-side Puppeteer (primarni) + client-side html2pdf.js (fallback). Pred exportem:
- Strip animaci, transitions, hover pravidel z CSS
- Konverze `transform: scale()` na CSS `zoom` (Puppeteer pagination pocita z layout dimensions, ne z transform)
- External images → base64
- Odstraneni @font-face (font aplikovan inline)

**Prenositelnost:** Vysoka pro:
- **KARTOGRAF** — export map do PDF/PNG
- **NG-ROBOT** — export clanku do PDF
- Obecne: kazdy projekt s "render → export" pipeline

### AI Streaming + Model Config Table [VERIFIED]
Config tabulka `AI_MODEL_CONFIGS` s per-model `validate()` funkci. Pridani noveho AI modelu = jeden zaznam v tabulce. Streaming pres ReadableStream reader.

**Prenositelnost:** Nizka pro STOPA (pouzivame Anthropic API primo), ale vzor je cisty.

---

## 2. UX Patterny

### Three-Panel Workbench [VERIFIED]
Side panel (navigace) | Edit panel (formulare) | Preview (live render). Vsechny panely nezavisle resizable pres `react-resizable-panels`. Obousmerny klik: klik v preview → zvyrazni editor, klik v editoru → scroll preview.

**Prenositelnost:**
- **KARTOGRAF** — layers panel | properties | map preview
- **GRAFIK** — layers | editor | canvas
- **MONITOR** — sources panel | config | dashboard

### Drag & Drop s Explicitnim Handle [VERIFIED]
Framer Motion `Reorder.Item` s `dragListener={false}` + GripVertical handle. Klik na obsah = navigace, drag za handle = reorder. Reseno cisty — prevent accidental drags.

**Prenositelnost:** Vysoka. Pattern pouzitelny vsude kde je sortable list + clickable items.

### Section Visibility Toggle [VERIFIED]
Kazda sekce ma `enabled: boolean`. Eye/EyeOff toggle v side panelu. Jednoduchy, efektivni.

### Auto One-Page Scaling [VERIFIED]
Hook `useAutoOnePage` meri obsah vs A4 vysku, spocita scale factor (min 0.9 = max 10% zmenseni). Pokud nestaci, oznaci `cannotFit`. Pekne reseni pro "vejit se na stranku".

---

## 3. Architektonicke vzory

### Co je dobre
| Vzor | Kvalita | Proc |
|------|---------|------|
| Template Registry | Vynikajici | Open-Closed princip, type-safe, zero-touch pridani |
| Zustand persist s partialize | Dobre | Ciste oddeleni persisted vs derived state |
| SectionWrapper click-to-select | Dobre | Zero extra event system, preview je interaktivni |
| AI config validation colocation | Dobre | Validace zije s konfigem, ne v store |
| Module-level debounce timer | Dobre | Mimo React lifecycle, survive re-renders |

### Co je slabe
| Vzor | Problem |
|------|---------|
| Dve UI knihovny (Shadcn + HeroUI) | Zbytecna duplicita, nesourodost |
| i18n jen 2 jazyky | Custom reseni misto proven knihovny (i18next) |
| Zustand bez middleware pro undo/redo | Chybi history — dulezite pro editor |
| Zadne testy | 0 test souboru v celem repu |
| SSR disabled pro hlavni stranku | Workaround misto spravneho hydration reseni |

---

## 4. Kontext v ekosystemu (landscape)

| Repo | Stars | Stack | PDF | AI |
|------|-------|-------|-----|-----|
| Reactive-Resume | 36,100 | TanStack Start + Zustand | Chromium | OpenAI + Gemini + Claude |
| Resume-Matcher | 26,500 | Python | — | Job matching AI |
| rendercv | 16,200 | Python CLI | Typst | AI career assistant |
| open-resume | 8,500 | Next.js | react-pdf | — |
| **magic-resume** | **4,522** | **TanStack Start + Zustand** | **Puppeteer** | **Multi-model** |
| LapisCV | 4,400 | Markdown plugin | — | — |

Magic-resume je mensim klonem Reactive-Resume (podobny stack, mene features). Reactive-Resume ma 46 jazyku, team management, self-hosting guide.

---

## 5. Doporuceni pro tvoje projekty

### Okamzite pouzitelne (low effort, high value)

1. **Template/Style Registry Pattern** → adoptovat v KARTOGRAF a GRAFIK
   - Typed config objekt + React komponenta v jednom zaznamu
   - Pridani stylu = 1 soubor, 0 zmeny jinde
   - Inspirace: `registry.ts` v magic-resume

2. **Three-Panel Layout s react-resizable-panels** → KARTOGRAF, MONITOR
   - Misto fixniho layoutu — uzivatel si upravi sirku panelu
   - Knihovna je mala (6KB), stabilni, well-maintained

3. **PDF/Image Export Pipeline vzor** → KARTOGRAF
   - Strip nepotrebnych CSS pravidel pred exportem
   - Scale → zoom konverze pro spravne rozmery
   - Base64 inline obrazky pro self-contained output

### Strednedoba inspirace

4. **Bidirectional click-to-navigate** → GRAFIK, KARTOGRAF
   - Klik v preview zvyrazni editor, klik v editoru zvyrazni preview
   - `SectionWrapper` pattern — wrapper kolem kazde sekce v rendereru

5. **Zustand partialize + merge** → jakykoli frontend s persistent state
   - Persistovat jen minimalni data, derived state rekonstruovat
   - Prevence stale state po page reload

### Neprebirat

- **Framer Motion pro DnD** — hello-pangea/dnd je udrzovanejsi a feature-complete
- **Custom i18n** — pouzij i18next od zacatku
- **Dva UI frameworky** — jeden staci (Shadcn/ui)
- **Zero testy** — anti-pattern, neprebirat

---

## Evidence

| # | Zdroj | URL | Confidence |
|---|-------|-----|------------|
| 1 | magic-resume repo | https://github.com/JOYCEQL/magic-resume | high |
| 2 | Reactive-Resume | https://github.com/AmruthPillai/Reactive-Resume | high |
| 3 | open-resume | https://github.com/xitanggg/open-resume | high |
| 4 | rendercv | https://github.com/rendercv/rendercv | high |
| 5 | react-resizable-panels | https://github.com/bvaughn/react-resizable-panels | high |
| 6 | hello-pangea/dnd | https://github.com/hello-pangea/dnd | high |

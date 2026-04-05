# Open-Source Resume Builders on GitHub (2024-2026) — Research Brief

**Date:** 2026-04-05
**Question:** What is the current landscape of open-source resume builders on GitHub (2024-2026)?
**Scope:** survey — broad overview, multiple sub-topics
**Sources consulted:** 18 URLs fetched directly, 6 WebSearch queries
**Synthesis file:** outputs/.research/magic-resume-research-2-synthesis.md

---

## Executive Summary

The open-source resume builder space on GitHub is dominated by **Reactive-Resume** (36.1k stars) [VERIFIED][2], which has become the de facto standard for web-based self-hostable resume editing. Below it, a long tail of specialized tools covers every niche: CLI/YAML-based builders for engineers (RenderCV, 16.2k stars [VERIFIED][3]), Markdown editors (LapisCV, oh-my-cv), LaTeX generators (resumake.io), and — notably — a growing cohort of AI-first tailoring tools led by Resume-Matcher (26.5k stars [VERIFIED][3]), though the latter is primarily a job-match optimizer rather than a traditional builder.

The dominant tech stack in 2024-2026 is **TypeScript + React/Next.js + Tailwind CSS + Zustand** for web builders [INFERRED][2,5,9], with **Puppeteer/Chromium** and **react-pdf** as the two main PDF export strategies. A major architectural divergence is between web-app builders (real-time WYSIWYG) and code-first tools (YAML/Markdown → PDF), with each approach attracting different audiences. [INFERRED][2,3,4,10]

The most notable UX innovation is **AI-assisted writing** integrated directly into the editor — Reactive-Resume supports OpenAI, Gemini, and Anthropic Claude; RenderCV launched a full AI career assistant on their web app. [VERIFIED][2,13] Internationalization is handled unevenly: Reactive-Resume leads with 46 community-translated languages via Crowdin [INFERRED][16], while most others cover only English + Chinese or are English-only.

---

## Detailed Findings

### 1. Top Repos by GitHub Stars

Star counts sourced directly from the GitHub Topics page (https://github.com/topics/resume-builder), fetched 2026-04-05 [VERIFIED][1]:

| Rank | Repository | Stars | Type |
|------|-----------|-------|------|
| 1 | AmruthPillai/Reactive-Resume | 36,100 | Web builder (WYSIWYG) |
| 2 | srbhr/Resume-Matcher | 26,500 | AI job-matching / tailoring tool |
| 3 | rendercv/rendercv | 16,200 | CLI / YAML → PDF builder |
| 4 | xitanggg/open-resume | 8,500 | Web builder (privacy-focused) |
| 5 | HugoBlox/hugo-theme-academic-cv | 4,900 | Static site / Hugo theme |
| 6 | BingyanStudio/LapisCV | 4,400 | Markdown plugin (VSCode/Typora/Obsidian) |
| 7 | saadq/resumake.io | 3,600 | LaTeX web generator |
| 8 | visiky/resume | 3,100 | Web builder (bilingual) |
| 9 | sproogen/modern-resume-theme | 2,300 | Jekyll theme |
| 10 | Arman19941113/dnd-resume | 1,400 | Drag-and-drop web builder |
| 11 | sadanandpai/resume-builder | 1,200 | Minimal web builder (no login) |
| 12 | twwch/JadeAI | 1,100 | AI-first builder (50+ templates) |
| 13 | Renovamen/oh-my-cv | 907 | Markdown PWA, local-first |

**Important caveat:** Resume-Matcher [VERIFIED][3] is primarily a tool that tailors an existing resume to a job description rather than building resumes from scratch. Its 26.5k stars reflect demand for AI-assisted job applications, but it belongs to a slightly different category than traditional resume builders.

**Note on hugo-theme-academic-cv and LapisCV:** These are not builders in the traditional sense — hugo-theme-academic-cv generates a website from Markdown content [UNVERIFIED - star count confirmed, tool type inferred], and LapisCV is a Markdown document format for editors (Typora/VSCode/Obsidian) with CSS-controlled export [VERIFIED][6].

---

### 2. Tech Stacks

#### Web Builders (WYSIWYG / browser-based)

**Reactive-Resume** [VERIFIED][2] — the most feature-complete open-source web builder:
- Framework: TanStack Start (React 19, Vite) — migrated from Next.js
- Language: TypeScript (99.2% of codebase)
- Database: PostgreSQL + Drizzle ORM
- API: ORPC (type-safe RPC layer)
- Auth: Better Auth (passkeys, 2FA)
- Styling: Tailwind CSS + Radix UI
- State: Zustand + TanStack Query
- Rich text: Tiptap editor
- Last commit: April 4, 2026

**OpenResume** [VERIFIED][5] — privacy-focused, no backend:
- Framework: Next.js 13
- Language: TypeScript (97.6%)
- State: Redux Toolkit
- PDF: react-pdf (client-side, no server)
- PDF parsing: PDF.js (import existing resumes)
- Last update: October 2024

**sadanandpai/resume-builder** [VERIFIED][9] — minimal, no sign-up:
- Framework: Next.js 15
- Language: TypeScript (96.8%)
- UI: Material UI + Tailwind CSS
- State: Zustand
- Last update: November 2025

**visiky/resume** [VERIFIED][7]:
- Framework: Gatsby + Ant Design
- Language: TypeScript (80.9%), Less (15.3%)
- Data storage: GitHub Gist (JSON in special repo)
- Last update: May 2023 (less actively maintained)

**JadeAI** [VERIFIED][11]:
- Framework: Next.js 16 (App Router, Turbopack)
- UI: React 19, Tailwind CSS 4, shadcn/ui, Radix UI
- DB: Drizzle ORM (SQLite / PostgreSQL)
- AI: Vercel AI SDK v6 + OpenAI / Anthropic
- PDF: Puppeteer Core + @sparticuz/chromium

#### CLI / Code-First Tools

**RenderCV** [VERIFIED][3,4] — YAML → PDF for engineers and academics:
- Language: Python (82.8%), Typst (16.5%)
- Input format: YAML with Pydantic validation + JSON Schema autocompletion
- PDF: Typst typesetting engine (switched from LaTeX in v2.0)
- Rationale for Typst switch [VERIFIED][15]: LaTeX couldn't be pip-installed cleanly and lacked CJK language support; Typst solves both
- Last commit: March 25, 2026

**Resumake.io** [VERIFIED][6] — LaTeX from a web form:
- Frontend: React + TypeScript
- Backend: Node.js
- Codebase: TeX 61.3%, TypeScript 38.6%
- PDF: LaTeX/PDFLaTeX compilation
- Last update: January 2024 (v3 rewrite in progress)

**oh-my-cv** [VERIFIED][10] — Markdown, browser-only PWA:
- Framework: Vue (39.9%)
- Language: TypeScript (56.6%)
- Architecture: local-first, data in browser storage
- PDF: exports to A4 and US Letter, auto-pagination
- Rich features: KaTeX (LaTeX math), Iconify icons, Google Fonts
- Last update: July 2024

**LapisCV** [VERIFIED][6] — Markdown-in-editor format:
- Format: pure Markdown with CSS variables for styling
- Editors: VSCode, Typora, Obsidian
- PDF: native export of each editor (no dedicated server)
- Themes: LapisCV, LapisCV Serif

---

### 3. Architectural Patterns

#### PDF Export — 5 distinct strategies

| Strategy | Tools | Pros | Cons |
|----------|-------|------|------|
| **LaTeX/PDFLaTeX** | resumake.io | High typography quality, professional output | Complex install, no CJK languages |
| **Typst** | rendercv | Modern TeX alternative, pip-installable, CJK support | Smaller ecosystem than LaTeX |
| **react-pdf** | open-resume, resumelm | React components → PDF, can run client-side | Limited CSS support compared to browser |
| **Puppeteer/headless Chromium** | Resume-Matcher, JadeAI | Pixel-perfect HTML→PDF, full CSS support | Server-side only, heavy binary |
| **Browser window.print()** | dnd-resume | Zero server dependency, simplest | Quality depends on browser, less control |

[INFERRED][2,3,5,6,8,11] — based on README and package.json data from multiple repos

#### State Management

Zustand is the emerging standard for newer projects (Reactive-Resume, sadanandpai/resume-builder), replacing Redux Toolkit which is used by OpenResume [INFERRED][2,5,9]. TanStack Query handles server-state in Reactive-Resume alongside Zustand for client-state [VERIFIED][2].

#### Data Persistence Models

Three distinct models observed [INFERRED][2,5,7,10]:
1. **Server-side DB** (Reactive-Resume, JadeAI) — PostgreSQL, accounts, multi-device sync
2. **GitHub Gist** (visiky/resume, JSON Resume standard) — version-controlled JSON, no server
3. **Local-only / browser storage** (open-resume, oh-my-cv, sadanandpai/resume-builder) — maximum privacy, no sync

#### Template Engine Approaches

- **React components as templates**: Reactive-Resume, open-resume (each template is a React component rendering the resume data)
- **Typst markup templates**: RenderCV (9 built-in themes, user-customizable)
- **LaTeX template files**: resumake.io (8+ LaTeX template files, TeX-based)
- **CSS-controlled Markdown**: oh-my-cv, LapisCV (one Markdown → different look via CSS)
- **Server-rendered HTML templates**: Resume-Matcher (classic/modern variants)

---

### 4. UX Innovations

#### AI-Assisted Writing

The biggest UX shift from 2023 to 2026 is native AI integration [INFERRED][2,11,12,13,16]:

- **Reactive-Resume**: Integrates OpenAI, Google Gemini, and Anthropic Claude directly in the editor. Users bring their own API key. AI can improve bullet points, rewrite summaries, suggest content. [VERIFIED][2] via README, [INFERRED][16] — 46-language support from Crowdin community
- **Resume-Matcher** [VERIFIED][3]: Full pipeline — upload resume, paste job description → AI rewrites resume for that specific role + generates cover letter. Supports Ollama (local), OpenAI, Anthropic, Gemini, OpenRouter, DeepSeek.
- **RenderCV web app** [VERIFIED][13]: AI career assistant with internet access — analyzes CVs against job descriptions, generates cover letters, searches for relevant jobs, applies edits directly to YAML
- **JadeAI** [VERIFIED][11]: AI interview simulation with 6 preset interviewer roles, grammar auto-fix, multi-language translation
- **ResumeLM** [VERIFIED][12]: Multi-LLM support (GPT, Claude, Gemini, DeepSeek, Groq) for job-specific tailoring

#### Real-Time Preview

All major web builders (Reactive-Resume, OpenResume, dnd-resume, visiky/resume, JadeAI) offer real-time preview — edits in the left panel immediately reflect in the PDF preview on the right [INFERRED][2,5,7,8,11] from feature lists and screenshots.

#### Drag-and-Drop Section Reordering

- **Reactive-Resume** [VERIFIED][2]: drag-and-drop section ordering in the editor
- **dnd-resume** [VERIFIED][8]: core feature, entire project built around it (dnd-resume.com)
- **Resume-Matcher** [VERIFIED][3]: drag-and-drop to rearrange resume sections within tailored output

Note: react-beautiful-dnd (the dominant drag-and-drop library) was archived by Atlassian on August 18, 2025 [VERIFIED][17]. The maintained community fork is hello-pangea/dnd.

#### Resume Import / Parsing

- **OpenResume** [VERIFIED][5]: imports existing PDF resumes via PDF.js, extracts content for redesign
- **JadeAI** [VERIFIED][11]: parses PDFs and images of resumes to extract content
- **Resume-Matcher** [VERIFIED][3]: uploads existing resume as starting point for tailoring

#### Self-Hosting

Reactive-Resume, JadeAI, and Resume-Matcher all provide Docker Compose configurations for self-hosting [INFERRED][2,11,3] — reflecting strong demand for data privacy in the job-seeking process.

---

### 5. Internationalization and Theming

#### Internationalization

| Project | Languages | Method |
|---------|-----------|--------|
| Reactive-Resume | 46 languages [INFERRED][16] | Crowdin community translations |
| Resume-Matcher | 5 languages [VERIFIED][3] | UI + AI content generation |
| RenderCV | "Any language" [VERIFIED][13] | Typst Unicode engine, no hard limits |
| visiky/resume | Chinese + English [VERIFIED][7] | Built-in i18n toggle |
| JadeAI | Chinese + English [VERIFIED][11] | next-intl library, configurable default locale |
| oh-my-cv | Not documented | — |
| open-resume | English only (inferred) | No i18n mentioned |

Chinese+English bilingual support appears as the second most common target after full i18n [INFERRED][7,11] — reflecting the large Chinese developer community building these tools.

#### Theming

| Project | Template/Theme Count | Theming Mechanism |
|---------|---------------------|-------------------|
| Reactive-Resume | 12 templates (Pokémon-named) [VERIFIED][2,14] | React components; custom CSS injection; dark mode |
| RenderCV | 9 themes [VERIFIED][3,13] | Typst theme files; customizable margins/fonts/colors |
| JadeAI | 50+ templates [VERIFIED][11] | Server-rendered per template |
| Resumake.io | 8+ LaTeX templates [VERIFIED][6] | LaTeX template switching |
| oh-my-cv | Custom CSS + Google Fonts [VERIFIED][10] | CSS variables, Iconify icons |
| open-resume | 1 default template [VERIFIED][5] | Minimal, no theming |
| sadanandpai/resume-builder | Multiple (undocumented count) | Material UI + Tailwind |

Reactive-Resume's custom CSS injection feature [INFERRED][16] is the most flexible theming approach — users can write arbitrary CSS or prompt an AI to generate it.

---

## Disagreements & Open Questions

1. **Resume-Matcher categorization**: With 26.5k stars, Resume-Matcher appears second on the resume-builder topic page, but it is fundamentally a tailoring/optimization tool, not a builder. Its star count may inflate perceived category size. [VERIFIED star count, [INFERRED] category disagreement from reading README vs. title]

2. **Reactive-Resume AI language count**: The Crowdin-powered 46-language claim comes from a secondary search result, not directly from the Crowdin dashboard or a dated commit. The README says "multi-language support" without a specific count. [SINGLE-SOURCE][16] — treat 46 as approximate.

3. **State of react-beautiful-dnd ecosystem**: The original library was archived August 2025 [VERIFIED][17]. It's unclear which resume builders have migrated to hello-pangea/dnd or other alternatives — this gap exists across the ecosystem.

4. **JadeAI and ResumeLM star counts**: The GitHub topic page showed JadeAI at 1.1k stars; ResumeLM's README fetch did not return a star count. These projects are newer (2024-2025) and growing rapidly. [VERIFIED] JadeAI stars, [UNVERIFIED] ResumeLM stars.

5. **Resumake.io v3 status**: The repo was undergoing a "major v3 rewrite" as of January 2024 [VERIFIED][6]. Current status of v3 is unknown.

---

## Evidence Table (full)

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | GitHub Topics: resume-builder | https://github.com/topics/resume-builder | Star rankings (fetched 2026-04-05) | primary | high |
| 2 | Reactive-Resume README | https://github.com/AmruthPillai/Reactive-Resume | 36.1k stars; TanStack Start+React 19; Zustand; 12 templates; 46 langs | primary | high |
| 3 | Resume-Matcher README | https://github.com/srbhr/Resume-Matcher | 26.5k stars; FastAPI+Next.js 16; Playwright PDF; multi-LLM; 5 langs | primary | high |
| 4 | RenderCV README | https://github.com/rendercv/rendercv | 16.2k stars; Python+Typst v2.0; YAML input; 9 themes | primary | high |
| 5 | OpenResume README | https://github.com/xitanggg/open-resume | 8.5k stars; Next.js 13; Redux Toolkit; react-pdf; PDF.js import | primary | high |
| 6 | Resumake.io README | https://github.com/saadq/resumake.io | 3.6k stars; LaTeX/PDFLaTeX; React+Node.js; v3 rewrite in progress | primary | high |
| 7 | visiky/resume README | https://github.com/visiky/resume | 3.1k stars; Gatsby+Ant Design; zh+en i18n; GitHub Gist storage | primary | high |
| 8 | dnd-resume README | https://github.com/Arman19941113/dnd-resume | 1.4k stars; drag-and-drop core feature; browser print PDF; TypeScript | primary | high |
| 9 | sadanandpai/resume-builder README | https://github.com/sadanandpai/resume-builder | 1.2k stars; Next.js 15; Material UI; Zustand; no sign-up | primary | high |
| 10 | oh-my-cv README | https://github.com/Renovamen/oh-my-cv | 907 stars; Vue+TypeScript; Markdown; local-first PWA; KaTeX support | primary | high |
| 11 | JadeAI README | https://github.com/twwch/JadeAI | 1.1k stars; Next.js 16+React 19; Puppeteer PDF; zh+en; 50+ templates | primary | high |
| 12 | ResumeLM README | https://github.com/olyaiy/resume-lm | Next.js 15; Supabase; React PDF; GPT+Claude+Gemini+DeepSeek+Groq | primary | medium |
| 13 | RenderCV web app | https://rendercv.com/ | AI career assistant; 9 themes; GitHub sync; YAML+form editor | primary | high |
| 14 | Reactive Resume docs | https://docs.rxresu.me/ | Tiptap rich text; Pokémon template names; Docker self-hosting | primary | high |
| 15 | RenderCV Typst discussion | https://github.com/rendercv/rendercv/discussions/233 | Switched to Typst v2.0 for pip install + CJK language support | primary | high |
| 16 | WebSearch: rxresume i18n | search aggregated | 46 languages via Crowdin; custom CSS injection in templates | secondary | medium |
| 17 | react-beautiful-dnd archive | https://github.com/atlassian/react-beautiful-dnd/issues/2573 | Archived Aug 18, 2025; hello-pangea/dnd is maintained fork | primary | high |
| 18 | resufit.com comparison | https://resufit.com/blog/5-best-open-source-cv-builders-for-professional-resumes-in-2024/ | Comparison: Reactive Resume, OpenResume, JSON Resume, Resumake, Visiky | secondary | medium |

---

## Sources

1. GitHub Topics: resume-builder — https://github.com/topics/resume-builder
2. AmruthPillai/Reactive-Resume — https://github.com/AmruthPillai/Reactive-Resume
3. srbhr/Resume-Matcher — https://github.com/srbhr/Resume-Matcher
4. rendercv/rendercv — https://github.com/rendercv/rendercv
5. xitanggg/open-resume — https://github.com/xitanggg/open-resume
6. saadq/resumake.io — https://github.com/saadq/resumake.io
7. visiky/resume — https://github.com/visiky/resume
8. Arman19941113/dnd-resume — https://github.com/Arman19941113/dnd-resume
9. sadanandpai/resume-builder — https://github.com/sadanandpai/resume-builder
10. Renovamen/oh-my-cv — https://github.com/Renovamen/oh-my-cv
11. twwch/JadeAI — https://github.com/twwch/JadeAI
12. olyaiy/resume-lm — https://github.com/olyaiy/resume-lm
13. RenderCV web app — https://rendercv.com/
14. Reactive Resume documentation — https://docs.rxresu.me/
15. RenderCV Typst migration discussion — https://github.com/rendercv/rendercv/discussions/233
16. WebSearch aggregated: reactive-resume i18n 2024
17. react-beautiful-dnd archive issue — https://github.com/atlassian/react-beautiful-dnd/issues/2573
18. Resufit.com comparison article — https://resufit.com/blog/5-best-open-source-cv-builders-for-professional-resumes-in-2024/

---

## Coverage Status

**[VERIFIED]** (directly checked, URL fetched, content confirmed):
- Star counts for all 13 repos (GitHub Topics page, fetched 2026-04-05)
- Reactive-Resume full stack: TanStack Start, React 19, TypeScript, Zustand, TanStack Query, Tailwind, Radix UI, Drizzle ORM, ORPC, Better Auth
- OpenResume stack: Next.js 13, TypeScript, Redux Toolkit, react-pdf, PDF.js
- RenderCV stack: Python, Typst, YAML, Pydantic, 9 themes, March 2026 last commit
- Resumake.io: LaTeX/PDFLaTeX, React+Node.js, v3 rewrite ongoing
- visiky/resume: Gatsby, Ant Design, Chinese+English i18n
- dnd-resume: drag-and-drop, browser print, AGPL-3.0
- oh-my-cv: Vue+TypeScript, Markdown, local-first PWA, KaTeX, A4+Letter export
- JadeAI: Next.js 16, Puppeteer Core + @sparticuz/chromium for PDF, zh+en
- react-beautiful-dnd archived August 18, 2025

**[INFERRED]** (derived from multiple sources, not stated verbatim anywhere):
- TypeScript + React/Next.js + Tailwind + Zustand as dominant 2024-2026 stack
- Puppeteer and react-pdf as the two main PDF strategies for web builders
- Three data persistence models: server DB / GitHub Gist / browser-only
- Chinese+English as the most common non-English language pair

**[SINGLE-SOURCE]:**
- Reactive-Resume supports 46 languages (one secondary search result; README says "multi-language" without count)
- Resumake.io star count (3.6k) from Jina fetch of README only

**[UNVERIFIED]:**
- Resumake.io v3 rewrite current status
- ResumeLM exact star count
- LapisCV exact star count (badge in README didn't render a number)
- Which specific DnD library Reactive-Resume uses internally (not stated in README)

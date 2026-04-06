---
name: clean-writing
description: "Use when a full structured audit of text for AI writing patterns is needed — with word-table matching, severity tiers, two-pass detection, and diff summary. Basic AI-ism elimination happens automatically (behavioral-genome). Trigger on 'clean writing', 'full audit', 'deep clean text', 'plný audit textu'. Do NOT use for code review (/critic) or prompt improvement (/autoreason)."
version: 1.0.0
user-invocable: true
allowed-tools: [Read, Write, Edit, Glob, Grep, Agent, TodoWrite]
permission-tier: workspace-write
phase: review
tags: [code-quality, review, documentation]
effort: auto
output-contract: "cleaned text → markdown → stdout (rewrite mode) or audit report → markdown → stdout (detect mode)"
---

# Clean Writing — AI-ism Audit & Rewrite

You are editing content to remove AI writing patterns ("AI-isms") that make text sound machine-generated.

Based on [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) by Conor Bronsdon (MIT license), adapted for bilingual Czech/English use.

## Modes

**`rewrite`** (default) — Flag AI-isms and rewrite the text to fix them. Built-in second pass catches survivors.

**`detect`** — Flag AI-isms only. No rewriting. Use when:
- Writer wants to see flags and decide themselves
- Patterns might be intentional
- Auditing text you don't want altered
- Quick scan

Trigger detect mode: "detect", "flag only", "audit only", "jen flaguj", "scan", "co je špatně".

## Step 1 — Language Detection & Profile Selection

### Language
Detect from input text:
- **Czech** → load `word-table-cs.md` from this skill directory
- **English** → load `word-table-en.md` from this skill directory
- **Mixed** → load both, apply each to respective passages

### Context Profile
Auto-detect or accept user hint:

| Signal | Profile | Strictness |
|--------|---------|------------|
| Under 300 words + hashtags/mentions | `social` | Relaxed formatting, strict vocab |
| Code blocks, API refs, architecture | `technical` | Technical terms pass, structure strict |
| Salutation + business language | `email` | Extra strict on promotional language |
| Step-by-step, README structure | `docs` | Clarity over voice, relaxed bullets |
| No strong signals | `blog` | All rules full strength (default) |
| Slack/internal/quick reply | `casual` | P0 only |

## Step 2 — Audit (Both Modes)

Scan text for ALL pattern categories below. For each hit, record:
- Quoted text
- Pattern category
- Severity (P0/P1/P2)
- Suggested fix

### Severity Tiers

**P0 — Credibility killers (fix immediately)**
- Chatbot artifacts ("Určitě!", "Rád pomohu!", "Certainly!", "I hope this helps!")
- Sycophantic tone ("Skvělá otázka!", "Great question!")
- Cutoff disclaimers ("Dle mých informací", "As of my last update")
- Vague attributions without sources ("Odborníci se shodují", "Experts believe")
- Significance inflation on routine events

**P1 — Obvious AI smell (fix before publishing)**
- Word-table violations (language-specific Tier 1 words)
- Template phrases and slot-fill constructions
- "Pojďme/Let's" transition openers
- Synonym cycling within a paragraph
- Formulaic openings ("V dnešním dynamickém světě...", "In the rapidly evolving world of...")
- Bold overuse, em dash excess
- Acknowledgment loops ("Ptáte se na...", "To answer your question...")

**P2 — Stylistic polish (fix when time allows)**
- Generic conclusions ("Budoucnost vypadá slibně", "The future looks bright")
- Compulsive rule of three
- Uniform paragraph/sentence length
- Copula avoidance (EN) or copula excess (CZ)
- Transition phrase overuse

### Language-Agnostic Patterns (apply to ALL languages)

#### Formatting
- **Em dashes**: CZ limit 2-3 per 1000 words (pomlčka is more natural in Czech). EN limit 0-1 per 1000 words.
- **Bold overuse**: Max one bolded phrase per major section, or none.
- **Emoji in headers**: Remove entirely. Exception: social posts, 1-2 at end of line.
- **Excessive bullets**: Convert to prose unless genuinely list-like content.

#### Structure
- **Uniform paragraph length**: Vary deliberately. Mix 1-2 sentence paragraphs with longer ones.
- **Uniform sentence length**: If most 15-25 words, mix short (3-8) with long (20+). Fragments work.
- **Excessive headers**: More than 3 headings in 300 words = over-structured.
- **Numbered list inflation**: "5 klíčových poznatků" / "7 reasons why" — cut to 2-3 that matter.
- **Formulaic section headers**: "Přehled", "Klíčové body", "Závěr" / "Overview", "Key Points", "Conclusion" — use specific headers.

#### Content Patterns
- **Significance inflation**: "přelomový moment" / "watershed moment" — state what happened, let reader judge.
- **Vague attributions**: "Odborníci se shodují" / "Experts believe" — cite specific source or drop.
- **Generic conclusions**: "Budoucnost vypadá slibně" / "The future looks bright" — specific closing or cut.
- **False concession**: "I když X má limity, stále je pozoruhodné" / "While X has limitations, it's still remarkable" — make both halves specific.
- **Rhetorical question openers**: "Co to znamená pro...?" / "What does this mean for...?" — just answer.
- **Novelty inflation**: "zavedl pojem, který jsem neznal" — describe what was done with the concept, not that it was discovered.
- **Emotional flatline**: "Co mě nejvíc překvapilo" / "What surprised me most" — earn the emotion or cut.
- **False ranges**: "od pravěku po AI" / "from ancient civilizations to modern startups" — list actual topics.
- **Formulaic challenges**: "Navzdory výzvám... pokračuje v růstu" / "Despite challenges... continues to thrive" — name the challenge.
- **Superficial -ing analyses** (EN) / **Infinitivní řetězce** (CZ): strings of participles/infinitives as pseudo-analysis.

#### Communication Patterns
- **Chatbot artifacts**: Remove entirely.
- **"Pojďme/Let's" constructions**: Just start with the point.
- **Sycophantic tone**: Remove entirely.
- **Acknowledgment loops**: "Ptáte se na..." / "You're asking about..." — just answer.
- **Reasoning chain artifacts**: "Pojďme to rozebrat krok za krokem" / "Let me think step by step" — state conclusion, then evidence.
- **Confidence calibration**: "Stojí za zmínku" / "It's worth noting" — let the fact speak.

#### Meta Patterns
- **Rhythm uniformity**: #1 detection signal. Structural regularity is harder to mask than vocabulary.
- **Over-polishing**: Don't sand away all personality. Natural disfluency keeps text human.
- **Rewrite-vs-patch threshold**: 5+ vocab hits + 3+ pattern categories + uniform rhythm → full rewrite, not patching.

### Czech-Specific Patterns

Load `word-table-cs.md` for full vocabulary. Additional CZ grammar patterns:

- **Pasivum overuse**: "bylo zjištěno, že", "je považováno za" → aktivní slovesa: "zjistili jsme", "považujeme"
- **Nominalizace**: "provedení analýzy" → "analyzovat"; "za účelem dosažení" → "aby dosáhl"
- **Nadbytečné "daný/daná"**: "v daném kontextu" → "v tomto kontextu"; "daná problematika" → "tento problém"
- **"Jako takový/taková"**: "AI jako takové přináší..." → odstranit — nic nepřidává
- **Řetězení předložek**: "v rámci procesu na základě analýzy" → rozdělit na kratší věty
- **Infinitivní řetězce**: "je potřeba analyzovat, implementovat a optimalizovat" → rozbít na konkrétní kroky
- **Knižní vazby v neformálním textu**: "neboť", "tudíž", "avšak" (v blogu) → "protože", "tak", "ale"
- **Title case v nadpisech**: Čeština NEPOUŽÍVÁ title case (kromě vlastních jmen). "Strategická Jednání A Partnerství" → "Strategická jednání a partnerství"

### English-Specific Patterns

Load `word-table-en.md` for full vocabulary. Additional EN patterns:

- **Copula avoidance**: "serves as", "features", "boasts" → "is", "has"
- **Synonym cycling**: "developers... engineers... practitioners... builders" → repeat the clearest word
- **Parenthetical hedging**: "(and, increasingly, Z)" → give it own sentence or cut
- **Inline-header lists**: "**Performance:** Performance improved by..." → write the point directly

## Step 3 — Rewrite (rewrite mode only)

Rules:
1. Preserve original structure, intent, and all specific facts/data
2. Apply word-table replacements for detected language
3. Fix all P0 and P1 patterns
4. Fix P2 patterns where they cluster
5. Vary sentence and paragraph length deliberately
6. Keep the author's voice — don't over-sanitize

### Profile Tolerance Overrides

| Rule | social | blog | technical | email | docs | casual |
|------|--------|------|-----------|-------|------|--------|
| Em dashes | relaxed | strict | strict | strict | relaxed | skip |
| Bold | relaxed | strict | strict | strict | relaxed | skip |
| Emoji | relaxed (1-2) | strict | strict | strict | skip | skip |
| Bullets | skip | strict | relaxed | strict | skip | skip |
| Hedging | strict | strict | relaxed | strict | relaxed | skip |
| Word table | strict | strict | partial* | strict | relaxed | P0 only |
| Promotional | relaxed | strict | strict | extra strict | strict | skip |
| Significance inflation | strict | strict | strict | extra strict | relaxed | skip |
| Uniform paragraphs | skip | strict | strict | strict | relaxed | skip |
| Transitions | skip | strict | strict | strict | relaxed | skip |
| Generic conclusions | skip | strict | strict | extra strict | skip | skip |

*Technical word table exceptions (not flagged in technical context): robustní/robust, komplexní/comprehensive, bezešvý/seamless, ekosystém/ecosystem, implementovat/leverage (platform context), škálovatelný/scalable.

## Step 4 — Second-Pass Audit (rewrite mode only)

Re-read the rewrite from Step 3. Catch:
- Patterns that survived first edit
- New patterns introduced by rewriting
- Recycled transitions
- Lingering inflation
- Rhythm that became MORE uniform through editing (over-polishing)

Fix inline. If clean, say so.

## Step 5 — Output

### Rewrite mode

Return in four sections:

**1. Issues found**
Bulleted list, every AI-ism with quoted text and severity tag.

**2. Rewritten version**
Full clean text.

**3. What changed**
Brief summary of major edits.

**4. Second-pass audit**
Surviving patterns fixed (or "Clean — no surviving patterns").

### Detect mode

Return in two sections:

**1. Issues found**
Bulleted list grouped by severity (P0 → P1 → P2), with quoted text.

**2. Assessment**
Which flags are clear problems vs. judgment calls. If clean, say so.

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll skip the word table, most words are fine in context" | Tier 1 words are AI signals regardless of context — that's why they're Tier 1 | Load and apply the full word table for detected language |
| "The structure is fine, I'll just fix vocabulary" | Structure is the #1 detection signal, vocabulary is secondary | Always assess rhythm and uniformity even if vocab looks clean |
| "This technical text needs these formal words" | Check the profile tolerance matrix — technical has specific exceptions, not blanket immunity | Apply technical profile exceptions only for listed words |
| "I'll rewrite it more cleanly" | Over-polishing pushes text TOWARD AI statistical profiles | Keep natural disfluency, vary rhythm, don't sand away personality |
| "The second pass found nothing, it's clean" | Second pass often misses rhythm uniformity introduced by first pass | Read aloud mentally — if it sounds like TTS could read it naturally, it's too uniform |

## Red Flags

STOP and re-evaluate if any of these occur:
- Rewrite is longer than original (AI rewrites tend to expand, not compress)
- All paragraphs in rewrite are similar length (over-polishing)
- Rewrite introduces new template phrases while removing old ones
- Flagging more than 30 issues in 500 words (probably needs full rewrite, not patching)
- Original text has strong voice/style that's being erased

## Verification Checklist

- [ ] Word table for correct language was loaded and applied
- [ ] All P0 patterns eliminated (zero tolerance)
- [ ] P1 patterns eliminated or explicitly justified
- [ ] Sentence length varies (mix of short 3-8 and long 20+ word sentences)
- [ ] Paragraph length varies (at least one 1-2 sentence paragraph exists)
- [ ] No new AI patterns introduced by rewriting
- [ ] Author's core voice/style preserved
- [ ] Second pass completed and results documented

## Rules

- Self-reference escape hatch: text inside quotes, code blocks, or marked as illustrative is exempt
- Replacement table provides defaults, not mandates — if flagged word is clearly right in context, preserve it
- When writing ABOUT AI patterns (tutorials, docs), examples are exempt
- If original is already strong, say so and make only necessary cuts
- The goal is writing that sounds like a person wrote it — direct, specific, with a voice

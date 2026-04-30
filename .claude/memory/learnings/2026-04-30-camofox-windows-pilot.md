---
date: 2026-04-30
type: best_practice
severity: medium
component: general
tags: [browser-automation, anti-detect, scraping, windows, mcp-pilot, camoufox, obscura]
summary: Anti-detect browser pilot pattern — install do izolovaného _<tool>-pilot/ adresáře, test REST API přímo místo MCP layer, time-box 1.5h. Camoufox v135.0.1-beta.24 (jo-inc/camofox-browser v1.8.15) na Windows: 4/5 fingerprint testů pass, ale Cloudflare bypass currently broken (Turnstile stuck na "Just a moment", upstream issue #574), 3 plugins padly na ESM URL bug, 7 lingering camoufox.exe po shutdown. Stalled upstream 13 měsíců = anti-detect efficacy decay risk.
source: agent_generated
uses: 2
successful_uses: 0
harmful_uses: 0
confidence: 0.80
maturity: draft
valid_until: 2026-10-30
verify_check: "Grep('camofox-browser', path='STOPA/.claude/memory/radar.md') → 1+ match"
related: [2026-03-27-playwright-mcp-download-hijack.md]
---

## Anti-detect MCP pilot pattern

**Goal**: Empirically verify whether new anti-detect browser tool replaces/complements existing stack vs ekosystém claims.

**Pattern** (validated 2026-04-30 on jo-inc/camofox-browser):

1. **Isolate**: clone do `~/Documents/000_NGM/_<tool>-pilot/` — ne do projektu, ne globálně. Smazatelné jednou rm.
2. **Skip MCP layer for empirical engine test**: testuj REST API přímo (curl + Python) místo Claude Desktop MCP wrapper. Engine quality ≠ MCP plumbing — testuj engine, ne wrapper.
3. **Skip Playwright browser downloads**: `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 PUPPETEER_SKIP_DOWNLOAD=1` před `npm install` — anti-detect tool má vlastní bundled Firefox fork, Chromium nepotřeba (~700 MB úspora).
4. **5 cílů, ne víc**: bot.sannysoft.com (fingerprint panel), CreepJS, AreYouHeadless, jeden Cloudflare-protected, jeden domain-relevant (CZ news pro ZACHVEV). Více = stejný signál, hořící čas.
5. **Comparable baseline**: pro každý target zachyt `urllib.request` baseline status — jaký vstup tool má vylepšit.
6. **Stability test = retry**: anti-detect bug class je často "1st request po startu OK, 2nd fails" (browser context race). Spusť 2× kvůli reproducibility.
7. **Memory + process cleanup audit**: po pilotu zkontroluj `taskkill //F //IM <browser>.exe` count — kolik procesů zůstalo orphaned. Production stability concern.

## Camoufox-specific empirical data (2026-04-30)

| Finding | Detail | Implication |
|---------|--------|-------------|
| Cloudflare bypass | ❌ STUCK na "Just a moment..." challenge na nopecha demo | Camoufox upstream issue #574/#584 confirmed reproducible. `<title>Just a moment...</title>` v HTML. |
| Daijro upstream stall | 13 měsíců bez release (v135.0.1-beta.24 z 2025-03-15) | Anti-detect efficacy decay, bypass-vs-detection gap roste měsíc co měsíc. |
| Windows ESM URL bug | 3 plugins (persistence, vnc, youtube) padly na `Received protocol 'c:'` | Native Windows is unsupported in practice. Code uses `c:\path` jako ESM import URL — Node potřebuje `file:///c:/path`. Persistence loss = no session continuity. |
| Process orphaning | 7 lingering `camoufox.exe` po node server shutdown | Long-running production leakuje procesy. Vyžaduje `taskkill //F //IM camoufox.exe` pro cleanup. |
| Memory leak claim | Upstream má 8/12 open `leak:native-memory` issues (200-839 MB růst) | Krátký pilot (5 tabů, 5 min) leak nereprodukoval, ale production lifetime risk je real. |
| Stability bug | `browserContext.newPage: Target page, context or browser has been closed` na 2nd-fresh-tab po startup | Reproducible. Možná race condition s plugin failures. |
| Niche wins | CreepJS BYPASSED (FP ID rendered), bot.sannysoft 4/4 fingerprint signals pass, AreYouHeadless explicit "not headless" | Pro Firefox-fingerprint-specific blockers funguje. Accessibility snapshot API + element refs (`e1`, `e2`) je nice pro AI-agent scraping. |

## Decision rule

Před investigací nového anti-detect tool spusť 1.5h pilot. **Vyhodnocení:**

- 🔴 **Install permanently**: Cloudflare bypass works + Windows native works + memory stable nad 30+ min usage + accessibility/snapshot API.
- 🟡 **Keep in radar**: Niche wins existují ale primary use case (Cloudflare) selhává. Re-evaluate když upstream ships fix.
- 🟢 **Skip**: Performance/stability worse than alternativa (Obscura Rust binary 30 MB, 85ms claim) bez kompenzujícího benefitu.

Camofox jo-inc 2026-04-30 = 🟡 keep in radar (Cloudflare broken now, niche wins via CreepJS depth).

## Related

- Obscura (radar line 123) — Rust anti-detect, untested locally — head-to-head pending
- BrowserAct skills (radar) — alternativní authenticated scraping
- Default browser handler hijacking — Camofox jo-inc je SAFE (jen npm + bundled Firefox v node_modules), unlike Playwright MCP (per behavioral-genome.md Anti-patterns)

## When to re-evaluate

- daijro/camoufox ships > v135.0.1-beta.24
- jo-inc/camofox-browser closes 8 open `leak:native-memory` issues
- Cloudflare Turnstile bypass demonstrated working v upstream issue trackeru
- Windows ESM URL bug fixed (PR pro `pathToFileURL()` na plugin loaderu)

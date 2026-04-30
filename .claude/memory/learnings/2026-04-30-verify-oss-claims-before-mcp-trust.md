---
date: 2026-04-30
type: best_practice
severity: medium
component: skill
tags: [tool-evaluation, mcp-trust, oss-verification, third-party-mcp, gdpr, radar]
summary: "Při evaluaci třetí-stranných MCP serverů, které proxují OAuth-scoped API volání, ověř open-source claim přes `gh api repos/<owner>/<repo>` PŘED udělením scope. Toprank/NotFair tvrdil `nowork-studio/ads-agent` jako open-source backend; gh API vrátil 404 → closed-source proxy s 1y retencí OAuth refresh tokenu, brand-new entity, single founder, GDPR-light policy. Pro EU/GDPR uživatele = downgrade trust delta vs direct API client."
source: agent_generated
maturity: draft
confidence: 0.7
verify_check: "Grep('gh api repos/<owner>/<repo>', path='.claude/memory/learnings/') → 1+ matches"
skill_scope: [radar, improve]
---

# Verify open-source claims before trusting MCP servers with OAuth scopes

## Context

Pre-flight pro Toprank plugin pilot (NG-ROBOT, Czech NatGeo SEO/GSC fit). Toprank ships s Google Ads integrací přes NotFair MCP (`notfair.co/api/mcp`). Toprank README + downstream search results tvrdí backend je open-source na `nowork-studio/ads-agent`.

## Observation

```
$ gh api repos/nowork-studio/ads-agent --jq '.name'
{"message":"Not Found","documentation_url":"https://docs.github.com/rest","status":"404"}
gh: Not Found (HTTP 404)
```

Repo neexistuje veřejně. Backend je closed-source. Public claim broken.

Doplňující signály:
- `notfair.co` copyright 2026 (brand new)
- Single contact: `tong@notfair.co` (single founder)
- Privacy policy: 1y retention OAuth refresh tokenu, account IDs, email, IP, OS — žádná formal GDPR rights sekce
- Pricing: free 300 ops/mo → $79/mo Growth → $999/mo Managed (5% ad spend)

## Why it matters

Granting OAuth scope k třetí-stranné MCP která proxuje API:
- Auth tokens (refresh + access) → jejich server
- Query payloady (Google Ads campaign data, GSC search analytics) → jejich server
- Data retention → jejich policy

Pro EU/GDPR jurisdikci: closed-source proxy + minimal GDPR docs + single founder + new entity + 1y retention = elevated risk vs direct OAuth flow přes native gcloud/Google API client libraries.

## Pattern to apply

Před každou MCP server evaluací s OAuth-scoped access:

1. **Verify open-source claim:** `gh api repos/<owner>/<repo>` pro každé repo, které MCP označuje jako backend
2. **Check policy gap:** WebFetch privacy + terms; missing GDPR rights section + EU relevance = downgrade
3. **Check maintenance signals:** contact email count, copyright year, contributor count, recent commit activity
4. **Compare to direct integration:** většina OAuth API (Google Ads, GSC, GA4) má native client libraries — měř jestli MCP proxy přidává dost value aby vyvážil trust delta

Pokud 404 + closed-source + minimal GDPR + new entity → preferuj direct integration. Convenience "no API key to copy" zřídka převažuje trust delta pro production data.

## Application scope

Direct fit:
- `/radar` skill — MCP server evaluace
- `/improve` routing pro plugin candidates s OAuth scope
- Plugin pilots vyžadující OAuth (Google APIs, Microsoft Graph, atd.)

Not directly applicable:
- Local-only MCPs bez proxy — risk profile differs
- Internal/company MCPs — different trust model
- Read-only public-API MCPs (no auth) — niche risk

## References

- Pre-flight artifact: `~/Documents/000_NGM/NG-ROBOT/.claude/memory/toprank-pilot-handoff.md`
- Radar entry: `.claude/memory/radar.md` line 139 (downgraded 7→6 based on tato finding)
- Toprank README claim: `https://github.com/nowork-studio/toprank` (search MCP/NotFair sections)
- NotFair privacy: `https://notfair.co/privacy` (fetched 2026-04-30)

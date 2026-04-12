---
name: feedback_marketplace
description: Don't remove marketplace config from target projects — keep for future auto-update even if skills exist locally
type: feedback
---

Neodstraňuj marketplace/plugin config z cílových projektů, i když skills jsou lokálně ze syncu. Nech pro budoucí auto-update.

**Why:** Uživatel preferuje mít oba kanály (lokální skills + marketplace fallback) pro robustnost.
**How to apply:** Při úpravách settings.json cílových projektů nikdy neodstraňuj extraKnownMarketplaces/enabledPlugins sekce.

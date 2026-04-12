---
name: approval_fatigue
description: User finds step-by-step approval annoying, wants more autonomous agent operation
type: feedback
---

Krokové schvalování (permission prompts) uživatele otravuje.

**Why:** Chce plynulý workflow bez neustálého potvrzování. Zajímá se o agenty běžící autonomně mimo sessions (24/7).

**How to apply:**
- Preferuj `bypassPermissions` / `auto` mode kde je to bezpečné
- Navrhuj batch operace místo jednotlivých kroků
- Při orchestraci: neptej se na každý subtask zvlášť, ptej se jen na high-level plán
- Sleduj NemoClaw/OpenClaw jako cestu k async autonomous agentům
- Když je potřeba schválení, seskup víc akcí do jednoho dotazu
- **Po dokončení úkolu: rovnou commitni a pushni** — neptej se "Chceš commitnout?" když je práce hotová a plán schválený. Uživatel řekne sám, pokud nechce.

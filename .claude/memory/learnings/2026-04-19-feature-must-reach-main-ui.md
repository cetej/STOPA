---
date: 2026-04-19
type: anti_pattern
severity: high
component: orchestration
tags: [feature-completeness, ui, verification, dead-code]
summary: Nová feature (backend + standalone page) není hotová dokud není dostupná z hlavní navigace projektu. Bez linku/pillu/entry-pointu z hlavního UI je feature mrtvá — user ji nenajde.
source: user_correction
uses: 1
harmful_uses: 0
successful_uses: 0
confidence: 0.95
maturity: draft
task_context: {task_class: feature, complexity: medium, tier: standard}
verify_check: "manual"
---

## Pattern: Feature musí dosáhnout do hlavního UI

### Kontext
Dodal jsem 8 sprintů pro MONITOR — kompletní intel pipeline od feedů přes
scoring po 2D/3D vizualizaci + REST API. Commitnul jsem a pushnul na main.
Uživatel: "A s tím, že se změny mají propsat do UI projektu s tím si asi
nepočítal že?"

Měl pravdu. Intel stránky `/intel` a `/intel-globe` byly funkční, ale
**z hlavního dashboardu (`jarvis.html`) na ně nevedl žádný odkaz**.
User by je našel jen přes přímou URL, což nikdo nedělá.

### Chyba
"Hotovo" = funkcionalita + atestace + commit + push. ALE také:
**integrace s existujícím UI** je součást "hotovo", ne bonus.

Udělal jsem standalone stránky + server routes + unit testy + push.
Všechno pracovalo. Ale feature byla z pohledu uživatele **neviditelná**
do té doby, než jsem přidal `<a href="/intel">INTEL</a>` do topbaru.

### Proč se to stalo
- Nekontroloval jsem "journey user": otevře `/` → co uvidí? Jak se dostane na novou feature?
- Dashboard (`jarvis.html` = 52 KB) byl "tabu zóna" — bál jsem se tam zasahovat
- Standalone stránky s routes vypadaly jako "kompletní" řešení, ale nebyly v context uživatele

### Checklist před "hotovo" u UI features

1. **Link v hlavní nav?** Přidal jsem menu/button/pill/tab do hlavního UI?
2. **Objevitelnost:** Může uživatel feature najít bez znalosti URL?
3. **Live data v hlavním UI?** Pokud feature produkuje dynamický signál
   (score, počet, status), zobrazit summary také v hlavním dashboardu
   (ne jen na detailní stránce)
4. **Vizuální konzistence:** Nová komponenta používá stejné design tokens
   (fonty, barvy, border style) jako zbytek?
5. **Cross-link:** Z feature zpět na hlavní dashboard (breadcrumb / logo)?

### Jak aplikovat
- U každého nového route vždy parallelně editnout hlavní HTML aby obsahovalo
  link/entry-point
- Pokud máš API endpoint, přidat live ukazatel (pill, badge) do topbaru
  hlavní stránky — uživatel vidí hodnotu bez nutnosti klikat
- Před commitem: otevřít hlavní `/` a zeptat se "Najde to uživatel?"

### Anti-vzor v praxi
```
✗ ŠPATNĚ: commit "feat: add /intel-globe 3D visualization" bez linku z /
✓ SPRÁVNĚ: commit obsahuje i edit jarvis.html s odkazem na nový route
```

### Kdy tohle NEplatí
- Backend-only modul (no user-facing UI) → nepotřebuje navigaci
- Admin/debug stránky skryté za feature flag → OK
- Hidden by design (např. /healthz) → OK

---
name: Preview Hub — stav implementace
description: Centrální editor z Náhled tabu — drawer, media panel, image editor modal. Fáze 1-3 hotové.
type: project
---

## Preview Hub — stav k 2026-04-06

### Hotové fáze

**Fáze 1: Foundation** — event bus, modal manager, drawer shell
**Fáze 2: Media Panel** — obrázky/videa/audio v draweru, badges, margin management
**Fáze 3: Image Editor Modal** — klik na obrázek v preview body otevře editor modal (caption, credit, AI regenerace, file replace)

### Nové soubory (Fáze 1-3)
- `static/js/article/preview-hub.js` — PreviewHub event bus (on/off/emit + state)
- `static/js/article/modal-manager.js` — ModalManager (open/close/stack/ESC, inline style fallback)
- `static/js/article/media-drawer.js` — MediaDrawer (expand/collapse, rail, margin adjust)
- `static/js/article/media-panel.js` — MediaPanel (renderImages/Videos/Audio, badges, insert)
- `static/js/article/image-editor-modal.js` — ImageEditorModal (click-to-edit obrázků v preview body)
- `templates/partials/preview/media-drawer.html` — drawer HTML (rail + 4 panely)
- `static/css/preview-hub.css` — drawer, modal, media panel, image editor CSS

### Modifikované soubory
- `templates/article_detail.html` — CSS link, drawer include, 5 script tagů, PreviewHub init s media daty
- `static/js/article/shared.js` — switchTab() toggluje drawer visibility + margin reset
- `blueprints/articles_bp.py` — nový endpoint `/api/article/images/upload` (nahrazení obrázku souborem)

### Architektonické vzory
- **Data flow:** Jinja2 → `window._mediaCaptions` + `PreviewHub.init({images, socialVideos, ...})` → MediaPanel renders
- **Drawer margin:** Expanded → `gridTemplateColumns: '1fr 280px'` + `marginRight: 456px`. Collapsed → reset.
- **Tab awareness:** Drawer viditelný POUZE v preview tabu (switchTab toggle)
- **Event bus:** `PreviewHub.emit('media:updated', ...)` → badge update, `PreviewHub.emit('image:edited', ...)` → media refresh
- **Image editor:** Click na `figure.preview-image:not(.preview-hero)` → `ModalManager.open('image-editor', ...)` → caption/credit edit, AI generate, file replace

### Zbývající fáze (viz plán noble-gliding-planet.md)
- Fáze 4: Generování médií z preview
- Fáze 5: Video + Podcast z preview
- Fáze 6: YouTube Short Clips (nová funkce)
- Fáze 7: Polish

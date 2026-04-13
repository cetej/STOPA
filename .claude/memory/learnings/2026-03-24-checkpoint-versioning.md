---
date: 2026-03-18
type: anti_pattern
severity: high
component: memory
tags: [checkpoint, versioning, session-continuity]
summary: "Never overwrite checkpoints without archiving. Version frequently, especially before scope changes."
source: auto_pattern
uses: 2
confidence: 0.9
---

# Checkpoint Versioning — Never Overwrite Without Archive

Dělej checkpointy ČASTĚJI a VERZUJ je.

**Problém**: Předchozí konverzace vyčistila checkpoint a ztratil se kontext pro další session.

**Pravidla**:
- Na začátku session: ihned checkpoint s aktuálním stavem
- Po každém dokončeném bloku: aktualizuj checkpoint
- Checkpoint NIKDY nemazat — přepsat jen aktuální, staré archivovat
- Checkpoint musí obsahovat: task list, technické poznatky, resume prompt

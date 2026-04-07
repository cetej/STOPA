---
name: Operational Rhythm Pattern
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [chief-of-staff-openclaw]
tags: [orchestration, session, memory]
---

# Operational Rhythm Pattern

> Scheduled daily structure via cron: morning brief (9am) and evening wrap (6pm) delivered via messaging channel. "If nothing needs attention, silence."

## Key Facts

- Morning brief: top priorities, overdue tasks, today's calendar, anything needing attention before opening laptop (ref: sources/chief-of-staff-openclaw.md)
- Evening wrap: what happened, what stalled, what to prep for tomorrow (ref: sources/chief-of-staff-openclaw.md)
- Delivery channel: WhatsApp (could be any messaging API) (ref: sources/chief-of-staff-openclaw.md)
- Signal discipline: "If there's nothing to say, I hear nothing" — silence = OK, no noise for noise's sake (ref: sources/chief-of-staff-openclaw.md)
- Pattern flag: if task rolled forward 5 days in a row → explicit flag (ref: sources/chief-of-staff-openclaw.md)
- "This is the piece that makes it feel like working with a chief of staff rather than using a tool" (ref: sources/chief-of-staff-openclaw.md)

## Relevance to STOPA

STOPA has `/status` (on-demand) and scheduled tasks but no daily operational rhythm skill. Morning brief + evening wrap = structured cadence that STOPA's scheduled-tasks infrastructure could implement (cron + Telegram). Signal discipline (silence when nothing) is a design principle worth capturing for any STOPA notification system.

## Mentioned In

- [How I Built a Chief of Staff on OpenClaw](../sources/chief-of-staff-openclaw.md)

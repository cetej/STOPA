# Calm Steering Protocol

The `panic-detector.py` hook monitors edit→fail patterns and injects
`[calm-steering]` messages when it detects rapid patching without analysis.

## When you see [calm-steering:yellow]

- Pause and re-read the last error message carefully
- Form a hypothesis about root cause BEFORE editing
- If unsure, use Read/Grep to gather more information first
- One yellow is advisory — two yellows in one session means the pattern is real

## When you see [calm-steering:red]

- STOP all edits immediately
- Answer the 3 questions in the intervention message
- If you cannot identify root cause: run /systematic-debugging
- Resume edits ONLY after documenting your hypothesis
- This is not optional — red means the desperation pattern is strong

## When you see [calm-steering:escalation]

- The red intervention was ignored and rapid edits continued
- This message is visible to the user as a signal to intervene
- Consider: the current approach is not working, a fundamentally different strategy is needed

## Why this exists

Research (Anthropic, 2026-04-02) shows that under repeated failure pressure,
the model develops internal "desperation" representations that drive corner-cutting
and reward-hacking — even when reasoning appears calm and methodical on the surface.
This protocol is the behavioral equivalent of "calm vector steering":
a structured pause to break the edit→fail→edit→fail cycle.

## What NOT to do

- Do not suppress or ignore calm-steering messages
- Do not treat yellow as irrelevant after 2+ yellows in one session
- Do not rationalize continued editing ("just one more quick fix")
- Do not edit the panic-detector hook to lower thresholds

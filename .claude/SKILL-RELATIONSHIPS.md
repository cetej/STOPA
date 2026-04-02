# Skill Relationships — Dependency & Handoff Graph

How skills chain, delegate, and exclude each other.

## Orchestration Chain (top-down)

```
triage ──→ orchestrate ──→ [subtask skills]
                │
                ├──→ scout (Phase 1: exploration)
                ├──→ critic (Phase 5: review)
                ├──→ verify (Phase 6: proof)
                ├──→ checkpoint (auto on health score 3+)
                └──→ compact (auto on health score 5+)
```

## Research Chain

```
deepresearch ──→ fetch (URL extraction)
             ──→ browse (authenticated pages)
             ──→ youtube-transcript (video sources)

liveprompt ──→ fetch (community forums)

watch ──→ fetch (news sources)
      ──→ scribe (save findings to news.md)
```

## Quality Chain (post-edit)

```
[code edit] ──→ critic ──→ scribe (capture learnings)
                       ──→ verify (if critic passes)

pr-review ──→ critic (per-file review)
          ──→ security-review (if security-tagged)

peer-review (independent — for documents, not code)
```

## Optimization Loops

```
autoloop ──→ critic (per-iteration quality check)
         ──→ eval (trace grading)

autoresearch ──→ eval (experiment metrics)

self-evolve ──→ eval (eval-case grading)
            ──→ autoloop (inner optimization loop)

autoreason (self-contained debate loop, no dependencies)
```

## Issue Resolution

```
fix-issue ──→ scout (understand codebase)
          ──→ critic (review fix)
          ──→ verify (prove it works)

autofix ──→ fix-issue (apply fix)
        ──→ critic (review)

incident-runbook ──→ systematic-debugging (root cause)
                 ──→ scout (explore affected area)
```

## Session Management

```
checkpoint ←── orchestrate (auto-save)
           ←── compact (context relief)

handoff ──→ scribe (persist findings to memory)

prp ──→ checkpoint (package context for handoff)

status ──→ budget (cost data)
       ──→ checkpoint (session state)
```

## Build & Project

```
build-project ──→ brainstorm (Phase 1: spec)
              ──→ scout (Phase 2: exploration)
              ──→ orchestrate (Phase 3+: execution)
              ──→ critic (Phase N: review)

project-init ──→ skill-generator (if custom skills needed)

project-sweep ──→ [any skill] × [all projects]
```

## Mutual Exclusions (Do NOT use X for Y)

| If you need... | Use | NOT |
|---------------|-----|-----|
| Code review | critic | pr-review (that's for PRs) |
| PR review | pr-review | critic (that's for code) |
| Document review | peer-review | critic or pr-review |
| Codebase search | scout | deepresearch (that's for web) |
| Web research | deepresearch | scout (that's for code) |
| Community prompts | liveprompt | watch (that's for news) |
| Ecosystem news | watch | liveprompt (that's for prompts) |
| File optimization | autoloop | autoresearch (that's for experiments) |
| Code experiments | autoresearch | autoloop (that's for files) |
| Skill improvement | self-evolve | autoloop (that's for files) |
| Text improvement | autoreason | autoloop (that's for metrics) |
| Quick fix | direct edit | orchestrate (overkill) |
| Session save | checkpoint | handoff (that's for cross-session) |

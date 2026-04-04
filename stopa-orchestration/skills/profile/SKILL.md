---
name: profile
description: "Use when entering a new project or onboarding to detect tech stack and recommend relevant STOPA skills. Trigger on 'profile', 'what stack', 'jaký stack', 'recommend skills', 'doporuč skills', 'onboard'. Do NOT use for task routing (/triage) or codebase exploration (/scout)."
argument-hint: [project-path] [--json]
tags: [exploration, orchestration, planning]
phase: define
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash
model: haiku
effort: low
maxTurns: 8
deny-tools: Write, Edit, Agent
---

# Profile — Project Stack Detector & Skill Recommender

Scan a project directory, detect technologies, and recommend the most relevant STOPA skills.
Inspired by midudev/autoskills static mapping approach — no API, no ML, just config file scanning.

## Arguments

- `[project-path]` — directory to scan (default: current working directory)
- `--json` — output structured JSON instead of markdown

## Phase 1: Detect Technologies

Scan the project root for these indicators. Check ALL categories — don't stop at first match.

### Detection Map

| Technology | Detection Method |
|-----------|-----------------|
| **Python** | `pyproject.toml`, `setup.py`, `requirements.txt`, `Pipfile`, `*.py` in root |
| **JavaScript/Node** | `package.json`, `node_modules/`, `.nvmrc` |
| **TypeScript** | `tsconfig.json`, `*.ts` files |
| **React** | package.json deps: `react`, `react-dom` |
| **Next.js** | package.json deps: `next`, `next.config.*` |
| **Vue** | package.json deps: `vue`, `nuxt` |
| **Svelte** | package.json deps: `svelte`, `@sveltejs/kit` |
| **Astro** | package.json deps: `astro`, `astro.config.*` |
| **Angular** | package.json deps: `@angular/core`, `angular.json` |
| **FastAPI** | pyproject.toml/requirements: `fastapi` |
| **Django** | `manage.py`, `settings.py`, pyproject.toml: `django` |
| **Flask** | pyproject.toml/requirements: `flask` |
| **Express** | package.json deps: `express` |
| **Hono** | package.json deps: `hono` |
| **NestJS** | package.json deps: `@nestjs/core` |
| **Rust** | `Cargo.toml` |
| **Go** | `go.mod` |
| **Java/Kotlin** | `build.gradle`, `pom.xml`, `*.kt` in `src/` |
| **Swift** | `Package.swift`, `*.xcodeproj` |
| **Docker** | `Dockerfile`, `docker-compose.yml` |
| **Terraform** | `*.tf` files |
| **Prisma** | `prisma/schema.prisma`, package.json: `prisma` |
| **Drizzle** | package.json: `drizzle-orm` |
| **SQLAlchemy** | pyproject.toml/requirements: `sqlalchemy` |
| **Supabase** | package.json: `@supabase/supabase-js`, `.env*` with SUPABASE |
| **Tailwind** | `tailwind.config.*`, package.json: `tailwindcss` |
| **Playwright** | package.json: `playwright`, `@playwright/test` |
| **Pytest** | pyproject.toml: `pytest`, `conftest.py` |
| **Vitest** | package.json: `vitest` |
| **Jest** | package.json: `jest`, `jest.config.*` |
| **CI/CD** | `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` |
| **Monorepo** | `pnpm-workspace.yaml`, `lerna.json`, `turbo.json`, `nx.json` |
| **Stripe** | package.json/pyproject: `stripe` |
| **Remotion** | package.json: `remotion`, `@remotion/*` |
| **Expo** | package.json: `expo` |
| **Tauri** | `src-tauri/`, package.json: `@tauri-apps/api` |
| **Electron** | package.json: `electron` |
| **fal.ai** | package.json/pyproject: `fal-client`, env: `FAL_KEY` |
| **Claude API** | package.json: `@anthropic-ai/sdk`, pyproject: `anthropic` |

### Detection Procedure

```
1. Glob for config files: package.json, pyproject.toml, Cargo.toml, go.mod, etc.
2. If package.json exists: Read it, extract dependencies + devDependencies keys
3. If pyproject.toml exists: Read it, extract [project.dependencies] and [tool.*] sections
4. If Cargo.toml exists: Read it, extract [dependencies]
5. Check for framework-specific config files (next.config.*, astro.config.*, etc.)
6. Check for CI/CD configs
7. Check for monorepo indicators
8. Check .env* files for service indicators (SUPABASE_URL, STRIPE_KEY, FAL_KEY, etc.)
   — read ONLY key names, NEVER values
```

## Phase 2: Combo Detection

After individual technologies, check for synergistic combinations:

| Combo | Detected When | Extra Insight |
|-------|--------------|---------------|
| **Full-stack JS** | React/Vue/Svelte + Express/Hono/NestJS | Frontend + backend in one repo |
| **Python API** | FastAPI/Django/Flask + SQLAlchemy/Prisma | API with ORM |
| **Monorepo** | turbo/nx/pnpm-workspace + 2+ packages | Multi-package coordination |
| **Testing stack** | Playwright + Vitest/Jest/Pytest | E2E + unit coverage |
| **AI-powered app** | Claude API / fal.ai + any framework | AI integration patterns |
| **Infra-heavy** | Docker + Terraform/CI + any backend | DevOps-oriented project |

## Phase 3: Skill Recommendations

Map detected technologies to STOPA skills using this priority matrix:

### Universal Skills (always recommend)

| Skill | Phase | Why Always |
|-------|-------|-----------|
| `/orchestrate` | plan | Multi-step task coordination |
| `/critic` | verify | Post-edit quality check |
| `/checkpoint` | ship | Session continuity |

### Technology-Specific Recommendations

| Detected | Recommended Skills | Reason |
|----------|-------------------|--------|
| Python | `/tdd`, `/systematic-debugging` | Python testing + debugging methodology |
| TypeScript/JS | `/tdd`, `/dependency-audit` | Type safety + dependency health |
| React/Vue/Svelte/Angular | `/browse`, `/scenario` | UI testing, edge cases |
| Next.js/Nuxt/Astro | `/browse`, `/seo-audit` | SSR verification, SEO |
| FastAPI/Express/Hono/NestJS | `/security-review`, `/verify` | API trust boundaries |
| Django/Flask | `/security-review`, `/tdd` | Web security + tests |
| Prisma/Drizzle/SQLAlchemy | `/scenario` | Migration edge cases |
| Docker/Terraform | `/incident-runbook` | Infra failure diagnosis |
| CI/CD | `/autofix`, `/harness` | CI repair + deterministic pipelines |
| Playwright/Pytest/Vitest | `/tdd`, `/harness`, `/eval` | Test methodology + regression detection |
| Monorepo | `/xsearch`, `/project-sweep` | Cross-package coordination |
| Stripe | `/security-review` | Payment trust boundaries |
| Claude API / fal.ai | `/claude-api`, `/autoresearch` | API best practices + experimentation |
| Remotion | `/verify`, `/browse` | Video output verification |

### Combo Recommendations

| Combo | Extra Skills | Reason |
|-------|-------------|--------|
| Full-stack JS | `/pr-review` | Multi-perspective review across layers |
| Python API + ORM | `/peer-review`, `/scenario` | Migration review + edge cases |
| Monorepo | `/orchestrate` (deep tier) | Cross-package changes need orchestration |
| Testing stack | `/self-evolve`, `/eval` | Test quality improvement loop |
| AI-powered | `/autoresearch`, `/autoloop` | Iterative AI optimization |
| Infra-heavy | `/incident-runbook`, `/systematic-debugging` | Ops methodology |

## Phase 4: Output

### Markdown Output (default)

```markdown
## Project Profile: <project-name>

### Detected Stack
| Category | Technologies |
|----------|-------------|
| Language | Python 3.12, TypeScript |
| Framework | FastAPI, React |
| Database | PostgreSQL (via SQLAlchemy) |
| Testing | Pytest, Playwright |
| Infra | Docker, GitHub Actions |
| Services | Supabase, Stripe |

### Combos Detected
- Python API (FastAPI + SQLAlchemy)
- Testing stack (Pytest + Playwright)

### Recommended Skills (prioritized)

#### Always Active
- `/orchestrate` — multi-step coordination
- `/critic` — quality review
- `/checkpoint` — session state

#### For This Project
1. `/tdd` — Python testing methodology (pytest detected)
2. `/security-review` — API + Stripe trust boundaries
3. `/scenario` — SQLAlchemy migration edge cases
4. `/autofix` — CI pipeline repair (GitHub Actions detected)
5. `/systematic-debugging` — root cause methodology

#### Consider Also
- `/dependency-audit` — 127 npm packages, 45 pip packages detected
- `/harness` — deterministic test pipeline from Playwright + Pytest
```

### JSON Output (--json)

```json
{
  "project": "<name>",
  "technologies": [
    {"id": "python", "version": "3.12", "confidence": "high"},
    {"id": "fastapi", "confidence": "high"},
    {"id": "react", "confidence": "high"}
  ],
  "combos": ["python-api", "testing-stack"],
  "skills": {
    "always": ["orchestrate", "critic", "checkpoint"],
    "recommended": ["tdd", "security-review", "scenario", "autofix"],
    "consider": ["dependency-audit", "harness"]
  }
}
```

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll just recommend all Tier 1 skills" | Generic recommendations add no value over /status | Tailor to detected stack — skip irrelevant skills |
| "I don't need to scan config files, I can guess from the directory name" | Directory names lie (e.g., "api" could be Python or Node) | Always read actual config files for evidence-based detection |
| "This .env file might have useful info" | Reading .env values is a security risk | Read ONLY key names from .env, NEVER values |
| "I'll skip combo detection since individual skills cover it" | Combos reveal architectural patterns that change recommendations | Always run combo detection after individual scanning |

## Red Flags

STOP and re-evaluate if any of these occur:
- Recommending more than 8 skills (too many = no prioritization)
- Recommending skills that require tools the project doesn't use (e.g., `/seo-audit` for a CLI tool)
- Reading .env values instead of just key names
- Spending more than 3 turns on detection (should be fast)

## Verification Checklist

- [ ] At least 1 config file was actually read (not just globbed)
- [ ] Recommendations reference specific detected technologies (not generic)
- [ ] No more than 8 recommended skills (3 always + max 5 specific)
- [ ] .env values were NOT read or exposed
- [ ] Output includes both categories and confidence levels

## Rules

1. **Fast scan** — profile should complete in <30 seconds, max 8 turns
2. **Evidence-based** — every technology listed must trace back to a config file or dependency
3. **No .env values** — only key names for service detection (SUPABASE_URL → "Supabase detected")
4. **Prioritize** — don't dump all 49 skills. Top 5-8 for this specific project.
5. **No execution** — profile only recommends. Never install, configure, or modify anything.
6. **Confidence levels** — "high" (explicit in config), "medium" (inferred from patterns), "low" (heuristic guess)

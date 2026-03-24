# Codebase Knowledge Graph — Reference Schema

Referenční schema pro budoucí codebase indexing v cílových projektech (NG-ROBOT, ADOBE-AUTOMAT).
Inspirováno projektem [Understand-Anything](https://github.com/Lum1104/Understand-Anything).

## Kdy použít

- Při budování `/scout` output ve strukturovaném JSON formátu
- Při implementaci codebase indexing pro velké projekty (200+ souborů)
- Jako základ pro knowledge graph, nad kterým běží dotazy

## Node Types (5)

| Type | ID Convention | Popis |
|------|---------------|-------|
| `file` | `file:<relative-path>` | Soubor v projektu |
| `function` | `func:<relative-path>:<name>` | Funkce/metoda |
| `class` | `class:<relative-path>:<name>` | Třída |
| `module` | `module:<name>` | Logický modul (npm balíček, Python modul) |
| `concept` | `concept:<name>` | Abstraktní koncept (auth, caching, routing) |

### Node Properties

```json
{
  "id": "file:src/auth/jwt.ts",
  "type": "file",
  "name": "jwt.ts",
  "filePath": "src/auth/jwt.ts",
  "lineRange": [1, 142],
  "summary": "JWT token generation and validation middleware",
  "tags": ["auth", "middleware", "security"],
  "complexity": "moderate",
  "languageNotes": "Uses generic type constraints for payload validation"
}
```

- `complexity`: `simple` | `moderate` | `complex`
- `tags`: semantic labels, volná forma
- `summary`: 1-2 věty, plain English, LLM-generované
- `lineRange`: `[startLine, endLine]` (pro function/class nodes)

## Edge Types (18)

### Structural (5)
| Type | Popis | Příklad |
|------|-------|---------|
| `imports` | A importuje z B | `file:routes.ts` → `file:jwt.ts` |
| `exports` | A exportuje symbol z B | `file:index.ts` → `func:jwt.ts:verify` |
| `contains` | A obsahuje B | `file:jwt.ts` → `func:jwt.ts:generateToken` |
| `inherits` | A dědí z B | `class:AdminUser` → `class:BaseUser` |
| `implements` | A implementuje interface B | `class:JwtAuth` → `concept:AuthProvider` |

### Behavioral (4)
| Type | Popis |
|------|-------|
| `calls` | A volá funkci z B |
| `subscribes` | A naslouchá na event z B |
| `publishes` | A emituje event pro B |
| `middleware` | A je middleware chain pro B |

### Data Flow (4)
| Type | Popis |
|------|-------|
| `reads_from` | A čte data z B (DB, file, API) |
| `writes_to` | A zapisuje data do B |
| `transforms` | A transformuje data z B |
| `validates` | A validuje data pro B |

### Dependencies (3)
| Type | Popis |
|------|-------|
| `depends_on` | A závisí na B (runtime) |
| `tested_by` | A je testováno v B |
| `configures` | A konfiguruje chování B |

### Semantic (2)
| Type | Popis |
|------|-------|
| `related` | A a B se týkají stejného konceptu |
| `similar_to` | A a B mají podobnou implementaci |

### Edge Properties

```json
{
  "source": "file:src/routes/api.ts",
  "target": "file:src/auth/jwt.ts",
  "type": "imports",
  "direction": "forward",
  "weight": 0.8,
  "description": "Imports verifyToken for route protection"
}
```

- `direction`: `forward` | `backward` | `bidirectional`
- `weight`: `0.0` – `1.0` (síla vazby, pro layout a ranking)

## Top-Level Graph Structure

```json
{
  "version": "1.0.0",
  "project": {
    "name": "my-project",
    "languages": ["typescript", "python"],
    "frameworks": ["express", "react"],
    "description": "E-commerce platform",
    "analyzedAt": "2026-03-24T12:00:00Z",
    "gitCommitHash": "abc123"
  },
  "nodes": [],
  "edges": [],
  "layers": [
    {
      "id": "api",
      "name": "API Layer",
      "description": "HTTP endpoints and route handlers",
      "nodeIds": ["file:src/routes/api.ts", "file:src/routes/auth.ts"]
    }
  ],
  "tour": [
    {
      "order": 1,
      "title": "Entry Point",
      "description": "Start here — the main server setup",
      "nodeIds": ["file:src/index.ts"]
    }
  ]
}
```

## Architectural Layers (standard set)

| Layer | Popis | Typické patterny |
|-------|-------|-----------------|
| `api` | HTTP endpoints, route handlers | Express routes, FastAPI endpoints |
| `service` | Business logic | Use cases, services, controllers |
| `data` | Persistence, DB access | Repositories, ORM models, migrations |
| `ui` | Frontend components | React components, templates |
| `utility` | Shared helpers | Utils, formatters, validators |
| `config` | Configuration | Env vars, settings, constants |
| `test` | Test files | Unit tests, integration tests |

## Použití v STOPA kontextu

### Pro `/scout` structured output
Scout může generovat lightweight verzi grafu (jen `file` nodes + `imports` edges) jako JSON pro lepší strojové zpracování výsledků průzkumu.

### Pro `/critic` diff impact trace
Critic používá subset tohoto schema — `imports` edges pro 1-hop dependency trace z `git diff --name-only`.

### Pro `/orchestrate` findings ledger
Agenti píšou intermediate JSON do `.claude/memory/intermediate/` — ne plný graf, ale strukturovaný výstup kompatibilní se schema.

### Plný knowledge graph (future)
Kompletní implementace (všech 5 node types, 18 edge types, layers, tours) je kandidát pro dedicated `/understand` skill. Zatím používáme jen relevantní subset per-skill.

## Zdroj

Analyzováno z: `Lum1104/Understand-Anything` (v1.1.1, 2026-03)
- Skills jsou pure markdown (LLM-orchestrated, ne TypeScript runtime)
- Core: TypeScript + tree-sitter (WASM) + Fuse.js + Zod
- Dashboard: React 19 + React Flow + Zustand + Dagre
- Neinstalujeme jako plugin — cherry-pickujeme schema a vzory

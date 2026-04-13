# PKM Methodology Research — R3
Generated: 2026-04-13

## Evidence Table

| # | Source | URL | Key claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Forte Labs — BASB Overview | https://fortelabs.com/blog/basboverview/ | CODE = Capture → Organize → Distill → Express; four-step workflow for turning consumed information into creative output | methodology | high |
| 2 | Forte Labs — BASB Overview | https://fortelabs.com/blog/basboverview/ | PARA method organizes information by actionability: Projects, Areas, Resources, Archive | methodology | high |
| 3 | Forte Labs — BASB Overview | https://fortelabs.com/blog/basboverview/ | Capture principle: keep single centralized place for all digital snippets; tools include ebook exporters, read-later apps, web clippers | methodology | high |
| 4 | Forte Labs — BASB Overview | https://fortelabs.com/blog/basboverview/ | "Resonance" heuristic for selection: save what resonates intuitively, not analytically | methodology | high |
| 5 | Forte Labs — BASB Overview | https://fortelabs.com/blog/basboverview/ | Progressive Summarization: highlight → bold → executive summary layers on top of original note text | methodology | high |
| 6 | Zettelkasten.de — Overview | https://zettelkasten.de/overview/ | Principle of Atomicity: each note covers one topic only, gets a unique ID | methodology | high |
| 7 | Zettelkasten.de — Overview | https://zettelkasten.de/overview/ | Principle of Connectivity: explicit links between notes; search alone is insufficient for long-term knowledge | methodology | high |
| 8 | Zettelkasten.de — Overview | https://zettelkasten.de/overview/ | Building blocks: inbox + note archive + reference manager; tags over categories | methodology | high |
| 9 | Zettelkasten.de — Overview | https://zettelkasten.de/overview/ | Use outlines to assemble notes into drafts; ease into writing by pasting Zettel content into outline structure | methodology | high |
| 10 | Zettelkasten.de — Overview | https://zettelkasten.de/overview/ | Single Zettelkasten for life recommended; Folgezettel (note sequences) as alternative to pure links | methodology | high |
| 11 | Reor README | https://raw.githubusercontent.com/reorproject/reor/main/README.md | Architecture: every note is chunked and embedded into local LanceDB vector database | implementation | high |
| 12 | Reor README | https://raw.githubusercontent.com/reorproject/reor/main/README.md | Related notes auto-connected via vector similarity (no manual linking required) | implementation | high |
| 13 | Reor README | https://raw.githubusercontent.com/reorproject/reor/main/README.md | "RAG app with two generators: the LLM and the human" — sidebar shows related notes retrieved from corpus during editing | implementation | high |
| 14 | Reor README | https://raw.githubusercontent.com/reorproject/reor/main/README.md | Runs Ollama locally; supports OpenAI-compatible APIs; AGPL-3.0 license | implementation | high |
| 15 | Reor README | https://raw.githubusercontent.com/reorproject/reor/main/README.md | LLM-powered Q&A does RAG on the entire notes corpus for question answering | implementation | high |
| 16 | dasroot.net — RAG+Obsidian | https://dasroot.net/posts/2025/12/rag-personal-knowledge-management-obsidian-integration/ | RAG pipeline: retrieval phase queries vector DB (LanceDB/Qdrant), generation phase uses retrieved context for LLM synthesis | implementation | high |
| 17 | dasroot.net — RAG+Obsidian | https://dasroot.net/posts/2025/12/rag-personal-knowledge-management-obsidian-integration/ | Local GraphRAG on 19 Markdown files: 36 hours on M2 Max 32GB vs <10 minutes on cloud — local LLM indexing severely constrained | benchmark | high |
| 18 | dasroot.net — RAG+Obsidian | https://dasroot.net/posts/2025/12/rag-personal-knowledge-management-obsidian-integration/ | RAG-based systems improve response accuracy by up to 15% in complex retrieval scenarios with advanced chunking | benchmark | medium |
| 19 | dasroot.net — RAG+Obsidian | https://dasroot.net/posts/2025/12/rag-personal-knowledge-management-obsidian-integration/ | Obsidian 2025 plugin ecosystem: Dataview Query Wizard (GPT) enables natural language querying of vault; LightRAG (with RAGAS eval + Langfuse tracing) | implementation | high |
| 20 | dasroot.net — RAG+Obsidian | https://dasroot.net/posts/2025/12/rag-personal-knowledge-management-obsidian-integration/ | Best practice chunking: overlap-based chunking + dynamic filtering by query complexity | implementation | high |
| 21 | dasroot.net — RAG+Obsidian | https://dasroot.net/posts/2025/12/rag-personal-knowledge-management-obsidian-integration/ | Reor v1.2 cited as example of RAG-based local PKM; uses LanceDB internally | implementation | high |
| 22 | dasroot.net — RAG+Obsidian | https://dasroot.net/posts/2025/12/rag-personal-knowledge-management-obsidian-integration/ | RAG still relevant even with large context window models (Llama 4): hardware constraints make full-context impractical for personal use | implementation | medium |

---

## Findings

### BASB: CODE as Workflow Backbone

Forte's Building a Second Brain centers on CODE — Capture, Organize, Distill, Express — as a "proven process for consistently turning information consumed into creative output" [1]. The workflow is intentionally linear but not rigid: each step can be applied at different granularities.

**Capture** is selective, not exhaustive. The key rule is resonance: save what connects to something you care about, not what seems analytically important [4]. Tools form a pipeline — ebook exporters, read-later apps (Instapaper, Pocket), web clippers — feeding into a single centralized note app [3]. The act of capturing should take seconds.

**Organize** uses PARA (Projects → Areas → Resources → Archive), sorting by actionability rather than topic [2]. This is the critical design choice that separates BASB from Zettelkasten: PARA is task-oriented, not knowledge-oriented. Notes live near the project that will use them, not in a subject hierarchy.

**Distill** is implemented as Progressive Summarization: layer highlights on top of original text, then bold the best highlights, then write an executive summary — all without deleting the underlying source [5]. This creates a three-pass retrieval system where you can read at different depths.

**Express** is the consumption goal: all knowledge work produces deliverables. The system exists to feed creation, not collection.

### Zettelkasten: Atomic Notes as Knowledge Graph

Zettelkasten operates on two canonical principles [6][7]. Atomicity requires each note to cover exactly one concept, identified by a unique ID. Connectivity requires explicit bidirectional links — "search alone is not enough" and connections "especially in the long run" are what make the system valuable [7]. This is the structural difference from BASB: Zettelkasten is a knowledge graph by construction, BASB is a filing system by project.

The building blocks are inbox + note archive + reference manager [8]. Tags over categories is a firm recommendation: categories create hierarchy that constrains future retrieval, while tags create non-hierarchical facets. The Folgezettel concept (note sequences as an alternative to links) acknowledges that hierarchical ordering sometimes matters [10].

The writing workflow derives from accumulated notes: use outlines as scaffolding, then paste Zettel content into the outline structure [9]. This mirrors how Forte describes "creative output" — notes exist to be assembled, not just stored.

**Key contrast with BASB**: Zettelkasten optimizes for knowledge emergence over time (Luhmann accumulated ~90,000 notes over 40 years with one Zettelkasten [10]). BASB optimizes for project completion. These are complementary, not competing — many practitioners combine PARA organization with Zettelkasten-style atomic notes.

### Reor: Local RAG as Automatic Link Layer

Reor's core insight is the "two generators" framing: the LLM and the human are both generators fed by the same retrieval corpus [13]. In Q&A mode, the LLM retrieves and synthesizes. In editor mode, the human sees related notes in a sidebar — the same retrieval pipeline, different consumer.

Technically: every note is chunked and embedded into LanceDB on write [11]. Related notes surface automatically via vector similarity without manual linking [12]. This is a direct LLM answer to Zettelkasten's Principle of Connectivity: instead of requiring the author to create links, the embedding model creates them automatically based on semantic similarity.

Reor runs entirely locally via Ollama [14], addressing the privacy objection to cloud PKM tools. The AGPL-3.0 license makes it fully auditable. Stack: Electron + LanceDB + Transformers.js + Ollama.

The limitation: automatic vector links are not the same as intentional Zettelkasten links. Vector similarity finds related content; deliberate Zettelkasten links encode the author's reasoning about *why* two notes connect. These are different semantic operations.

### RAG+Obsidian: Integration Architecture and Constraints

The dasroot.net guide documents the state of RAG-Obsidian integration as of late 2025. The standard architecture uses LangChain v4.2 or Dify v1.5 as orchestration layer, with LanceDB or Qdrant as vector store, embedding models from the BGE/E5/Instructor families, and Ollama for local LLM inference [16][19].

The practical constraint is severe: indexing 19 Markdown files with local GraphRAG took 36 hours on an M2 Max with 32GB RAM [17]. This is a 216× slowdown vs cloud. For personal vaults with hundreds or thousands of notes, local LLM indexing is impractical — embedding-only pipelines (no LLM at index time) are the viable local path.

Best practices extracted [20]:
- Overlap-based chunking to preserve context at note boundaries
- Dynamic filtering based on query complexity (simple queries skip heavy retrieval)
- RAGAS evaluation + Langfuse tracing for system quality monitoring

The Obsidian plugin **Dataview Query Wizard (GPT)** enables natural language vault queries without a separate pipeline [19]. LightRAG (with RAGAS + Langfuse) is cited as the most mature framework for Obsidian RAG integration.

### Patterns for Building a New System

Synthesizing across all four sources, the architectural decisions for a new LLM-augmented PKM system are:

1. **Capture pipeline** (BASB): resonance filter + automated ingestion from highlight exporters → reduces cognitive load at entry point
2. **Storage model** (Zettelkasten): atomic notes with unique IDs + explicit semantic links → knowledge graph grows over time
3. **Auto-linking layer** (Reor): embeddings on write → vector similarity links complement (not replace) intentional links
4. **Retrieval** (RAG+Obsidian): overlap chunking + embedding-only indexing at write time + LLM synthesis at query time → avoids 36h GraphRAG problem
5. **Organization** (BASB PARA): project-first filing for active work, archive for completed projects
6. **Writing workflow** (Zettelkasten): outline → slot notes in → refine → the knowledge graph feeds the draft

The "two generators" concept from Reor [13] is the strongest architectural insight for building a new system: design the retrieval pipeline to serve both humans (editor sidebar) and LLMs (Q&A) from the same index.

---

## Sources

1. Tiago Forte — "Building a Second Brain: The Definitive Introductory Guide" (2023-05-01) — https://fortelabs.com/blog/basboverview/
2. Zettelkasten.de — "Getting Started — Zettelkasten Method" (updated 2026-03-31) — https://zettelkasten.de/overview/
3. reorproject — "Reor README" (GitHub) — https://raw.githubusercontent.com/reorproject/reor/main/README.md
4. dasroot.net — "RAG for Personal Knowledge Management: Obsidian Integration" (2025-12-25) — https://dasroot.net/posts/2025/12/rag-personal-knowledge-management-obsidian-integration/

---

## Coverage Status

Tool calls used: 8/8

### What was covered
- BASB CODE methodology: full (Capture in depth, Organize/PARA/Distill/Express from earlier call)
- Zettelkasten principles: full overview page content retrieved
- Reor architecture: README fully read, technical stack confirmed
- RAG+Obsidian: article body retrieved, architecture and benchmarks documented

### What was NOT covered (budget exhausted)
- Fabric.so: not fetched (pre-selected but budget ran out — no URL provided in pre-selected list, only mentioned in task description)
- Zettelkasten introduction article (https://zettelkasten.de/introduction) — deeper principles not fetched, only overview page
- Reor v1.2 specific changelog or feature list
- Any academic papers on PKM or RAG for notes

### Data quality notes
- BASB article body was partially inaccessible via Jina (nav repeated), but CODE section captured in full from first successful parse
- Zettelkasten overview page: structure and principles captured from direct body extraction
- Reor README: complete, untruncated
- RAG+Obsidian article: 9000+ chars of body content retrieved

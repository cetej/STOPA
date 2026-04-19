---
name: Memory System Research Cluster
description: Papers on agent memory architecture — retrieval, consolidation, external artifacts — informing STOPA memory design
type: reference
originSessionId: 16b10457-62ed-45b8-91c1-49616a4950d4
---
Cluster of papers informing STOPA memory system design.

| Paper | Key Finding | STOPA Impact |
|-------|------------|--------------|
| ByteRover (arXiv:2604.01599) | Hierarchical Context Tree, 5-tier retrieval, SOTA without embeddings | Upgrade proposals for retrieval |
| 724-office | 3-layer auto-compress vector memory (LanceDB, cosine dedup) | Pattern for persistent session memory |
| MemPalace v3.1.0 | 3-layer integration (session archive, semantic fallback, KG sync) | Integration architecture |
| Memory systems research | Retrieval>>storage, 3-signal ACT-R fusion, dreams consolidation | Created /dreams skill |
| Experience replay (Meta FAIR, arXiv:2604.08706) | Replay buffer 40% compute savings | Gap: outcomes/ underused in Phase 0 |
| Artifact memory (arXiv:2604.08756) | Env artifacts substitute for internal memory (Artifact Reduction Theorem) | Validates file-based memory design |

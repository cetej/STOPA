# LLM Papers — Implementation from Scratch

Implementace klíčových konceptů z "26 Essential Papers for Mastering LLMs and Transformers".

## Phase 1: Decoder-only Transformer (LLaMA-style)

Moderní GPT model s architekturou inspirovanou LLaMA:

| Komponenta | Paper | Soubor |
|-----------|-------|--------|
| Multi-Head Self-Attention | Attention Is All You Need (2017) | `attention.py` |
| RoPE Position Encoding | RoFormer (Su et al., 2021) | `attention.py` |
| RMSNorm | LLaMA (Touvron et al., 2023) | `layers.py` |
| SwiGLU FFN | LLaMA (Touvron et al., 2023) | `layers.py` |
| KV-Cache | Standard practice | `attention.py`, `generate.py` |

### Prerekvizity

```bash
# PyTorch s CUDA (pro GPU trénink):
pip install torch --index-url https://download.pytorch.org/whl/cu124
# Ostatní:
pip install tiktoken tqdm
```

### Trénink

```bash
# Tiny model na Shakespeare (~15M params, minuty na GPU):
python -m phase1_transformer.train --config tiny --data shakespeare

# Small model (~125M params, hodiny na 8GB GPU):
python -m phase1_transformer.train --config small --data shakespeare --batch-size 4
```

### Generování textu

```bash
python -m phase1_transformer.generate --checkpoint checkpoints/tiny_best.pt --interactive
```

### Testy

```bash
python -m tests.test_model
```

### Model configs

| Config | Layers | Heads | Dim | Params | GPU RAM |
|--------|--------|-------|-----|--------|---------|
| tiny | 6 | 6 | 384 | ~30M | <1 GB |
| small | 12 | 12 | 768 | ~125M | ~4 GB |
| medium | 24 | 16 | 1024 | ~350M | ~8 GB |

## Phase 2: RAG + ReAct Agent + Chain-of-Thought

Praktické aplikace stavějící na hotových LLM (Ollama/OpenAI API).

### 2A: RAG Pipeline (Paper #10)

| Komponenta | Soubor | Popis |
|-----------|--------|-------|
| Document Chunker | `chunker.py` | Fixed-size + semantic chunking |
| Embeddings | `embeddings.py` | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Store | `vector_store.py` | FAISS in-memory index |
| Retriever | `retriever.py` | Orchestrace: chunk → embed → search |
| RAG Pipeline | `rag_pipeline.py` | Retrieve → Augment prompt → Generate |
| LLM Client | `llm_client.py` | OpenAI-compatible API (Ollama/OpenAI/vLLM) |

```bash
pip install sentence-transformers faiss-cpu requests

# S Ollama (spusť v jiném terminálu: ollama run llama3.2:3b):
python -m phase2_rag.demo_rag

# Mock mode (bez LLM, testuje jen retrieval):
python -m phase2_rag.demo_rag --mock
```

### 2B: ReAct Agent (Paper #14)

| Komponenta | Soubor | Popis |
|-----------|--------|-------|
| Tool Registry | `tools.py` | Registrace nástrojů + calculator |
| ReAct Loop | `react_agent.py` | Thought → Action → Observation loop |

```bash
python -m phase2_react.demo_react         # S Ollama
python -m phase2_react.demo_react --mock   # Mock mode
```

### 2C: Chain-of-Thought Benchmark (Paper #13)

```bash
python -m phase2_cot.cot_benchmark         # S LLM
python -m phase2_cot.cot_benchmark --mock   # Mock mode
```

### Testy Phase 2

```bash
python -m tests.test_rag     # Chunking, embeddings, vector search
python -m tests.test_react   # Tool parsing, agent loop, calculator
```

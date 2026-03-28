"""Document chunking for RAG.

Why chunk documents?
- LLMs have limited context windows
- Embedding models work best on short passages (~256-512 tokens)
- Smaller chunks = more precise retrieval (less noise)
- Overlap prevents losing information at chunk boundaries

Two strategies:
1. Fixed-size: split every N characters with overlap (simple, predictable)
2. Semantic: split on paragraph/section boundaries (preserves meaning)

Paper context: Lewis et al. (2020) used Wikipedia passages as retrieval units.
Modern RAG systems use recursive character splitting with overlap.
"""

from dataclasses import dataclass


@dataclass
class Chunk:
    """A piece of a document with metadata."""
    text: str
    doc_id: str = ""         # Source document identifier
    chunk_id: int = 0        # Position within document
    metadata: dict = None    # Additional info (title, page, etc.)

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


def chunk_fixed_size(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
    doc_id: str = "",
) -> list[Chunk]:
    """Split text into fixed-size character chunks with overlap.

    Example with chunk_size=10, overlap=3:
        "Hello beautiful world today"
        → ["Hello beau", "eautiful w", "l world to", "today"]

    The overlap ensures that sentences split at boundaries are still
    captured in at least one chunk. Typical values:
    - chunk_size: 500-1000 chars (~100-250 tokens)
    - overlap: 50-200 chars (~10-50 tokens, ~10-20% of chunk size)

    Args:
        text: Full document text
        chunk_size: Maximum characters per chunk
        chunk_overlap: Characters of overlap between consecutive chunks
        doc_id: Identifier for the source document
    """
    if not text.strip():
        return []

    chunks = []
    start = 0
    chunk_idx = 0

    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append(Chunk(
                text=chunk_text,
                doc_id=doc_id,
                chunk_id=chunk_idx,
            ))
            chunk_idx += 1

        # Move forward by (chunk_size - overlap)
        start += chunk_size - chunk_overlap
        if start >= len(text):
            break

    return chunks


def chunk_semantic(
    text: str,
    max_chunk_size: int = 1000,
    doc_id: str = "",
) -> list[Chunk]:
    """Split text on semantic boundaries (paragraphs, sections).

    Strategy:
    1. Split on double newlines (paragraph boundaries)
    2. If a paragraph exceeds max_chunk_size, fall back to sentence splitting
    3. Merge small consecutive paragraphs into a single chunk

    This preserves meaning better than fixed-size chunking because
    it keeps complete thoughts together.
    """
    if not text.strip():
        return []

    # Split on paragraph boundaries
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks = []
    current_text = ""
    chunk_idx = 0

    for para in paragraphs:
        # If adding this paragraph would exceed limit, save current chunk
        if current_text and len(current_text) + len(para) + 2 > max_chunk_size:
            chunks.append(Chunk(
                text=current_text.strip(),
                doc_id=doc_id,
                chunk_id=chunk_idx,
            ))
            chunk_idx += 1
            current_text = ""

        # If single paragraph exceeds limit, split by sentences
        if len(para) > max_chunk_size:
            if current_text:
                chunks.append(Chunk(text=current_text.strip(), doc_id=doc_id, chunk_id=chunk_idx))
                chunk_idx += 1
                current_text = ""

            sentences = _split_sentences(para)
            sentence_buffer = ""
            for sent in sentences:
                if sentence_buffer and len(sentence_buffer) + len(sent) + 1 > max_chunk_size:
                    chunks.append(Chunk(text=sentence_buffer.strip(), doc_id=doc_id, chunk_id=chunk_idx))
                    chunk_idx += 1
                    sentence_buffer = ""
                sentence_buffer += " " + sent if sentence_buffer else sent

            if sentence_buffer:
                current_text = sentence_buffer
        else:
            current_text += ("\n\n" + para) if current_text else para

    # Don't forget the last chunk
    if current_text.strip():
        chunks.append(Chunk(text=current_text.strip(), doc_id=doc_id, chunk_id=chunk_idx))

    return chunks


def _split_sentences(text: str) -> list[str]:
    """Simple sentence splitter (split on . ! ? followed by space/newline)."""
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

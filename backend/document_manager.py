"""
Document Manager — Holds the current document state for both RAG approaches.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Manages:
  - Current document pages (dict of page_num → text)
  - Vector store (chunks + embeddings)
  - PageIndex tree (hierarchical JSON)
  - Metadata (document name, page count, etc.)

Supports the built-in PBRER demo document AND user-uploaded PDFs.
"""
import json
import time
import numpy as np
import anthropic
from pathlib import Path

from backend.config import (
    ANTHROPIC_API_KEY, LLM_MODEL, EMBEDDING_MODEL_NAME,
    CHUNK_SIZE, CHUNK_OVERLAP, TREE_INDEX_PATH, VECTORSTORE_PATH
)


class DocumentManager:
    def __init__(self):
        self.document_name: str = ""
        self.pages: dict[int, str] = {}
        self.total_pages: int = 0
        self.chunks: list[dict] = []
        self.embeddings: np.ndarray | None = None
        self.tree_index: dict | None = None
        self.tree_text: str = ""
        self.is_default: bool = False
        self._embedder = None

    def _get_embedder(self):
        if self._embedder is None:
            from sentence_transformers import SentenceTransformer
            self._embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
        return self._embedder

    # ── Load the built-in PBRER demo ──

    def load_default_document(self):
        """Load the pre-built Cardiozan PBRER with existing vector store and tree."""
        from data.pbrer_document import DOCUMENT_PAGES

        self.document_name = "PBRER — Cardiozan (Rivaximab Sodium) v6.0 [Demo]"
        self.pages = DOCUMENT_PAGES
        self.total_pages = len(DOCUMENT_PAGES)
        self.is_default = True

        # Load pre-built vector store
        if VECTORSTORE_PATH.exists():
            with open(VECTORSTORE_PATH) as f:
                store = json.load(f)
            self.chunks = store["chunks"]
            self.embeddings = np.array(store["embeddings"])
        else:
            # Build on the fly if not initialized
            self._build_vector_store()

        # Load pre-built tree
        if TREE_INDEX_PATH.exists():
            with open(TREE_INDEX_PATH) as f:
                self.tree_index = json.load(f)
            self.tree_text = self._format_tree(self.tree_index["document"])

        return {
            "document_name": self.document_name,
            "total_pages": self.total_pages,
            "num_chunks": len(self.chunks),
            "tree_nodes": len(self.tree_index["document"]["nodes"]) if self.tree_index else 0,
        }

    # ── Load a user-uploaded PDF ──

    def load_uploaded_pdf(self, file_bytes: bytes, filename: str) -> dict:
        """
        Process an uploaded PDF:
          1. Extract text per page (PyMuPDF)
          2. Chunk and embed (sentence-transformers)
          3. Generate tree index (Claude)
        """
        import fitz  # PyMuPDF

        self.is_default = False
        self.document_name = filename
        t0 = time.time()

        # ── Step 1: Extract text by page ──
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        self.pages = {}
        for i, page in enumerate(doc):
            text = page.get_text("text").strip()
            if text:  # Skip blank pages
                self.pages[i + 1] = text
        doc.close()
        self.total_pages = len(self.pages)

        if self.total_pages == 0:
            raise ValueError("Could not extract text from PDF. It may be scanned/image-based.")

        t_extract = time.time() - t0

        # ── Step 2: Chunk and embed ──
        t1 = time.time()
        self._build_vector_store()
        t_vector = time.time() - t1

        # ── Step 3: Generate tree index with Claude ──
        t2 = time.time()
        self._generate_tree_index()
        t_tree = time.time() - t2

        t_total = time.time() - t0

        return {
            "document_name": self.document_name,
            "total_pages": self.total_pages,
            "num_chunks": len(self.chunks),
            "tree_nodes": len(self.tree_index["document"]["nodes"]) if self.tree_index else 0,
            "timing": {
                "extract_ms": round(t_extract * 1000),
                "vector_build_ms": round(t_vector * 1000),
                "tree_build_ms": round(t_tree * 1000),
                "total_ms": round(t_total * 1000),
            },
        }

    # ── Build vector store from current pages ──

    def _build_vector_store(self):
        """Chunk current document and embed with sentence-transformers."""
        import re

        full_text = "\n\n".join(
            f"[PAGE {p}] {content}" for p, content in sorted(self.pages.items())
        )
        words = full_text.split()
        self.chunks = []
        start = 0
        chunk_id = 0

        while start < len(words):
            end = min(start + CHUNK_SIZE, len(words))
            chunk_text = " ".join(words[start:end])
            page_refs = sorted(set(
                int(m.group(1)) for m in re.finditer(r"\[PAGE (\d+)\]", chunk_text)
            ))
            self.chunks.append({
                "chunk_id": f"chunk_{chunk_id:03d}",
                "text": chunk_text,
                "word_count": end - start,
                "pages": page_refs or [-1],
            })
            start += CHUNK_SIZE - CHUNK_OVERLAP
            chunk_id += 1

        # Embed
        embedder = self._get_embedder()
        texts = [c["text"] for c in self.chunks]
        self.embeddings = embedder.encode(texts, show_progress_bar=False)

    # ── Generate tree index using Claude ──

    def _generate_tree_index(self):
        """Send document to Claude to generate a hierarchical tree index."""
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        # For very large documents, send first ~50 pages + TOC if available
        pages_to_send = dict(list(sorted(self.pages.items()))[:50])
        doc_text = "\n\n".join(
            f"[PAGE {p}]\n{content}" for p, content in sorted(pages_to_send.items())
        )

        # Truncate if too large (keep within context limits)
        if len(doc_text) > 80000:
            doc_text = doc_text[:80000] + "\n\n[... truncated for indexing ...]"

        prompt = f"""Analyze this document and create a hierarchical JSON tree index.

Each node must have: node_id (N001, N002...), title, start_page, end_page, summary.
Summaries should be DENSE — include key facts, numbers, names, cross-references.
Add sub_nodes for sections longer than 3 pages.

The tree must be valid JSON with this structure:
{{
  "document": {{
    "title": "...",
    "description": "One paragraph describing the entire document and its key topics",
    "total_pages": {self.total_pages},
    "nodes": [
      {{
        "node_id": "N001",
        "title": "...",
        "start_page": 1,
        "end_page": 2,
        "summary": "Dense summary with key facts...",
        "sub_nodes": []
      }}
    ]
  }}
}}

DOCUMENT ({self.total_pages} pages):

{doc_text}

Respond with ONLY valid JSON. No markdown fences. No extra text."""

        response = client.messages.create(
            model=LLM_MODEL,
            max_tokens=4000,
            system="You are an expert document analyst. Create comprehensive hierarchical indexes for documents. Always respond with valid JSON only.",
            messages=[{"role": "user", "content": prompt}],
        )

        raw = response.content[0].text.strip()

        # Parse JSON, handling possible markdown fences
        if raw.startswith("```"):
            lines = raw.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            raw = "\n".join(lines).strip()

        try:
            self.tree_index = json.loads(raw)
        except json.JSONDecodeError:
            start = raw.find("{")
            end = raw.rfind("}") + 1
            if start >= 0 and end > start:
                self.tree_index = json.loads(raw[start:end])
            else:
                raise ValueError("Failed to generate tree index — Claude returned invalid JSON")

        self.tree_text = self._format_tree(self.tree_index["document"])

    # ── Format tree for LLM context ──

    def _format_tree(self, doc: dict) -> str:
        lines = [
            f"DOCUMENT: {doc['title']}",
            f"Description: {doc.get('description', '')}",
            f"Total pages: {doc.get('total_pages', self.total_pages)}",
            "",
            "TREE INDEX (node_id | title | pages | summary):",
            "=" * 70,
        ]

        def fmt(node, indent=0):
            prefix = "  " * indent
            lines.append(
                f"{prefix}[{node['node_id']}] {node['title']} "
                f"(pages {node['start_page']}-{node['end_page']})"
            )
            lines.append(f"{prefix}  Summary: {node['summary']}")
            lines.append("")
            for child in node.get("sub_nodes", []):
                fmt(child, indent + 1)

        for node in doc.get("nodes", []):
            fmt(node)

        return "\n".join(lines)

    # ── Helper: get page content ──

    def get_pages(self, start: int, end: int) -> str:
        return "\n\n".join(
            f"[PAGE {p}]\n{self.pages[p]}"
            for p in range(start, end + 1)
            if p in self.pages
        )


# ── Global singleton ──
doc_manager = DocumentManager()

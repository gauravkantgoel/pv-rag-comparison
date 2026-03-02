"""
One-time initialization: Chunk the PBRER → Embed → Save to JSON.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run: python scripts/init_vectorstore.py

No ChromaDB, no C++ builds. Just sentence-transformers → numpy → JSON.
"""
import sys
import json
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from sentence_transformers import SentenceTransformer

from data.pbrer_document import DOCUMENT_PAGES
from backend.vector_rag import chunk_document, cosine_similarity_search
from backend.config import VECTORSTORE_PATH, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL_NAME


def main():
    print("=" * 60)
    print("  INITIALIZING VECTOR STORE")
    print("  Document: PBRER for Cardiozan (25 pages)")
    print("  Storage: Simple JSON file (no ChromaDB needed)")
    print("=" * 60)

    # ── Step 1: Chunk the document ──
    print(f"\n📄 Step 1: Chunking document (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    chunks = chunk_document(DOCUMENT_PAGES, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
    print(f"   Created {len(chunks)} chunks")
    for c in chunks[:3]:
        print(f"   - {c['chunk_id']}: {c['word_count']} words, pages {c['pages']}")
    if len(chunks) > 3:
        print(f"   ... and {len(chunks) - 3} more")

    # ── Step 2: Load embedding model ──
    print(f"\n🔢 Step 2: Loading embedding model '{EMBEDDING_MODEL_NAME}'...")
    print("   (First run downloads ~80MB model — cached afterwards)")
    t0 = time.time()
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    print(f"   Model loaded in {time.time()-t0:.1f}s")

    # ── Step 3: Embed all chunks ──
    print(f"\n📦 Step 3: Embedding {len(chunks)} chunks...")
    texts = [c["text"] for c in chunks]
    t0 = time.time()
    embeddings = model.encode(texts, show_progress_bar=True)
    print(f"   Embedded in {time.time()-t0:.1f}s")
    print(f"   Embedding shape: {embeddings.shape}  (chunks x dimensions)")

    # ── Step 4: Save to JSON ──
    print(f"\n💾 Step 4: Saving vector store to {VECTORSTORE_PATH}...")
    store = {
        "model": EMBEDDING_MODEL_NAME,
        "embedding_dim": int(embeddings.shape[1]),
        "num_chunks": len(chunks),
        "chunks": chunks,                              # chunk metadata + text
        "embeddings": embeddings.tolist(),              # float lists (JSON serializable)
    }

    VECTORSTORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(VECTORSTORE_PATH, "w") as f:
        json.dump(store, f)

    file_size_mb = VECTORSTORE_PATH.stat().st_size / (1024 * 1024)
    print(f"   ✅ Saved! File size: {file_size_mb:.1f} MB")

    # ── Step 5: Verify with a test query ──
    print("\n🔍 Step 5: Verification — test query...")
    test_query = "hepatotoxicity signal evaluation"
    query_emb = model.encode(test_query)
    stored_embs = np.array(store["embeddings"])

    results = cosine_similarity_search(query_emb, stored_embs, top_k=3)

    print(f"   Query: '{test_query}'")
    for rank, (idx, sim) in enumerate(results):
        chunk = chunks[idx]
        print(f"   #{rank+1} {chunk['chunk_id']} (pages {chunk['pages']}, similarity={sim:.4f})")

    print("\n" + "=" * 60)
    print("  ✅ VECTOR STORE READY")
    print(f"  File: {VECTORSTORE_PATH}")
    print(f"  Chunks: {len(chunks)}")
    print(f"  Embedding model: {EMBEDDING_MODEL_NAME} ({embeddings.shape[1]}-dim)")
    print(f"  Size: {file_size_mb:.1f} MB")
    print("=" * 60)
    print("\nNext step — start the server:")
    print("  uvicorn backend.app:app --reload --port 8000")


if __name__ == "__main__":
    main()

"""
APPROACH 1: VECTOR-BASED RAG
Pipeline: Query → Embed → Cosine Search (numpy) → Generate (Claude)
Now reads from DocumentManager instead of a static file.
"""
import time
import numpy as np
import anthropic
from backend.config import ANTHROPIC_API_KEY, LLM_MODEL, TOP_K, EMBEDDING_MODEL_NAME
from backend.document_manager import doc_manager

_embedder = None
_client = None


def _get_embedder():
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _embedder


def _get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def cosine_similarity_search(query_embedding: np.ndarray,
                              stored_embeddings: np.ndarray,
                              top_k: int = 3) -> list[tuple[int, float]]:
    query_norm = query_embedding / (np.linalg.norm(query_embedding) + 1e-10)
    stored_norms = stored_embeddings / (np.linalg.norm(stored_embeddings, axis=1, keepdims=True) + 1e-10)
    similarities = stored_norms @ query_norm
    top_indices = np.argsort(similarities)[::-1][:top_k]
    return [(int(idx), float(similarities[idx])) for idx in top_indices]


def query(user_query: str) -> dict:
    t0 = time.time()
    embedder = _get_embedder()
    client = _get_client()

    if doc_manager.embeddings is None or len(doc_manager.chunks) == 0:
        return {"approach": "vector_rag", "answer": "No document loaded. Please upload a document first.", "error": True}

    chunks_data = doc_manager.chunks
    stored_embeddings = doc_manager.embeddings

    # Step 1: Embed query
    t_embed_start = time.time()
    query_embedding = embedder.encode(user_query)
    t_embed = time.time() - t_embed_start

    # Step 2: Similarity search
    t_search_start = time.time()
    results = cosine_similarity_search(query_embedding, stored_embeddings, top_k=TOP_K)
    t_search = time.time() - t_search_start

    # Parse results
    retrieved_chunks = []
    all_pages = set()
    context_parts = []

    for chunk_idx, similarity in results:
        chunk = chunks_data[chunk_idx]
        pages = chunk["pages"]
        all_pages.update(p for p in pages if p > 0)

        retrieved_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "similarity": round(similarity, 4),
            "pages": pages,
            "preview": chunk["text"][:250] + "..." if len(chunk["text"]) > 250 else chunk["text"],
            "full_text": chunk["text"],
        })
        context_parts.append(
            f"--- Chunk {chunk['chunk_id']} (pages {pages}, similarity={similarity:.3f}) ---\n{chunk['text']}"
        )

    # Step 3: Generate answer
    context = "\n\n".join(context_parts)
    prompt = f"""RETRIEVED CONTEXT:
{context}

QUESTION: {user_query}

Answer based ONLY on the provided context. If the context doesn't contain enough information, say what's missing. Cite page numbers, statistics, and details when available."""

    t_generate_start = time.time()
    response = client.messages.create(
        model=LLM_MODEL,
        max_tokens=800,
        system="You are an expert document analyst answering questions based on retrieved document sections.",
        messages=[{"role": "user", "content": prompt}],
    )
    t_generate = time.time() - t_generate_start
    answer = response.content[0].text

    t_total = time.time() - t0

    return {
        "approach": "vector_rag",
        "answer": answer,
        "retrieved_chunks": retrieved_chunks,
        "pages_accessed": sorted(all_pages),
        "num_chunks": len(retrieved_chunks),
        "timing": {
            "embed_ms": round(t_embed * 1000),
            "search_ms": round(t_search * 1000),
            "retrieval_ms": round((t_embed + t_search) * 1000),
            "generation_ms": round(t_generate * 1000),
            "total_ms": round(t_total * 1000),
        },
        "steps": [
            {
                "step": 1,
                "action": "EMBED_QUERY",
                "detail": f"Embedded query into 384-dim vector using {EMBEDDING_MODEL_NAME} (local, {round(t_embed*1000)}ms)",
            },
            {
                "step": 2,
                "action": "SIMILARITY_SEARCH",
                "detail": f"Cosine similarity over {len(chunks_data)} chunks - top-{TOP_K} retrieved ({round(t_search*1000)}ms)",
                "chunks": [
                    {"id": c["chunk_id"], "sim": c["similarity"], "pages": c["pages"]}
                    for c in retrieved_chunks
                ],
            },
            {
                "step": 3,
                "action": "GENERATE_ANSWER",
                "detail": f"Sent {len(context_parts)} chunks + query to {LLM_MODEL} ({round(t_generate*1000)}ms)",
            },
        ],
    }

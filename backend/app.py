"""
FastAPI Backend — Runs both RAG approaches, supports document upload.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Start with:  uvicorn backend.app:app --reload --port 8000
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend import vector_rag, pageindex_rag
from backend.document_manager import doc_manager

app = FastAPI(
    title="PV RAG Comparison",
    description="Vector RAG vs PageIndex — upload any document",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = ThreadPoolExecutor(max_workers=2)


# ── Request / Response models ──

class QueryRequest(BaseModel):
    query: str


# ── Test queries (only for the demo PBRER) ──

TEST_QUERIES = [
    {
        "id": 1,
        "query": "What is the reporting rate for serious adverse events?",
        "challenge": "Direct lookup",
        "difficulty": "Easy",
        "ideal_pages": [9],
    },
    {
        "id": 2,
        "query": "What were the RUCAM scores for the fatal hepatic failure cases?",
        "challenge": "Cross-reference following",
        "difficulty": "Hard",
        "ideal_pages": [13, 23],
    },
    {
        "id": 3,
        "query": "What risk minimization measures were taken for hepatotoxicity?",
        "challenge": "Multi-section synthesis",
        "difficulty": "Hard",
        "ideal_pages": [5, 6, 13, 16],
    },
    {
        "id": 4,
        "query": "Has the drug been shown to affect heart rhythm?",
        "challenge": "Vocabulary mismatch",
        "difficulty": "Hard",
        "ideal_pages": [15],
    },
    {
        "id": 5,
        "query": "What is the incidence of DILI and what are the key risk factors?",
        "challenge": "Multi-hop reasoning",
        "difficulty": "Hard",
        "ideal_pages": [12, 13, 16],
    },
]


# ── Startup: Load default document ──

@app.on_event("startup")
async def startup():
    try:
        result = doc_manager.load_default_document()
        print(f"✅ Default document loaded: {result['document_name']}")
        print(f"   Pages: {result['total_pages']}, Chunks: {result['num_chunks']}, Tree nodes: {result['tree_nodes']}")
    except Exception as e:
        print(f"⚠️ Could not load default document: {e}")
        print("   Upload a document via the UI to get started.")


# ── Endpoints ──

@app.get("/")
async def root():
    return {"status": "ok", "document": doc_manager.document_name or "No document loaded"}


@app.get("/api/document-status")
async def document_status():
    """Return current document info."""
    return {
        "document_name": doc_manager.document_name,
        "total_pages": doc_manager.total_pages,
        "num_chunks": len(doc_manager.chunks),
        "has_tree": doc_manager.tree_index is not None,
        "is_default": doc_manager.is_default,
    }


@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF document. This will:
      1. Extract text from each page
      2. Chunk and embed for Vector RAG
      3. Generate a tree index for PageIndex (Claude API call)
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_bytes = await file.read()

    if len(file_bytes) > 50 * 1024 * 1024:  # 50MB limit
        raise HTTPException(status_code=400, detail="File too large (max 50MB)")

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            doc_manager.load_uploaded_pdf,
            file_bytes,
            file.filename,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.post("/api/load-demo")
async def load_demo():
    """Reload the built-in PBRER demo document."""
    result = doc_manager.load_default_document()
    return result


@app.get("/api/test-queries")
async def get_test_queries():
    """Return test queries (only meaningful for the demo PBRER)."""
    return {
        "queries": TEST_QUERIES,
        "is_default_document": doc_manager.is_default,
    }


@app.post("/api/query")
async def compare_query(req: QueryRequest):
    """Run BOTH RAG approaches on the same query."""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    if not doc_manager.pages:
        raise HTTPException(status_code=400, detail="No document loaded. Upload a PDF first.")

    loop = asyncio.get_event_loop()

    vector_future = loop.run_in_executor(executor, vector_rag.query, req.query)
    pageindex_future = loop.run_in_executor(executor, pageindex_rag.query, req.query)

    vector_result, pageindex_result = await asyncio.gather(
        vector_future, pageindex_future
    )

    return {
        "query": req.query,
        "vector_rag": vector_result,
        "pageindex": pageindex_result,
    }

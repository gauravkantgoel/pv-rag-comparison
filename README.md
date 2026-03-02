# PV RAG Comparison: Vector RAG vs PageIndex

Side-by-side comparison of **Vector-based RAG** vs **PageIndex (Reasoning-based RAG)**
on a Pharmacovigilance PBRER document.

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                  BROWSER (UI)                        │
│  ┌─────────────────┐    ┌──────────────────────┐     │
│  │  Vector RAG      │    │  PageIndex RAG        │    │
│  │  - Chunks found  │    │  - Reasoning steps    │    │
│  │  - Similarity    │    │  - Tree navigation    │    │
│  │  - LLM answer    │    │  - LLM answer         │    │
│  └────────┬────────┘    └──────────┬───────────┘     │
│           └──────────┬─────────────┘                  │
│                      │ HTTP (fetch)                   │
└──────────────────────┼───────────────────────────────┘
                       │
┌──────────────────────┼───────────────────────────────┐
│              FastAPI Backend (:8000)                   │
│                      │                                │
│  ┌───────────────────┴────────────────────┐           │
│  │          /api/query                     │           │
│  │   Runs BOTH pipelines in parallel       │           │
│  └───────┬───────────────────┬────────────┘           │
│          │                   │                        │
│  ┌───────▼───────┐  ┌───────▼───────────┐            │
│  │ Vector RAG     │  │ PageIndex RAG      │           │
│  │                │  │                    │           │
│  │ 1. Embed query │  │ 1. Read tree index │           │
│  │ 2. NumPy      │  │ 2. LLM reasons     │           │
│  │    cosine sim │  │ 3. Fetch node      │           │
│  │ 3. Top-k chunk│  │ 4. Extract info    │           │
│  │ 4. LLM answer  │  │ 5. Loop or answer  │           │
│  └───────┬───────┘  └───────┬───────────┘            │
│          │                   │                        │
│  ┌───────▼───────┐  ┌───────▼───────────┐            │
│  │ JSON + NumPy   │  │ OpenAI GPT-4o     │            │
│  │ (local vector  │  │ (reasoning calls)  │           │
│  │  store file)   │  │                    │           │
│  └───────────────┘  └───────────────────┘            │
│                                                       │
│  ┌────────────────────────────────────────┐           │
│  │ PBRER Document (25 pages)               │          │
│  │ data/pbrer_document.py                  │          │
│  └────────────────────────────────────────┘           │
└───────────────────────────────────────────────────────┘
```

## Prerequisites

- Python 3.10+
- Node.js 18+ (only for optional PDF generation)
- Anthropic API key (for LLM calls)

## Setup (Step by Step)

### Step 1: Clone and enter project
```bash
cd pv-rag-comparison
```

### Step 2: Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set your OpenAI API key
```bash
# Create .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### Step 5: Initialize the vector store (one-time)
```bash
python scripts/init_vectorstore.py
```
This chunks the PBRER, embeds it with sentence-transformers, and saves to a JSON file.

### Step 6: Start the backend
```bash
uvicorn backend.app:app --reload --port 8000
```

### Step 7: Open the UI
Open `frontend/index.html` in your browser.
Or serve it:
```bash
python -m http.server 3000 --directory frontend
```
Then visit http://localhost:3000

## Test Queries

The UI comes with 5 pre-loaded test queries designed to expose
different failure modes:

| # | Query | Challenge |
|---|-------|-----------|
| 1 | What is the reporting rate for SAEs? | Direct lookup |
| 2 | What were the RUCAM scores for fatal hepatic cases? | Cross-reference |
| 3 | What risk minimization measures for hepatotoxicity? | Multi-section |
| 4 | Has the drug been shown to affect heart rhythm? | Vocabulary mismatch |
| 5 | Incidence of DILI and key risk factors? | Multi-hop reasoning |

## Project Structure

```
pv-rag-comparison/
├── README.md
├── requirements.txt
├── .env                          # Your OpenAI key
├── backend/
│   ├── __init__.py
│   ├── app.py                    # FastAPI server
│   ├── vector_rag.py             # Approach 1: Vector RAG
│   ├── pageindex_rag.py          # Approach 2: PageIndex
│   └── config.py                 # Settings
├── data/
│   ├── pbrer_document.py         # The 25-page PBRER
│   ├── pageindex_tree.json       # Pre-built tree index
│   └── vectorstore.json          # Auto-created by init script
├── scripts/
│   ├── init_vectorstore.py       # One-time: chunk + embed + store
│   └── build_tree_index.py       # One-time: generate PageIndex tree
├── frontend/
│   └── index.html                # Comparison UI
```

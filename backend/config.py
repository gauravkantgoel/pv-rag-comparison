"""
Configuration for the PV RAG Comparison app.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Paths ──
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
VECTORSTORE_PATH = DATA_DIR / "vectorstore.json"

# ── Anthropic ──
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LLM_MODEL = "claude-sonnet-4-20250514"

# ── Vector RAG Settings ──
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
TOP_K = 3
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# ── PageIndex Settings ──
MAX_ITERATIONS = 5
TREE_INDEX_PATH = DATA_DIR / "pageindex_tree.json"
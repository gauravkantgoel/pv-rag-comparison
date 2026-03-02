"""
Optional: Generate the PageIndex tree index from the PBRER document using GPT-4o.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
We already provide a pre-built tree (data/pageindex_tree.json).
Run this only if you want to regenerate it or adapt it for a different document.

Run: python scripts/build_tree_index.py
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from openai import OpenAI
from dotenv import load_dotenv
from data.pbrer_document import get_full_text
from backend.config import OPENAI_API_KEY, LLM_MODEL, TREE_INDEX_PATH

load_dotenv()

TREE_GENERATION_PROMPT = """You are an expert document analyst. I will give you the full text of a PBRER (Periodic Benefit-Risk Evaluation Report) for a pharmaceutical drug.

Your task: Create a hierarchical JSON tree index of this document. This tree will be used by an LLM at query time to navigate the document efficiently.

Requirements:
1. Each node must have: node_id, title, start_page, end_page, summary
2. Use the document's natural section structure (sections, subsections, appendices)
3. Summaries should be DENSE — pack in key facts, numbers, study names, cross-references
4. Sub-nodes are optional but useful for long sections (>3 pages)
5. The tree should fit in ~5000 characters when formatted as text

Output format:
{
  "document": {
    "title": "...",
    "description": "...",
    "total_pages": 25,
    "nodes": [
      {
        "node_id": "N001",
        "title": "...",
        "start_page": 1,
        "end_page": 2,
        "summary": "...",
        "sub_nodes": [...]  // optional
      }
    ]
  }
}

Be thorough with summaries — include specific numbers, study names, dates, and cross-references.
These summaries are what the LLM reads to decide WHERE to navigate."""


def main():
    print("🌲 Building PageIndex tree from PBRER document...")
    print(f"   Using model: {LLM_MODEL}")

    client = OpenAI(api_key=OPENAI_API_KEY)
    document_text = get_full_text()

    print(f"   Document length: {len(document_text)} characters")
    print("   Sending to LLM for tree generation...")

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": TREE_GENERATION_PROMPT},
            {"role": "user", "content": f"Here is the PBRER document:\n\n{document_text}"},
        ],
        temperature=0.1,
        max_tokens=4000,
        response_format={"type": "json_object"},
    )

    tree_json = json.loads(response.choices[0].message.content)

    # Validate structure
    assert "document" in tree_json
    assert "nodes" in tree_json["document"]
    node_count = len(tree_json["document"]["nodes"])
    print(f"   Generated tree with {node_count} top-level nodes")

    # Save
    with open(TREE_INDEX_PATH, "w") as f:
        json.dump(tree_json, f, indent=2)

    print(f"   ✅ Saved to {TREE_INDEX_PATH}")


if __name__ == "__main__":
    main()

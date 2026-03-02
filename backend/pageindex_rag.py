"""
APPROACH 2: PAGEINDEX — VECTORLESS, REASONING-BASED RAG
Pipeline: Tree Index (in-context) → Claude Reasons → Fetch Node → Extract → Loop or Answer
Now reads from DocumentManager instead of static files.
"""
import json
import time
import anthropic
from backend.config import ANTHROPIC_API_KEY, LLM_MODEL, MAX_ITERATIONS
from backend.document_manager import doc_manager

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def _find_node(node_id: str, nodes: list) -> dict | None:
    for node in nodes:
        if node["node_id"] == node_id:
            return node
        found = _find_node(node_id, node.get("sub_nodes", []))
        if found:
            return found
    return None


REASONING_SYSTEM_PROMPT = """You are an expert document analyst navigating a document using a tree index.

Your task: Answer the user's question by navigating to the right sections of the document.

You have access to a TREE INDEX that shows the document's hierarchical structure with summaries.
At each step, you will either:
  1. REQUEST a node's full content (to read the actual text)
  2. Provide your FINAL ANSWER (when you have enough information)

RULES:
- Read the tree index carefully. Use summaries to decide WHERE to look.
- Think step by step. Explain your reasoning before each action.
- Follow cross-references (e.g., "see Section 7.1" or "refer to Appendix A").
- You can request multiple nodes across iterations to build a complete answer.
- When you have sufficient information, provide a comprehensive answer.

RESPONSE FORMAT (strict JSON, no markdown fences, no extra text):
For requesting a node:
{"action": "FETCH_NODE", "node_id": "N008a", "reasoning": "The question asks about X. Node N008a covers Y which is relevant because Z."}

For providing the final answer:
{"action": "ANSWER", "answer": "Based on the document...", "reasoning": "I gathered information from nodes X, Y, Z which together provide...", "sources": ["N008a (page 13)", "N013 (page 23)"]}

CRITICAL: Respond with ONLY valid JSON. No markdown code fences. No extra text before or after the JSON."""


def _parse_json_response(raw: str) -> dict:
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end])
            except json.JSONDecodeError:
                pass
        return {"action": "ANSWER", "answer": raw, "reasoning": "JSON parse fallback", "sources": []}


def query(user_query: str) -> dict:
    t0 = time.time()
    client = _get_client()

    if doc_manager.tree_index is None:
        return {"approach": "pageindex", "answer": "No document loaded. Please upload a document first.", "error": True}

    tree_data = doc_manager.tree_index
    tree_text = doc_manager.tree_text

    messages = [
        {
            "role": "user",
            "content": f"""Here is the document tree index:

{tree_text}

QUESTION: {user_query}

Navigate the tree to find the answer. Start by reasoning about which node(s) to check first.
Respond with ONLY valid JSON.""",
        },
    ]

    steps = []
    pages_accessed = set()
    nodes_visited = []
    iteration = 0

    while iteration < MAX_ITERATIONS:
        iteration += 1
        t_step_start = time.time()

        response = client.messages.create(
            model=LLM_MODEL,
            max_tokens=1000,
            system=REASONING_SYSTEM_PROMPT,
            messages=messages,
        )
        raw = response.content[0].text
        t_step = time.time() - t_step_start

        decision = _parse_json_response(raw)
        action = decision.get("action", "ANSWER")
        reasoning = decision.get("reasoning", "")

        if action == "FETCH_NODE":
            node_id = decision.get("node_id", "")
            node = _find_node(node_id, tree_data["document"]["nodes"])

            if node:
                content = doc_manager.get_pages(node["start_page"], node["end_page"])
                for p in range(node["start_page"], node["end_page"] + 1):
                    pages_accessed.add(p)
                nodes_visited.append(node_id)

                steps.append({
                    "step": iteration,
                    "action": "FETCH_NODE",
                    "node_id": node_id,
                    "node_title": node["title"],
                    "pages": f"{node['start_page']}-{node['end_page']}",
                    "reasoning": reasoning,
                    "duration_ms": round(t_step * 1000),
                })

                messages.append({"role": "assistant", "content": raw})
                messages.append({
                    "role": "user",
                    "content": f"""Here is the content of node {node_id} ({node['title']}, pages {node['start_page']}-{node['end_page']}):

{content}

Based on this content and any previously fetched content, either:
- Request another node if you need more information
- Provide your final answer if you have enough

Remember the original question: {user_query}
Respond with ONLY valid JSON.""",
                })
            else:
                steps.append({
                    "step": iteration,
                    "action": "ERROR",
                    "detail": f"Node {node_id} not found in tree",
                    "reasoning": reasoning,
                    "duration_ms": round(t_step * 1000),
                })
                messages.append({"role": "assistant", "content": raw})
                messages.append({
                    "role": "user",
                    "content": f"Node {node_id} was not found. Check the tree index and try a different node. Respond with ONLY valid JSON.",
                })

        elif action == "ANSWER":
            answer = decision.get("answer", "")
            sources = decision.get("sources", [])

            steps.append({
                "step": iteration,
                "action": "ANSWER",
                "reasoning": reasoning,
                "sources": sources,
                "duration_ms": round(t_step * 1000),
            })

            t_total = time.time() - t0
            return {
                "approach": "pageindex",
                "answer": answer,
                "pages_accessed": sorted(pages_accessed),
                "nodes_visited": nodes_visited,
                "num_iterations": iteration,
                "timing": {
                    "total_ms": round(t_total * 1000),
                    "per_step_ms": [s.get("duration_ms", 0) for s in steps],
                },
                "steps": steps,
                "tree_summary": f"{len(tree_text)} chars, fits in context window",
            }

    # Max iterations reached
    messages.append({
        "role": "user",
        "content": f"Maximum iterations reached. Provide your best answer to: {user_query}\nRespond with ONLY valid JSON with action ANSWER.",
    })
    response = client.messages.create(
        model=LLM_MODEL,
        max_tokens=800,
        system=REASONING_SYSTEM_PROMPT,
        messages=messages,
    )
    raw = response.content[0].text
    decision = _parse_json_response(raw)
    forced_answer = decision.get("answer", raw)

    steps.append({
        "step": iteration + 1,
        "action": "FORCED_ANSWER",
        "reasoning": "Max iterations reached",
        "duration_ms": 0,
    })

    t_total = time.time() - t0
    return {
        "approach": "pageindex",
        "answer": forced_answer,
        "pages_accessed": sorted(pages_accessed),
        "nodes_visited": nodes_visited,
        "num_iterations": iteration + 1,
        "timing": {
            "total_ms": round(t_total * 1000),
            "per_step_ms": [s.get("duration_ms", 0) for s in steps],
        },
        "steps": steps,
        "tree_summary": f"{len(tree_text)} chars, fits in context window",
    }

"""3-stage LLM Council orchestration."""

from typing import List, Dict, Any, Tuple
from .ollama import query_members_parallel, query_model
from .config import COUNCIL_LANGUAGE, COUNCIL_MEMBERS, CHAIRMAN_MODEL


async def stage1_collect_responses(user_query: str):
    messages = [{"role": "user", "content": user_query}]
    responses = await query_members_parallel(COUNCIL_MEMBERS, messages)
    return [
        {"model": name, "response": r["content"]}
        for name, r in responses.items() if r is not None
    ]


async def stage2_collect_comparisons(user_query, stage1_results):
    """Ask each worldview to compare the question through its own lens."""
    views = "\n\n".join(f"{r['model']}: {r['response']}" for r in stage1_results)
    prompt = f"""Question: {user_query}

The other schools answered:

{views}

Stay inside your named school and do not blend it with the other schools. Do not rank, score,
or choose a winner. Answer in {COUNCIL_LANGUAGE} using this organized structure in 3-5 sentences:
What the school sees: ...
Point of conflict: ...
What the school cannot easily explain: ...
Represent the conflict fairly, but do not answer from outside your framework."""

    responses = await query_members_parallel(
        COUNCIL_MEMBERS, [{"role": "user", "content": prompt}]
    )
    stage2_results = [
        {"model": name, "comparison": r["content"]}
        for name, r in responses.items() if r is not None
    ]
    return stage2_results


async def stage3_synthesize_final(user_query, stage1_results, stage2_results):
    s1 = "\n\n".join(f"{r['model']}: {r['response']}" for r in stage1_results)
    s2 = "\n\n".join(f"{r['model']} (comparison): {r['comparison']}" for r in stage2_results)

    prompt = f"""You are the facilitator of a council of philosophical schools. Answer in {COUNCIL_LANGUAGE}.
Do not choose a winner, rank the schools, or pretend the frameworks collapse into one answer.
Map how each school understands the question and make their genuine conflicts useful to the reader.

Question: {user_query}

OPENING VIEWS:
{s1}

COMPARISONS:
{s2}

Write the report in {COUNCIL_LANGUAGE} using exactly these headings:

AGREEMENT: (what the schools share, in 1-2 sentences)
DISAGREEMENT: (the core conflict between the schools, in 2-4 sentences)
MINORITY VIEW: (the strongest dissenting position and why it matters)
BOTTOM LINE: (2-3 sentences explaining why the question remains open; do not choose a winner)"""

    response = await query_model(CHAIRMAN_MODEL, [{"role": "user", "content": prompt}])
    if response is None:
        return {"model": CHAIRMAN_MODEL, "response": "Unable to generate the council synthesis."}
    return {"model": CHAIRMAN_MODEL, "response": response["content"]}


async def generate_conversation_title(user_query: str) -> str:
    """
    Generate a short title for a conversation based on the first user message.

    Args:
        user_query: The first user message

    Returns:
        A short title (3-5 words)
    """
    title_prompt = f"""Generate a very short title (3-5 words) in {COUNCIL_LANGUAGE} for the question below.
Keep it concise and descriptive. Do not use quotes or punctuation.

Question: {user_query}

Title:"""

    messages = [{"role": "user", "content": title_prompt}]

    response = await query_model(CHAIRMAN_MODEL, messages, timeout=30.0)
    
    if response is None:
        # Fallback to a generic title
        return "New Conversation"

    title = response.get('content', 'New Conversation').strip()

    # Clean up the title - remove quotes, limit length
    title = title.strip('"\'')

    # Truncate if too long
    if len(title) > 50:
        title = title[:47] + "..."

    return title


async def run_full_council(user_query: str) -> Tuple[List, List, Dict, Dict]:
    """
    Run the complete 3-stage council process.

    Args:
        user_query: The user's question

    Returns:
        Tuple of (stage1_results, stage2_results, stage3_result, metadata)
    """
    # Stage 1: Collect individual responses
    stage1_results = await stage1_collect_responses(user_query)

    # If no models responded successfully, return error
    if not stage1_results:
        return [], [], {
            "model": "error",
            "response": "All models failed to respond. Please try again."
        }, {}

    # Stage 2: Compare the worldviews
    stage2_results = await stage2_collect_comparisons(user_query, stage1_results)

    # Stage 3: Synthesize final answer
    stage3_result = await stage3_synthesize_final(
        user_query,
        stage1_results,
        stage2_results
    )

    # Prepare metadata
    metadata = {
        "frameworks": [member["name"] for member in COUNCIL_MEMBERS],
    }

    return stage1_results, stage2_results, stage3_result, metadata

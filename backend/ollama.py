import re
import asyncio
import httpx
from typing import List, Dict, Any, Optional
from .config import (
    API_BASE_URL,
    API_KEY,
    COUNCIL_SEQUENTIAL,
    MAX_TOKENS,
    MODEL_PROVIDER,
    OLLAMA_BASE_URL,
    OLLAMA_TEMPERATURE,
    OLLAMA_TOP_K,
    OLLAMA_TOP_P,
)


async def query_model(model, messages, timeout: float = 300.0,
                      system: Optional[str] = None) -> Optional[Dict[str, Any]]:
    if system:
        messages = [{"role": "system", "content": system}] + messages

    if MODEL_PROVIDER == "api":
        url = f"{API_BASE_URL.rstrip('/')}/chat/completions"
        headers = {"Content-Type": "application/json"}
        if API_KEY:
            headers["Authorization"] = f"Bearer {API_KEY}"
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "temperature": OLLAMA_TEMPERATURE,
            "top_p": OLLAMA_TOP_P,
            "max_tokens": MAX_TOKENS,
        }
    else:
        url = f"{OLLAMA_BASE_URL.rstrip('/')}/api/chat"
        headers = {}
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": OLLAMA_TEMPERATURE,
                "top_k": OLLAMA_TOP_K,
                "top_p": OLLAMA_TOP_P,
                "num_predict": MAX_TOKENS,
            },
        }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            if MODEL_PROVIDER == "api":
                message = data.get("choices", [{}])[0].get("message", {})
                content = message.get("content", "")
                stop_reason = data.get("choices", [{}])[0].get("finish_reason")
            else:
                content = data.get("message", {}).get("content", "")
                stop_reason = data.get("done_reason")
            # strip deepseek-r1 style reasoning blocks
            content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
            return {"content": content, "model": model,
                    "stop_reason": stop_reason}
    except Exception as e:
        print(f"Error querying model {model}: {e}")
        return None


async def query_members_parallel(members: List[Dict[str, str]],
                                 messages: List[Dict[str, str]]) -> Dict[str, Optional[Dict[str, Any]]]:
    """Query council members; results are keyed by persona NAME, not model."""
    if COUNCIL_SEQUENTIAL:
        results = []
        for m in members:
            results.append(await query_model(m["model"], messages, system=m["system"]))
    else:
        results = await asyncio.gather(
            *[query_model(m["model"], messages, system=m["system"]) for m in members]
        )
    return {m["name"]: r for m, r in zip(members, results)}
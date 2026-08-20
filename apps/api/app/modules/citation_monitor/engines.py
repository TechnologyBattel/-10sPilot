"""Answer engine probes.

Each probe asks an engine the prompt and returns the raw answer text plus any cited URLs.
Perplexity and OpenAI need paid keys, so the free default is Gemini with Google Search grounding;
engines without credentials are reported as errored rather than silently skipped.
"""

from dataclasses import dataclass, field
from typing import Any

import httpx

from app.core.config import settings
from app.core.errors import MissingCredentialError, UpstreamError

PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


@dataclass
class EngineAnswer:
    engine: str
    text: str = ""
    citations: list[str] = field(default_factory=list)
    error: str | None = None


async def _post(url: str, **kwargs: Any) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
        response = await client.post(url, **kwargs)
    if response.status_code >= 400:
        raise UpstreamError(url, response.status_code)
    data: dict[str, Any] = response.json()
    return data


async def ask_gemini(prompt: str) -> EngineAnswer:
    if not settings.google_api_key:
        raise MissingCredentialError("GOOGLE_API_KEY")

    data = await _post(
        GEMINI_URL.format(model=settings.google_model),
        params={"key": settings.google_api_key},
        json={
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "tools": [{"google_search": {}}],
        },
    )
    candidates: list[dict[str, Any]] = data.get("candidates", [])
    if not candidates:
        return EngineAnswer(engine="gemini")

    parts: list[dict[str, Any]] = candidates[0].get("content", {}).get("parts", [])
    grounding: dict[str, Any] = candidates[0].get("groundingMetadata", {})
    chunks: list[dict[str, Any]] = grounding.get("groundingChunks", [])
    citations = [str(chunk.get("web", {}).get("uri", "")) for chunk in chunks]
    return EngineAnswer(
        engine="gemini",
        text="".join(str(part.get("text", "")) for part in parts),
        citations=[url for url in citations if url],
    )


async def ask_perplexity(prompt: str) -> EngineAnswer:
    if not settings.perplexity_api_key:
        raise MissingCredentialError("PERPLEXITY_API_KEY")

    data = await _post(
        PERPLEXITY_URL,
        headers={"Authorization": f"Bearer {settings.perplexity_api_key}"},
        json={
            "model": settings.perplexity_model,
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    choices: list[dict[str, Any]] = data.get("choices", [])
    text = str(choices[0].get("message", {}).get("content", "")) if choices else ""
    citations = [str(url) for url in data.get("citations", [])]
    return EngineAnswer(engine="perplexity", text=text, citations=citations)


async def ask_chatgpt(prompt: str) -> EngineAnswer:
    if not settings.openai_api_key:
        raise MissingCredentialError("OPENAI_API_KEY")

    data = await _post(
        OPENAI_URL,
        headers={"Authorization": f"Bearer {settings.openai_api_key}"},
        json={
            "model": settings.openai_model,
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    choices: list[dict[str, Any]] = data.get("choices", [])
    text = str(choices[0].get("message", {}).get("content", "")) if choices else ""
    return EngineAnswer(engine="chatgpt", text=text)


ENGINES = {"chatgpt": ask_chatgpt, "perplexity": ask_perplexity, "gemini": ask_gemini}

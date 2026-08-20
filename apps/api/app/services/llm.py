"""Free-tier LLM client shared by the content, AEO, GEO and citation engines."""

from typing import Any

import httpx

from app.core.config import settings
from app.core.errors import MissingCredentialError, UpstreamError

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


class LlmClient:
    """Talks to Groq or Gemini, both of which have free API tiers."""

    def __init__(self, provider: str | None = None, timeout: float | None = None) -> None:
        self.provider = provider or settings.ai_provider
        self.timeout = timeout or settings.request_timeout_seconds

    async def complete(self, prompt: str, system: str | None = None) -> str:
        if self.provider == "gemini":
            return await self._complete_gemini(prompt, system)
        return await self._complete_groq(prompt, system)

    async def _complete_groq(self, prompt: str, system: str | None) -> str:
        if not settings.groq_api_key:
            raise MissingCredentialError("GROQ_API_KEY")

        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                GROQ_URL,
                headers={"Authorization": f"Bearer {settings.groq_api_key}"},
                json={"model": settings.groq_model, "messages": messages, "temperature": 0.2},
            )

        if response.status_code >= 400:
            raise UpstreamError("groq", response.status_code)

        data: dict[str, Any] = response.json()
        choices: list[dict[str, Any]] = data.get("choices", [])
        if not choices:
            return ""
        message: dict[str, Any] = choices[0].get("message", {})
        return str(message.get("content", ""))

    async def _complete_gemini(self, prompt: str, system: str | None) -> str:
        if not settings.google_api_key:
            raise MissingCredentialError("GOOGLE_API_KEY")

        text = f"{system}\n\n{prompt}" if system else prompt
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                GEMINI_URL.format(model=settings.google_model),
                params={"key": settings.google_api_key},
                json={"contents": [{"role": "user", "parts": [{"text": text}]}]},
            )

        if response.status_code >= 400:
            raise UpstreamError("gemini", response.status_code)

        data: dict[str, Any] = response.json()
        candidates: list[dict[str, Any]] = data.get("candidates", [])
        if not candidates:
            return ""
        parts: list[dict[str, Any]] = candidates[0].get("content", {}).get("parts", [])
        return "".join(str(part.get("text", "")) for part in parts)

"""Keyword discovery from free SERP signals (People Also Ask and related searches)."""

from typing import Any

import httpx

from app.core.config import settings
from app.core.errors import UpstreamError
from app.modules.keyword_engine.intent import classify_intent, estimate_difficulty
from app.modules.keyword_engine.schemas import Keyword, KeywordResearchRequest
from app.modules.serp_engine import SerpQuery, SerpService
from app.modules.serp_engine.free_serp import SERPER_URL, get_serp_results

__all__ = [
    "KeywordResearcher",
    "classify_intent",
    "estimate_difficulty",
    "expand_keywords",
    "parse_serper_expansions",
]


def _clean(term: str) -> str:
    return " ".join(term.strip().strip("?.,").split()).lower()


def parse_serper_expansions(payload: dict[str, Any]) -> list[str]:
    """Pull People Also Ask questions and related searches out of a Serper response."""
    terms: list[str] = []
    for item in payload.get("peopleAlsoAsk", []):
        question = _clean(str(item.get("question", "")))
        if question:
            terms.append(question)
    for item in payload.get("relatedSearches", []):
        related = _clean(str(item.get("query", "")))
        if related:
            terms.append(related)
    return terms


async def _serper_expansions(
    seed: str, country: str, language: str, client: httpx.AsyncClient | None
) -> list[str]:
    payload = {"q": seed, "gl": country, "hl": language}
    headers = {"X-API-KEY": settings.serper_api_key or "", "Content-Type": "application/json"}
    if client is not None:
        response = await client.post(SERPER_URL, headers=headers, json=payload)
    else:
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as owned:
            response = await owned.post(SERPER_URL, headers=headers, json=payload)

    if response.status_code >= 400:
        raise UpstreamError("serper", response.status_code)
    return parse_serper_expansions(response.json())


async def expand_keywords(
    seed: str,
    *,
    limit: int = 20,
    country: str = "us",
    language: str = "en",
    client: httpx.AsyncClient | None = None,
) -> list[str]:
    """Expand a seed into related keywords.

    Uses Serper's People Also Ask and related searches when ``SERPER_API_KEY`` is set; otherwise
    derives candidates from the keyless SERP fallback (result titles), so it costs nothing.
    """
    seed_clean = _clean(seed)
    if settings.serper_api_key:
        candidates = await _serper_expansions(seed_clean, country, language, client)
    else:
        results = await get_serp_results(
            seed_clean, num_results=limit, country=country, language=language, client=client
        )
        candidates = [_clean(str(item["title"]).split("|")[0].split(" - ")[0]) for item in results]

    expansions: list[str] = []
    for term in candidates:
        if term and term != seed_clean and term not in expansions:
            expansions.append(term)
    return expansions[:limit]


class KeywordResearcher:
    def __init__(self, serp: SerpService | None = None) -> None:
        self.serp = serp or SerpService()

    async def research(self, request: KeywordResearchRequest) -> list[Keyword]:
        ranking = await self.serp.get_rankings(
            SerpQuery(keyword=request.seed, domain=request.domain, country=request.country)
        )

        terms: list[str] = [request.seed]
        for result in ranking.results:
            title = result.title.split("|")[0].split("-")[0].strip().lower()
            if title and title not in terms:
                terms.append(title)

        return [to_keyword(term) for term in terms[: request.limit]]


def to_keyword(term: str) -> Keyword:
    difficulty = estimate_difficulty(term)
    return Keyword(
        term=term,
        intent=classify_intent(term),
        difficulty=difficulty,
        opportunity=round(100.0 - difficulty, 2),
    )

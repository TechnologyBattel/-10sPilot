"""Keyword discovery from free SERP signals (related searches and PAA questions)."""

from app.modules.keyword_engine.schemas import Keyword, KeywordResearchRequest
from app.modules.serp_engine import SerpQuery, SerpService

QUESTION_PREFIXES = ("how", "what", "why", "when", "where", "who", "can", "is", "does")
COMMERCIAL_MARKERS = ("best", "top", "vs", "review", "pricing", "cheap", "alternative")


def classify_intent(term: str) -> str:
    lowered = term.lower()
    if lowered.startswith(QUESTION_PREFIXES):
        return "informational"
    if any(marker in lowered for marker in COMMERCIAL_MARKERS):
        return "commercial"
    if lowered.startswith(("buy", "order", "signup", "sign up")):
        return "transactional"
    return "navigational" if " " not in lowered else "informational"


def estimate_difficulty(term: str) -> float:
    """Longer, more specific phrases are cheaper to rank for."""
    words = max(len(term.split()), 1)
    return round(max(5.0, 95.0 - (words - 1) * 12.0), 2)


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

        keywords: list[Keyword] = []
        for term in terms[: request.limit]:
            difficulty = estimate_difficulty(term)
            keywords.append(
                Keyword(
                    term=term,
                    intent=classify_intent(term),
                    difficulty=difficulty,
                    opportunity=round(100.0 - difficulty, 2),
                )
            )
        return keywords

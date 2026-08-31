"""AEO service."""

from app.modules.aeo_engine.optimizer import score_aeo
from app.modules.aeo_engine.router import AEOResult
from app.modules.aeo_engine.schemas import AeoReport
from app.services.llm import LlmClient


class AeoService:
    def analyze(self, markdown: str) -> AeoReport:
        return score_aeo(markdown)


async def check_brand_visibility(
    brand: str,
    query: str,
    provider: str = "groq",
) -> AEOResult:
    llm = LlmClient(provider=provider)

    prompt = (
        f"Evaluate the brand visibility of {brand!r} for the query {query!r}. "
        "Return the answer as plain text and mention the brand's position in "
        "the answer if it is mentioned."
    )

    response = await llm.complete(prompt)

    lowered = response.lower()
    mentioned = brand.lower() in lowered

    position = None
    if mentioned:
        import re

        match = re.search(
            r"position\s+(\d+)|rank(?:ed)?\s+(?:at\s+)?(?:#)?(\d+)",
            lowered,
        )
        if match:
            position = int(next(group for group in match.groups() if group))

    return AEOResult(
        brand=brand,
        query=query,
        mentioned=mentioned,
        position=position,
        context=response,
        provider=provider,
    )

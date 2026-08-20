"""Content engine service."""

from app.modules.aeo_engine.optimizer import score_aeo
from app.modules.content_engine.prompts import SYSTEM_PROMPT, brief_prompt, draft_prompt
from app.modules.content_engine.schemas import ContentBrief, ContentDraft, ContentRequest
from app.modules.geo_engine.optimizer import score_geo
from app.modules.serp_engine import SerpQuery, SerpService
from app.services.llm import LlmClient


def _parse_outline(text: str) -> list[str]:
    return [
        line.lstrip("-*# ").strip()
        for line in text.splitlines()
        if line.strip().startswith(("-", "*", "#"))
    ]


class ContentService:
    def __init__(self, serp: SerpService | None = None, llm: LlmClient | None = None) -> None:
        self.serp = serp or SerpService()
        self.llm = llm or LlmClient()

    async def build_brief(self, request: ContentRequest) -> ContentBrief:
        ranking = await self.serp.get_rankings(
            SerpQuery(keyword=request.keyword, domain=request.domain)
        )
        competitors = [result.title for result in ranking.results[:10]]
        response = await self.llm.complete(
            brief_prompt(request.keyword, competitors), system=SYSTEM_PROMPT
        )
        outline = _parse_outline(response)
        return ContentBrief(
            keyword=request.keyword,
            title=outline[0] if outline else request.keyword.title(),
            outline=outline[1:] or outline,
            questions=[line for line in outline if line.endswith("?")],
            competitors=competitors,
        )

    async def generate(self, request: ContentRequest) -> ContentDraft:
        brief = await self.build_brief(request)
        markdown = await self.llm.complete(
            draft_prompt(request.keyword, brief.outline, request.tone, request.word_count),
            system=SYSTEM_PROMPT,
        )
        return ContentDraft(
            keyword=request.keyword,
            title=brief.title,
            markdown=markdown,
            aeo_score=score_aeo(markdown).score,
            geo_score=score_geo(markdown).score,
            word_count=len(markdown.split()),
        )

"""Keyword engine service."""

from app.modules.keyword_engine.clustering import cluster_keywords
from app.modules.keyword_engine.research import KeywordResearcher
from app.modules.keyword_engine.schemas import Keyword, KeywordCluster, KeywordResearchRequest


class KeywordService:
    def __init__(self, researcher: KeywordResearcher | None = None) -> None:
        self.researcher = researcher or KeywordResearcher()

    async def research(self, request: KeywordResearchRequest) -> list[Keyword]:
        return await self.researcher.research(request)

    async def research_and_cluster(self, request: KeywordResearchRequest) -> list[KeywordCluster]:
        return cluster_keywords(await self.research(request))

    def cluster(self, keywords: list[Keyword]) -> list[KeywordCluster]:
        return cluster_keywords(keywords)

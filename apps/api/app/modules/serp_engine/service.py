"""SERP engine service: the central ranking data source for every other engine."""

from app.modules.serp_engine.free_serp import GscClient, SerperClient, to_ranking
from app.modules.serp_engine.schemas import GscRow, RankingResult, SerpQuery


class SerpService:
    def __init__(self, serper: SerperClient | None = None, gsc: GscClient | None = None) -> None:
        self.serper = serper or SerperClient()
        self.gsc = gsc or GscClient()

    async def get_rankings(self, query: SerpQuery) -> RankingResult:
        results = await self.serper.search(query)
        return to_ranking(query, results)

    async def get_rankings_bulk(self, queries: list[SerpQuery]) -> list[RankingResult]:
        return [await self.get_rankings(query) for query in queries]

    async def get_search_console(self, start_date: str, end_date: str) -> list[GscRow]:
        return await self.gsc.query(start_date, end_date)

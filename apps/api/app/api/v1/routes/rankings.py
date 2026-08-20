"""Ranking endpoints backed by the SERP engine."""

from fastapi import APIRouter

from app.modules.serp_engine import GscRow, RankingResult, SerpQuery, SerpService

router = APIRouter()
service = SerpService()


@router.post("", response_model=RankingResult)
async def get_rankings(query: SerpQuery) -> RankingResult:
    return await service.get_rankings(query)


@router.post("/bulk", response_model=list[RankingResult])
async def get_rankings_bulk(queries: list[SerpQuery]) -> list[RankingResult]:
    return await service.get_rankings_bulk(queries)


@router.get("/search-console", response_model=list[GscRow])
async def search_console(start_date: str, end_date: str) -> list[GscRow]:
    return await service.get_search_console(start_date, end_date)

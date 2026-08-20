"""SERP engine: free ranking data from Serper.dev and Google Search Console."""

from app.modules.serp_engine.free_serp import get_serp_results
from app.modules.serp_engine.schemas import (
    GscRow,
    RankingResult,
    SerpQuery,
    SerpResult,
)
from app.modules.serp_engine.service import SerpService

__all__ = [
    "GscRow",
    "RankingResult",
    "SerpQuery",
    "SerpResult",
    "SerpService",
    "get_serp_results",
]

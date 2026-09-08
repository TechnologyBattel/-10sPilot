"""AI citation monitoring endpoints."""

from fastapi import APIRouter, Request

from app.core.limiter import limiter
from app.modules.citation_monitor import CitationCheck, CitationMonitorService, CitationRequest

router = APIRouter()
service = CitationMonitorService()


@router.post("/check", response_model=list[CitationCheck])
@limiter.limit("5/minute")
async def check(request: Request, payload: CitationRequest) -> list[CitationCheck]:
    return await service.check(payload)

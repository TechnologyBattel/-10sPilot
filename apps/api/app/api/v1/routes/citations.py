"""AI citation monitoring endpoints."""

from fastapi import APIRouter

from app.modules.citation_monitor import CitationCheck, CitationMonitorService, CitationRequest

router = APIRouter()
service = CitationMonitorService()


@router.post("/check", response_model=list[CitationCheck])
async def check(request: CitationRequest) -> list[CitationCheck]:
    return await service.check(request)

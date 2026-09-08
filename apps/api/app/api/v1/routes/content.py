"""Content generation endpoints (AEO + GEO optimized)."""

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.core.limiter import limiter
from app.modules.aeo_engine import AeoReport, AeoService
from app.modules.content_engine import ContentBrief, ContentDraft, ContentRequest, ContentService
from app.modules.geo_engine import GeoReport, GeoService

router = APIRouter()
service = ContentService()


class OptimizeRequest(BaseModel):
    markdown: str


class OptimizeResponse(BaseModel):
    aeo: AeoReport
    geo: GeoReport


@router.post("/brief", response_model=ContentBrief)
@limiter.limit("5/minute")
async def brief(request: Request, payload: ContentRequest) -> ContentBrief:
    return await service.build_brief(payload)


@router.post("/generate", response_model=ContentDraft)
@limiter.limit("5/minute")
async def generate(request: Request, payload: ContentRequest) -> ContentDraft:
    return await service.generate(payload)


@router.post("/optimize", response_model=OptimizeResponse)
@limiter.limit("30/minute")
def optimize(request: Request, payload: OptimizeRequest) -> OptimizeResponse:
    return OptimizeResponse(
        aeo=AeoService().analyze(payload.markdown), geo=GeoService().analyze(payload.markdown)
    )

"""Content generation endpoints (AEO + GEO optimized)."""

from fastapi import APIRouter
from pydantic import BaseModel

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
async def brief(request: ContentRequest) -> ContentBrief:
    return await service.build_brief(request)


@router.post("/generate", response_model=ContentDraft)
async def generate(request: ContentRequest) -> ContentDraft:
    return await service.generate(request)


@router.post("/optimize", response_model=OptimizeResponse)
def optimize(request: OptimizeRequest) -> OptimizeResponse:
    return OptimizeResponse(
        aeo=AeoService().analyze(request.markdown), geo=GeoService().analyze(request.markdown)
    )

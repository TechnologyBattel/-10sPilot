"""AEO engine - ChatGPT visibility tracker."""

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/aeo", tags=["aeo"])

class AEOCheckRequest(BaseModel):
    brand: str = Field(min_length=1)
    query: str = Field(min_length=1)
    providers: list[str] = Field(default=["openai"])

class AEOResult(BaseModel):
    brand: str
    query: str
    mentioned: bool
    position: int | None = None
    context: str | None = None
    provider: str

@router.post("/check", response_model=list[AEOResult])
async def check_aeo(req: AEOCheckRequest) -> list[AEOResult]:
    from app.modules.aeo_engine.service import check_brand_visibility
    results = []
    for provider in req.providers:
        result = await check_brand_visibility(req.brand, req.query, provider)
        results.append(result)
    return results

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "aeo_engine ready", "cost_per_check": ".01"}

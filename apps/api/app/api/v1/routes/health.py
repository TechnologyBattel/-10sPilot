"""Health endpoints."""

from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.services.health_service import get_health

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return get_health()

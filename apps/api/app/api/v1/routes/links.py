"""Internal linking endpoints."""

from fastapi import APIRouter, Request

from app.core.limiter import limiter
from app.modules.link_engine import LinkService, LinkSuggestion, LinkSuggestionRequest

router = APIRouter()
service = LinkService()


@router.post("/suggest", response_model=list[LinkSuggestion])
@limiter.limit("30/minute")
def suggest(request: Request, payload: LinkSuggestionRequest) -> list[LinkSuggestion]:
    return service.suggest(payload)

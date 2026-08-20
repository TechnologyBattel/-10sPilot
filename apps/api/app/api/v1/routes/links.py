"""Internal linking endpoints."""

from fastapi import APIRouter

from app.modules.link_engine import LinkService, LinkSuggestion, LinkSuggestionRequest

router = APIRouter()
service = LinkService()


@router.post("/suggest", response_model=list[LinkSuggestion])
def suggest(request: LinkSuggestionRequest) -> list[LinkSuggestion]:
    return service.suggest(request)

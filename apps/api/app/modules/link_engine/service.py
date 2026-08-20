"""Internal linking service: relevance-ranked anchor suggestions."""

from app.modules.keyword_engine.clustering import similarity
from app.modules.link_engine.schemas import LinkSuggestion, LinkSuggestionRequest


class LinkService:
    def suggest(self, request: LinkSuggestionRequest) -> list[LinkSuggestion]:
        source = request.source
        source_text = source.text.lower()
        suggestions: list[LinkSuggestion] = []

        for candidate in request.candidates:
            if candidate.url == source.url:
                continue

            anchor = candidate.target_keyword or candidate.title
            if not anchor:
                continue

            relevance = similarity(f"{source.title} {source.target_keyword}", anchor)
            already_linked = candidate.url in source_text
            if already_linked or relevance <= 0:
                continue

            mentioned = anchor.lower() in source_text
            suggestions.append(
                LinkSuggestion(
                    source_url=source.url,
                    target_url=candidate.url,
                    anchor_text=anchor,
                    relevance=round(min(relevance + (0.2 if mentioned else 0.0), 1.0), 3),
                    reason=(
                        "Anchor phrase already appears in the source copy."
                        if mentioned
                        else "Topically related page with no existing link."
                    ),
                )
            )

        suggestions.sort(key=lambda item: item.relevance, reverse=True)
        return suggestions[: request.max_suggestions]

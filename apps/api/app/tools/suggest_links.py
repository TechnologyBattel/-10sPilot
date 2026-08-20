"""MCP tool: suggest internal links for a page."""

from typing import Any

from app.modules.link_engine import LinkService, LinkSuggestionRequest
from app.tools.base import Tool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "source": {"type": "object"},
        "candidates": {"type": "array", "items": {"type": "object"}},
        "max_suggestions": {"type": "integer", "default": 5},
    },
    "required": ["source"],
}


async def run(arguments: dict[str, Any]) -> list[dict[str, Any]]:
    suggestions = LinkService().suggest(LinkSuggestionRequest(**arguments))
    return [suggestion.model_dump() for suggestion in suggestions]


tool = Tool(
    name="suggest_links",
    description="Suggest internal links from a source page to topically related pages.",
    input_schema=INPUT_SCHEMA,
    handler=run,
)

"""MCP tool: discover keyword opportunities from a seed term."""

from typing import Any

from app.modules.keyword_engine import KeywordResearchRequest, KeywordService
from app.tools.base import Tool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "seed": {"type": "string"},
        "domain": {"type": "string"},
        "limit": {"type": "integer", "default": 20},
    },
    "required": ["seed"],
}


async def run(arguments: dict[str, Any]) -> list[dict[str, Any]]:
    request = KeywordResearchRequest(**arguments)
    keywords = await KeywordService().research(request)
    return [keyword.model_dump() for keyword in keywords]


tool = Tool(
    name="research_keywords",
    description="Discover related keywords with intent, difficulty and opportunity scores.",
    input_schema=INPUT_SCHEMA,
    handler=run,
)

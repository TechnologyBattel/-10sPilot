"""MCP tool: fetch SERP rankings for a keyword."""

from typing import Any

from app.modules.serp_engine import SerpQuery, SerpService
from app.tools.base import Tool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "keyword": {"type": "string"},
        "domain": {"type": "string"},
        "country": {"type": "string", "default": "us"},
    },
    "required": ["keyword"],
}


async def run(arguments: dict[str, Any]) -> dict[str, Any]:
    query = SerpQuery(**arguments)
    ranking = await SerpService().get_rankings(query)
    return ranking.model_dump()


tool = Tool(
    name="get_rankings",
    description="Get the Google ranking position and top results for a keyword.",
    input_schema=INPUT_SCHEMA,
    handler=run,
)

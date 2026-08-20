"""MCP tool: group keywords into topical clusters."""

from typing import Any

from app.modules.keyword_engine import KeywordService
from app.modules.keyword_engine.schemas import Keyword
from app.tools.base import Tool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"keywords": {"type": "array", "items": {"type": "object"}}},
    "required": ["keywords"],
}


async def run(arguments: dict[str, Any]) -> list[dict[str, Any]]:
    raw: list[dict[str, Any]] = arguments.get("keywords", [])
    keywords = [
        Keyword(**item) if isinstance(item, dict) else Keyword(term=str(item)) for item in raw
    ]
    clusters = KeywordService().cluster(keywords)
    return [cluster.model_dump() for cluster in clusters]


tool = Tool(
    name="cluster_keywords",
    description="Cluster keywords into topic groups for content planning.",
    input_schema=INPUT_SCHEMA,
    handler=run,
)

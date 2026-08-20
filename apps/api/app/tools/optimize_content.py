"""MCP tool: score existing content for AEO and GEO."""

from typing import Any

from app.modules.aeo_engine import AeoService
from app.modules.geo_engine import GeoService
from app.tools.base import Tool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"markdown": {"type": "string"}},
    "required": ["markdown"],
}


async def run(arguments: dict[str, Any]) -> dict[str, Any]:
    markdown = str(arguments["markdown"])
    return {
        "aeo": AeoService().analyze(markdown).model_dump(),
        "geo": GeoService().analyze(markdown).model_dump(),
    }


tool = Tool(
    name="optimize_content",
    description="Score markdown content for answer-engine and generative-engine readiness.",
    input_schema=INPUT_SCHEMA,
    handler=run,
)

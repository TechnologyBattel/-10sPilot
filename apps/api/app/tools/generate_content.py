"""MCP tool: generate AEO/GEO optimized content."""

from typing import Any

from app.modules.content_engine import ContentRequest, ContentService
from app.tools.base import Tool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "keyword": {"type": "string"},
        "domain": {"type": "string"},
        "tone": {"type": "string"},
        "word_count": {"type": "integer", "default": 900},
    },
    "required": ["keyword"],
}


async def run(arguments: dict[str, Any]) -> dict[str, Any]:
    draft = await ContentService().generate(ContentRequest(**arguments))
    return draft.model_dump()


tool = Tool(
    name="generate_content",
    description="Draft an article optimized for both answer engines and generative engines.",
    input_schema=INPUT_SCHEMA,
    handler=run,
)

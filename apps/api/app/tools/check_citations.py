"""MCP tool: check whether a domain is cited by AI answer engines."""

from typing import Any

from app.modules.citation_monitor import CitationMonitorService, CitationRequest
from app.tools.base import Tool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "prompt": {"type": "string"},
        "domain": {"type": "string"},
        "brand": {"type": "string"},
        "engines": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["prompt", "domain"],
}


async def run(arguments: dict[str, Any]) -> list[dict[str, Any]]:
    checks = await CitationMonitorService().check(CitationRequest(**arguments))
    return [check.model_dump() for check in checks]


tool = Tool(
    name="check_citations",
    description="Ask ChatGPT, Perplexity and Gemini a prompt and report whether we are cited.",
    input_schema=INPUT_SCHEMA,
    handler=run,
)

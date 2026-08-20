"""MCP tool: run a technical SEO audit on a URL."""

from typing import Any

from app.modules.audit_engine import AuditRequest, AuditService
from app.tools.base import Tool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"url": {"type": "string"}},
    "required": ["url"],
}


async def run(arguments: dict[str, Any]) -> dict[str, Any]:
    report = await AuditService().audit(AuditRequest(**arguments))
    return report.model_dump()


tool = Tool(
    name="audit_page",
    description="Audit a page for technical SEO issues and return a score with findings.",
    input_schema=INPUT_SCHEMA,
    handler=run,
)

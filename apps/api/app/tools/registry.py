"""Registry of MCP tools available to the workflow agent."""

from typing import Any

from app.tools import (
    audit_page,
    check_citations,
    cluster_keywords,
    generate_content,
    get_rankings,
    optimize_content,
    research_keywords,
    suggest_links,
)
from app.tools.base import Tool

TOOL_MODULES = (
    get_rankings,
    research_keywords,
    cluster_keywords,
    audit_page,
    generate_content,
    optimize_content,
    check_citations,
    suggest_links,
)


class ToolRegistry:
    def __init__(self, tools: list[Tool] | None = None) -> None:
        self._tools: dict[str, Tool] = {tool.name: tool for tool in tools or []}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(f"unknown tool: {name}")
        return self._tools[name]

    def list_tools(self) -> list[Tool]:
        return list(self._tools.values())

    def describe(self) -> list[dict[str, Any]]:
        return [
            {"name": tool.name, "description": tool.description, "inputSchema": tool.input_schema}
            for tool in self.list_tools()
        ]

    async def call(self, name: str, arguments: dict[str, Any]) -> Any:
        return await self.get(name).handler(arguments)


def default_registry() -> ToolRegistry:
    return ToolRegistry([module.tool for module in TOOL_MODULES])

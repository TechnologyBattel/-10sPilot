"""MCP-style tools. Each module exposes a single callable the agent can invoke."""

from app.tools.registry import ToolRegistry, default_registry

__all__ = ["ToolRegistry", "default_registry"]

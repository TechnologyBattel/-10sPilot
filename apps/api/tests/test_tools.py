"""MCP tool registry tests."""

from fastapi.testclient import TestClient

from app.main import app
from app.tools.registry import default_registry

client = TestClient(app)


def test_registry_exposes_every_tool() -> None:
    names = {tool.name for tool in default_registry().list_tools()}
    assert {"get_rankings", "audit_page", "generate_content", "check_citations"} <= names


def test_list_tools_endpoint() -> None:
    response = client.get("/api/v1/tools")
    assert response.status_code == 200
    assert any(tool["name"] == "get_rankings" for tool in response.json())


def test_unknown_tool_returns_404() -> None:
    response = client.post("/api/v1/tools/call", json={"name": "nope", "arguments": {}})
    assert response.status_code == 404

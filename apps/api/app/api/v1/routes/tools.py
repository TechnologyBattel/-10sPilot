"""MCP tool discovery and invocation endpoints."""

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.errors import EngineError
from app.tools.registry import default_registry

router = APIRouter()
registry = default_registry()


class ToolCallRequest(BaseModel):
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


@router.get("")
def list_tools() -> list[dict[str, Any]]:
    return registry.describe()


@router.post("/call")
async def call_tool(request: ToolCallRequest) -> dict[str, Any]:
    try:
        return {"result": await registry.call(request.name, request.arguments)}
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except EngineError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error

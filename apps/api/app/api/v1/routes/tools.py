"""MCP tool discovery and invocation endpoints."""

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app.core.errors import EngineError
from app.core.limiter import limiter
from app.tools.registry import default_registry

router = APIRouter()
registry = default_registry()


class ToolCallRequest(BaseModel):
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


@router.get("")
@limiter.limit("60/minute")
def list_tools(request: Request) -> list[dict[str, Any]]:
    return registry.describe()


@router.post("/call")
@limiter.limit("30/minute")
async def call_tool(request: Request, payload: ToolCallRequest) -> dict[str, Any]:
    try:
        return {"result": await registry.call(payload.name, payload.arguments)}
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except EngineError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error

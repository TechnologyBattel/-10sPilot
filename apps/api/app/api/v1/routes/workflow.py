"""Autonomous workflow endpoints."""

from fastapi import APIRouter, Request

from app.core.limiter import limiter
from app.modules.workflow_engine import WorkflowRequest, WorkflowRun, WorkflowService

router = APIRouter()
service = WorkflowService()


@router.post("/run", response_model=WorkflowRun)
@limiter.limit("30/minute")
async def run(request: Request, payload: WorkflowRequest) -> WorkflowRun:
    return await service.run(payload)

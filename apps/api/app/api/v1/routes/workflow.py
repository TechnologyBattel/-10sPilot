"""Autonomous workflow endpoints."""

from fastapi import APIRouter

from app.modules.workflow_engine import WorkflowRequest, WorkflowRun, WorkflowService

router = APIRouter()
service = WorkflowService()


@router.post("/run", response_model=WorkflowRun)
async def run(request: WorkflowRequest) -> WorkflowRun:
    return await service.run(request)

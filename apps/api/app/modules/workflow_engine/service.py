"""Workflow engine service: runs the planned steps through the MCP tool registry."""

from datetime import datetime, timezone
from typing import Any

from app.core.errors import EngineError
from app.modules.workflow_engine.planner import plan
from app.modules.workflow_engine.schemas import WorkflowRequest, WorkflowRun, WorkflowStepResult
from app.tools.registry import ToolRegistry, default_registry


class WorkflowService:
    def __init__(self, registry: ToolRegistry | None = None) -> None:
        self.registry = registry or default_registry()

    async def run(self, request: WorkflowRequest) -> WorkflowRun:
        started_at = datetime.now(timezone.utc)
        run = WorkflowRun(
            project=request.project, domain=request.domain, started_at=started_at, status="running"
        )
        context: dict[str, Any] = {}

        for step, arguments in plan(request):
            if request.dry_run:
                run.steps.append(WorkflowStepResult(step=step, status="skipped"))
                continue

            if step == "cluster_keywords":
                arguments = {"keywords": context.get("research_keywords", [])}

            try:
                output = await self.registry.call(step, arguments)
                context[step] = output
                run.steps.append(WorkflowStepResult(step=step, output={"result": output}))
            except (EngineError, KeyError, ValueError) as error:
                run.steps.append(WorkflowStepResult(step=step, status="failed", error=str(error)))

        run.finished_at = datetime.now(timezone.utc)
        failed = any(step.status == "failed" for step in run.steps)
        run.status = "failed" if failed else "succeeded"
        return run

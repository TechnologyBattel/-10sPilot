"""Workflow engine tests using a stub tool registry."""

from typing import Any

import pytest

from app.modules.workflow_engine import WorkflowRequest, WorkflowService
from app.tools.base import Tool
from app.tools.registry import ToolRegistry


async def _echo(arguments: dict[str, Any]) -> dict[str, Any]:
    return {"received": arguments}


def _registry() -> ToolRegistry:
    names = ["research_keywords", "cluster_keywords", "get_rankings", "audit_page"]
    return ToolRegistry(
        [Tool(name=name, description=name, input_schema={}, handler=_echo) for name in names]
    )


@pytest.mark.asyncio
async def test_workflow_runs_requested_steps() -> None:
    service = WorkflowService(registry=_registry())
    run = await service.run(
        WorkflowRequest(
            project="demo",
            domain="example.com",
            seed_keyword="answer engine optimization",
            steps=["research_keywords", "get_rankings"],
        )
    )
    assert run.status == "succeeded"
    assert [step.step for step in run.steps] == ["research_keywords", "get_rankings"]


@pytest.mark.asyncio
async def test_workflow_marks_unknown_step_failed() -> None:
    service = WorkflowService(registry=_registry())
    run = await service.run(
        WorkflowRequest(
            project="demo",
            domain="example.com",
            seed_keyword="aeo",
            steps=["generate_content"],
        )
    )
    assert run.status == "failed"
    assert run.steps[0].error is not None


@pytest.mark.asyncio
async def test_dry_run_skips_every_step() -> None:
    service = WorkflowService(registry=_registry())
    run = await service.run(
        WorkflowRequest(project="demo", domain="example.com", seed_keyword="aeo", dry_run=True)
    )
    assert {step.status for step in run.steps} == {"skipped"}

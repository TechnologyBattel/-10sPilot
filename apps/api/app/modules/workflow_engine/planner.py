"""Turns a workflow request into an ordered list of tool invocations."""

from typing import Any

from app.modules.workflow_engine.schemas import WorkflowRequest

DEFAULT_PIPELINE = [
    "research_keywords",
    "cluster_keywords",
    "get_rankings",
    "audit_page",
    "generate_content",
    "suggest_links",
    "check_citations",
]


def plan(request: WorkflowRequest) -> list[tuple[str, dict[str, Any]]]:
    steps = request.steps or DEFAULT_PIPELINE
    arguments: dict[str, dict[str, Any]] = {
        "research_keywords": {"seed": request.seed_keyword, "domain": request.domain},
        "cluster_keywords": {"keywords": []},
        "get_rankings": {"keyword": request.seed_keyword, "domain": request.domain},
        "audit_page": {"url": request.url or f"https://{request.domain}"},
        "generate_content": {"keyword": request.seed_keyword, "domain": request.domain},
        "suggest_links": {"source": {"url": request.url or f"https://{request.domain}"}},
        "check_citations": {
            "prompt": f"What is the best tool for {request.seed_keyword}?",
            "domain": request.domain,
        },
    }
    return [(step, arguments.get(step, {})) for step in steps]

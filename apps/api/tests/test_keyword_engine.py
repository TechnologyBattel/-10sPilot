"""Keyword engine tests: TF-IDF clustering, seed expansion and the /api/v1/keywords router."""

from typing import Any

import httpx
import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from app.modules.keyword_engine.cluster import cluster_keywords
from app.modules.keyword_engine.research import expand_keywords

client = TestClient(app)

SERPER_EXPANSION_PAYLOAD = {
    "peopleAlsoAsk": [
        {"question": "What is answer engine optimization?"},
        {"question": "How does AEO differ from SEO?"},
    ],
    "relatedSearches": [
        {"query": "aeo tools"},
        {"query": "answer engine optimization"},
    ],
}


def test_cluster_keywords_groups_related_terms() -> None:
    result = cluster_keywords(
        [
            "answer engine optimization",
            "answer engine optimization guide",
            "what is answer engine optimization",
            "best espresso machine",
            "espresso machine reviews",
        ]
    )

    clusters = result["clusters"]
    grouped = {cluster["name"]: set(cluster["keywords"]) for cluster in clusters}
    assert len(clusters) == 2

    aeo = next(terms for terms in grouped.values() if "answer engine optimization" in terms)
    espresso = next(terms for terms in grouped.values() if "best espresso machine" in terms)
    assert "answer engine optimization guide" in aeo
    assert "espresso machine reviews" in espresso
    assert all(cluster["intent"] for cluster in clusters)


def test_cluster_keywords_handles_empty_input() -> None:
    assert cluster_keywords([]) == {"clusters": []}


@pytest.mark.asyncio
async def test_expand_keywords_parses_people_also_ask(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "serper_api_key", "test-key")

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["x-api-key"] == "test-key"
        return httpx.Response(200, json=SERPER_EXPANSION_PAYLOAD)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        expansions = await expand_keywords("answer engine optimization", client=http)

    # The seed itself is dropped, questions lose their trailing '?'.
    assert expansions == [
        "what is answer engine optimization",
        "how does aeo differ from seo",
        "aeo tools",
    ]


def test_keywords_router_expand_and_cluster(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_expand(seed: str, **_: Any) -> list[str]:
        return ["aeo tools", "what is aeo"]

    monkeypatch.setattr("app.modules.keyword_engine.router.expand_keywords", fake_expand)

    expand_response = client.post("/api/v1/keywords/expand", json={"seed": "aeo"})
    assert expand_response.status_code == 200
    assert expand_response.json() == {"seed": "aeo", "keywords": ["aeo tools", "what is aeo"]}

    cluster_response = client.post(
        "/api/v1/keywords/cluster",
        json={"keywords": ["seo audit tool", "seo audit checklist", "cold brew recipe"]},
    )
    assert cluster_response.status_code == 200
    clusters = cluster_response.json()["clusters"]
    assert len(clusters) == 2
    assert {"name", "keywords", "intent"} <= clusters[0].keys()

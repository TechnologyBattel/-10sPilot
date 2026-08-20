"""SERP engine tests: Serper path, keyless scrape fallback and the /api/v1/serp router."""

from typing import Any

import httpx
import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from app.modules.serp_engine.free_serp import get_serp_results
from app.modules.serp_engine.scrape import SCRAPE_URL

client = TestClient(app)

SERPER_PAYLOAD = {
    "organic": [
        {
            "position": 1,
            "title": "Answer engine optimization guide",
            "link": "https://example.com/aeo",
            "snippet": "How to rank in AI answers.",
        },
        {"position": 2, "title": "AEO basics", "link": "https://other.com/aeo"},
    ]
}

SCRAPE_HTML = """
<div class="result">
  <a class="result__a" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fexample.com%2Faeo">
    Answer engine <b>optimization</b> guide
  </a>
  <a class="result__snippet">How to rank in AI answers.</a>
</div>
<div class="result">
  <a class="result__a" href="https://other.com/aeo">AEO basics</a>
</div>
"""


@pytest.mark.asyncio
async def test_get_serp_results_uses_serper_when_key_is_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "serper_api_key", "test-key")

    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == "https://google.serper.dev/search"
        assert request.headers["x-api-key"] == "test-key"
        return httpx.Response(200, json=SERPER_PAYLOAD)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        results = await get_serp_results("answer engine optimization", client=http)

    assert [item["position"] for item in results] == [1, 2]
    assert results[0] == {
        "position": 1,
        "title": "Answer engine optimization guide",
        "url": "https://example.com/aeo",
        "snippet": "How to rank in AI answers.",
        "source": "serper",
    }


@pytest.mark.asyncio
async def test_get_serp_results_falls_back_to_scraping_without_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "serper_api_key", None)

    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url).startswith(SCRAPE_URL)
        return httpx.Response(200, text=SCRAPE_HTML)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        results = await get_serp_results("answer engine optimization", client=http)

    assert [item["url"] for item in results] == ["https://example.com/aeo", "https://other.com/aeo"]
    assert results[0]["title"] == "Answer engine optimization guide"
    assert results[0]["source"] == "scrape"


def test_serp_search_endpoint_reports_domain_position(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get_serp_results(keyword: str, **_: Any) -> list[dict[str, Any]]:
        return [
            {"position": 1, "title": "Other", "url": "https://other.com/a", "snippet": None},
            {"position": 2, "title": "Us", "url": "https://www.example.com/aeo", "snippet": "hi"},
        ]

    monkeypatch.setattr(
        "app.modules.serp_engine.router.get_serp_results",
        fake_get_serp_results,
    )

    response = client.post(
        "/api/v1/serp/search",
        json={"keyword": "answer engine optimization", "domain": "example.com"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["keyword"] == "answer engine optimization"
    assert body["domain_position"] == 2
    assert body["results"][1]["url"] == "https://www.example.com/aeo"

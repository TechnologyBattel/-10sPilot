import pytest
"""Engine unit tests that do not touch the network."""

from app.modules.aeo_engine.optimizer import score_aeo
from app.modules.audit_engine.checks import run_checks
from app.modules.geo_engine.optimizer import score_geo
from app.modules.keyword_engine.clustering import cluster_keywords
from app.modules.keyword_engine.research import classify_intent, estimate_difficulty
from app.modules.keyword_engine.schemas import Keyword
from app.modules.link_engine.schemas import LinkSuggestionRequest, PageSummary
from app.modules.link_engine.service import LinkService
from app.modules.serp_engine.free_serp import find_domain_position
from app.modules.serp_engine.schemas import SerpResult

MARKDOWN = """
Answer engines cite pages that answer fast. This page explains how in plain terms.

## What is AEO?

- Lead with the answer
- Use lists

| Tool | Price |
| --- | --- |
| 10sPilot | Free |

Conversion rose 42% in 2026.

## FAQ
"""


def test_aeo_scoring_rewards_structure() -> None:
    report = score_aeo(MARKDOWN)
    assert report.score > 50
    assert any(signal.name == "comparison_table" and signal.passed for signal in report.signals)


def test_geo_scoring_flags_missing_citations() -> None:
    report = score_geo(MARKDOWN)
    assert "Cite at least three authoritative sources with inline links." in report.recommendations


def test_keyword_intent_and_difficulty() -> None:
    assert classify_intent("best seo tool") == "commercial"
    assert classify_intent("how to rank on chatgpt") == "informational"
    assert estimate_difficulty("seo") > estimate_difficulty("how to rank on chatgpt in 2026")


def test_clustering_groups_related_terms() -> None:
    keywords = [
        Keyword(term="answer engine optimization", opportunity=90),
        Keyword(term="answer engine optimization guide", opportunity=80),
        Keyword(term="internal linking tools", opportunity=70),
    ]
    clusters = cluster_keywords(keywords)
    assert len(clusters) == 2


def test_audit_flags_missing_tags() -> None:
    issues = {issue.check for issue in run_checks("<html><body><p>hi</p></body></html>")}
    assert {"title", "h1", "canonical", "viewport", "thin_content"} <= issues


def test_find_domain_position() -> None:
    results = [
        SerpResult(position=1, title="Other", link="https://other.com/a"),
        SerpResult(position=2, title="Us", link="https://www.example.com/b"),
    ]
    match = find_domain_position(results, "example.com")
    assert match is not None and match.position == 2


def test_link_suggestions_rank_by_relevance() -> None:
    request = LinkSuggestionRequest(
        source=PageSummary(
            url="https://example.com/aeo",
            title="Answer engine optimization",
            target_keyword="answer engine optimization",
            text="Answer engine optimization is how you get cited by chatgpt.",
        ),
        candidates=[
            PageSummary(url="https://example.com/aeo-guide", target_keyword="answer engine guide"),
            PageSummary(url="https://example.com/pricing", target_keyword="pricing"),
        ],
    )
    suggestions = LinkService().suggest(request)
    assert suggestions and suggestions[0].target_url == "https://example.com/aeo-guide"


def test_aeo_brand_visibility_uses_llm(monkeypatch) -> None:
    from app.modules.aeo_engine import service

    class FakeLlm:
        def __init__(self, provider: str | None = None) -> None:
            self.provider = provider

        async def complete(self, prompt: str, system: str | None = None) -> str:
            assert "10sPilot" in prompt
            assert "Best SEO tools" in prompt
            return "10sPilot is mentioned at position 2."

    monkeypatch.setattr(service, "LlmClient", FakeLlm)

    result = __import__("asyncio").run(
        service.check_brand_visibility(
            brand="10sPilot",
            query="Best SEO tools",
        )
    )

    assert result.mentioned is True
    assert result.position == 2
    assert "10sPilot" in (result.context or "")

@pytest.mark.asyncio
async def test_aeo_rejects_unsupported_provider(monkeypatch) -> None:
    from app.modules.aeo_engine import service

    with pytest.raises(ValueError):
        await service.check_brand_visibility(
            brand="10sPilot", query="Best SEO tools", provider="openai"
        )

def test_assert_safe_url_blocks_private_ip() -> None:
    from app.core.url_safety import UnsafeUrlError, assert_safe_url

    with pytest.raises(UnsafeUrlError):
        assert_safe_url("http://127.0.0.1/")

    with pytest.raises(UnsafeUrlError):
        assert_safe_url("http://169.254.169.254/")

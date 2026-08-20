"""GEO heuristics: authority, citations and entity coverage."""

import re

from app.modules.geo_engine.schemas import GeoReport, GeoSignal

CITATION_RE = re.compile(r"\[[^\]]+\]\(https?://[^)]+\)")
QUOTE_RE = re.compile(r"^>\s+", re.MULTILINE)
AUTHOR_RE = re.compile(r"\b(author|written by|reviewed by)\b", re.IGNORECASE)
DATE_RE = re.compile(r"\b(20\d{2})\b")


def score_geo(markdown: str) -> GeoReport:
    citations = CITATION_RE.findall(markdown)
    signals = [
        GeoSignal(
            name="external_citations",
            passed=len(citations) >= 3,
            detail="Cite at least three authoritative sources with inline links.",
        ),
        GeoSignal(
            name="quotable_statements",
            passed=bool(QUOTE_RE.search(markdown)),
            detail="Blockquotes give generative engines ready-made pull quotes.",
        ),
        GeoSignal(
            name="author_signals",
            passed=bool(AUTHOR_RE.search(markdown)),
            detail="Name an author or reviewer to establish E-E-A-T.",
        ),
        GeoSignal(
            name="freshness",
            passed=bool(DATE_RE.search(markdown)),
            detail="Reference the current year so the page reads as fresh.",
        ),
        GeoSignal(
            name="entity_density",
            passed=len(set(re.findall(r"\b[A-Z][a-z]{2,}\b", markdown))) >= 8,
            detail="Mention the named entities of the topic (brands, tools, people).",
        ),
    ]
    passed = sum(1 for signal in signals if signal.passed)
    return GeoReport(
        score=round(passed / len(signals) * 100, 2),
        signals=signals,
        recommendations=[signal.detail for signal in signals if not signal.passed],
    )

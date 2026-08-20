"""Heuristics that decide whether an answer engine can lift a direct answer."""

import re

from app.modules.aeo_engine.schemas import AeoReport, AeoSignal

QUESTION_RE = re.compile(r"^#{2,3}\s+.*\?\s*$", re.MULTILINE)
LIST_RE = re.compile(r"^\s*([-*]|\d+\.)\s+", re.MULTILINE)
TABLE_RE = re.compile(r"^\|.+\|$", re.MULTILINE)
STAT_RE = re.compile(r"\b\d+(\.\d+)?\s*(%|percent|x)\b", re.IGNORECASE)


def _first_paragraph(markdown: str) -> str:
    for block in markdown.split("\n\n"):
        cleaned = block.strip()
        if cleaned and not cleaned.startswith("#"):
            return cleaned
    return ""


def score_aeo(markdown: str) -> AeoReport:
    lead = _first_paragraph(markdown)
    signals = [
        AeoSignal(
            name="direct_answer_lead",
            passed=0 < len(lead.split()) <= 80,
            detail="Opening paragraph should answer the query in under 80 words.",
        ),
        AeoSignal(
            name="question_headings",
            passed=bool(QUESTION_RE.search(markdown)),
            detail="Use question-shaped H2/H3 headings so answers map to prompts.",
        ),
        AeoSignal(
            name="structured_lists",
            passed=bool(LIST_RE.search(markdown)),
            detail="Lists and steps are extracted more often than prose.",
        ),
        AeoSignal(
            name="comparison_table",
            passed=bool(TABLE_RE.search(markdown)),
            detail="A comparison table wins 'best X' style answers.",
        ),
        AeoSignal(
            name="verifiable_stats",
            passed=bool(STAT_RE.search(markdown)),
            detail="Concrete numbers make the passage citation-worthy.",
        ),
        AeoSignal(
            name="faq_block",
            passed="faq" in markdown.lower(),
            detail="An FAQ block covers long-tail follow-up prompts.",
        ),
    ]
    passed = sum(1 for signal in signals if signal.passed)
    return AeoReport(
        score=round(passed / len(signals) * 100, 2),
        signals=signals,
        recommendations=[signal.detail for signal in signals if not signal.passed],
    )

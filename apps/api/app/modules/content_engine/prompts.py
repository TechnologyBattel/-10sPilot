"""Prompt templates for content generation."""

SYSTEM_PROMPT = (
    "You are 10sPilot, an SEO/AEO/GEO content strategist. "
    "You write factual, citation-friendly content that answer engines can quote directly."
)


def brief_prompt(keyword: str, competitors: list[str]) -> str:
    listed = "\n".join(f"- {item}" for item in competitors) or "- (no competitor data)"
    return (
        f"Create a content brief for the keyword '{keyword}'.\n"
        f"Top ranking pages:\n{listed}\n\n"
        "Return a title, an H2 outline (6-10 items) and 5 questions the page must answer."
    )


def draft_prompt(keyword: str, outline: list[str], tone: str, word_count: int) -> str:
    sections = "\n".join(f"- {item}" for item in outline)
    return (
        f"Write a {word_count}-word markdown article targeting '{keyword}'.\n"
        f"Tone: {tone}.\n"
        f"Follow this outline:\n{sections}\n\n"
        "Lead each section with a direct, quotable answer of 2-3 sentences, "
        "use tables or lists where useful, and include a short FAQ."
    )

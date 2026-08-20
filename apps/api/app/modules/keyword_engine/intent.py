"""Heuristic search-intent classification and difficulty estimation."""

QUESTION_PREFIXES = ("how", "what", "why", "when", "where", "who", "can", "is", "does")
COMMERCIAL_MARKERS = ("best", "top", "vs", "review", "pricing", "cheap", "alternative")


def classify_intent(term: str) -> str:
    lowered = term.lower()
    if lowered.startswith(QUESTION_PREFIXES):
        return "informational"
    if any(marker in lowered for marker in COMMERCIAL_MARKERS):
        return "commercial"
    if lowered.startswith(("buy", "order", "signup", "sign up")):
        return "transactional"
    return "navigational" if " " not in lowered else "informational"


def estimate_difficulty(term: str) -> float:
    """Longer, more specific phrases are cheaper to rank for."""
    words = max(len(term.split()), 1)
    return round(max(5.0, 95.0 - (words - 1) * 12.0), 2)

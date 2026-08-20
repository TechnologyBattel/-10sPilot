"""Cluster `Keyword` objects on top of the TF-IDF clustering in `cluster.py`."""

from app.modules.keyword_engine.cluster import DEFAULT_THRESHOLD, group_terms
from app.modules.keyword_engine.schemas import Keyword, KeywordCluster

STOPWORDS = {"the", "a", "an", "for", "to", "of", "and", "in", "on", "with", "best", "how"}


def tokens(term: str) -> set[str]:
    return {word for word in term.lower().split() if word not in STOPWORDS}


def similarity(left: str, right: str) -> float:
    """Jaccard token overlap, used where a cheap pairwise score is enough."""
    left_tokens, right_tokens = tokens(left), tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def cluster_keywords(
    keywords: list[Keyword], threshold: float = DEFAULT_THRESHOLD
) -> list[KeywordCluster]:
    by_term = {keyword.term: keyword for keyword in keywords}
    groups = group_terms(list(by_term), threshold)
    return [
        KeywordCluster(
            label=min(group, key=lambda term: (len(term.split()), len(term))),
            keywords=[by_term[term] for term in group],
        )
        for group in groups
    ]

"""Lightweight keyword clustering (no ML dependency, token overlap based)."""

from app.modules.keyword_engine.schemas import Keyword, KeywordCluster

STOPWORDS = {"the", "a", "an", "for", "to", "of", "and", "in", "on", "with", "best", "how"}


def tokens(term: str) -> set[str]:
    return {word for word in term.lower().split() if word not in STOPWORDS}


def similarity(left: str, right: str) -> float:
    left_tokens, right_tokens = tokens(left), tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def cluster_keywords(keywords: list[Keyword], threshold: float = 0.34) -> list[KeywordCluster]:
    clusters: list[KeywordCluster] = []

    for keyword in sorted(keywords, key=lambda item: item.opportunity, reverse=True):
        for cluster in clusters:
            if similarity(cluster.label, keyword.term) >= threshold:
                cluster.keywords.append(keyword)
                break
        else:
            clusters.append(KeywordCluster(label=keyword.term, keywords=[keyword]))

    return clusters

"""TF-IDF + cosine similarity keyword clustering (scikit-learn, no paid API)."""

from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.modules.keyword_engine.intent import classify_intent

DEFAULT_THRESHOLD = 0.25


def _cluster_name(terms: list[str]) -> str:
    """The shortest term is the most head-like phrasing of the group."""
    return min(terms, key=lambda term: (len(term.split()), len(term)))


def _cluster_intent(terms: list[str]) -> str:
    counts: dict[str, int] = {}
    for term in terms:
        intent = classify_intent(term)
        counts[intent] = counts.get(intent, 0) + 1
    return max(counts.items(), key=lambda item: item[1])[0]


def group_terms(keywords: list[str], threshold: float = DEFAULT_THRESHOLD) -> list[list[str]]:
    """Greedy agglomeration over the TF-IDF cosine similarity matrix.

    Each term joins the first existing group whose average similarity clears ``threshold``, which
    keeps clusters topical without needing a preset cluster count.
    """
    terms = [term.strip() for term in keywords if term and term.strip()]
    if not terms:
        return []
    if len(terms) == 1:
        return [terms]

    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True)
    matrix = vectorizer.fit_transform(terms)
    similarity = cosine_similarity(matrix)

    groups: list[list[int]] = []
    for index in range(len(terms)):
        for group in groups:
            score = sum(float(similarity[index][member]) for member in group) / len(group)
            if score >= threshold:
                group.append(index)
                break
        else:
            groups.append([index])

    return [[terms[index] for index in group] for group in groups]


def cluster_keywords(
    keywords: list[str], threshold: float = DEFAULT_THRESHOLD
) -> dict[str, list[dict[str, Any]]]:
    """Cluster raw keyword strings into ``{"clusters": [{name, keywords, intent}]}``."""
    return {
        "clusters": [
            {"name": _cluster_name(group), "keywords": group, "intent": _cluster_intent(group)}
            for group in group_terms(keywords, threshold)
        ]
    }

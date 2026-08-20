"""Zero-key SERP fallback used for local development.

Serper.dev is the primary provider, but a fresh checkout has no ``SERPER_API_KEY``. Scraping the
JS-free DuckDuckGo HTML endpoint keeps the engine usable at $0 without any credential. It is
best-effort: rate limits and markup changes can return an empty list.
"""

import html
import re
from urllib.parse import parse_qs, unquote, urlparse

import httpx

from app.modules.serp_engine.schemas import SerpResult

SCRAPE_URL = "https://html.duckduckgo.com/html/"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0 Safari/537.36"
)

_RESULT_RE = re.compile(
    r'<a[^>]+class="[^"]*result__a[^"]*"[^>]+href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>'
    r'(?P<rest>.*?)(?=<a[^>]+class="[^"]*result__a|\Z)',
    re.DOTALL,
)
_SNIPPET_RE = re.compile(r'class="[^"]*result__snippet[^"]*"[^>]*>(?P<snippet>.*?)</a>', re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")


def _text(raw: str) -> str:
    return html.unescape(_TAG_RE.sub("", raw)).strip()


def _clean_link(href: str) -> str:
    """DuckDuckGo wraps results in a redirect such as ``//duckduckgo.com/l/?uddg=<url>``."""
    if href.startswith("//"):
        href = f"https:{href}"
    parsed = urlparse(href)
    target = parse_qs(parsed.query).get("uddg")
    return unquote(target[0]) if target else href


def _is_ad(link: str) -> bool:
    """Sponsored rows stay on the engine's own redirect host instead of the target site."""
    host = urlparse(link).netloc.removeprefix("www.")
    return host.endswith("duckduckgo.com") or host.endswith("bing.com")


def parse_scraped_results(markup: str, limit: int) -> list[SerpResult]:
    results: list[SerpResult] = []
    for match in _RESULT_RE.finditer(markup):
        link = _clean_link(match.group("href"))
        title = _text(match.group("title"))
        if not link or not title or _is_ad(link):
            continue
        snippet_match = _SNIPPET_RE.search(match.group("rest"))
        results.append(
            SerpResult(
                position=len(results) + 1,
                title=title,
                link=link,
                snippet=_text(snippet_match.group("snippet")) if snippet_match else None,
            )
        )
        if len(results) >= limit:
            break
    return results


async def scrape_serp(
    keyword: str,
    *,
    limit: int = 10,
    country: str = "us",
    language: str = "en",
    client: httpx.AsyncClient | None = None,
    timeout: float = 20.0,
) -> list[SerpResult]:
    params = {"q": keyword, "kl": f"{country}-{language}"}
    headers = {"User-Agent": USER_AGENT}
    if client is not None:
        response = await client.get(SCRAPE_URL, params=params, headers=headers)
    else:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as owned:
            response = await owned.get(SCRAPE_URL, params=params, headers=headers)

    if response.status_code >= 400:
        return []
    return parse_scraped_results(response.text, limit)

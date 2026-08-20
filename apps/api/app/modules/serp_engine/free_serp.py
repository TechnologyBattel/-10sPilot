"""Free SERP data providers.

Serper.dev gives 2,500 free Google searches and Google Search Console is free for verified
properties, so together they cover ranking data at zero cost.
"""

from typing import Any
from urllib.parse import urlparse

import httpx

from app.core.config import settings
from app.core.errors import MissingCredentialError, UpstreamError
from app.modules.serp_engine.schemas import GscRow, RankingResult, SerpQuery, SerpResult
from app.modules.serp_engine.scrape import scrape_serp

SERPER_URL = "https://google.serper.dev/search"
GSC_URL_TEMPLATE = (
    "https://searchconsole.googleapis.com/webmasters/v3/sites/{site}/searchAnalytics/query"
)


def _domain_of(url: str) -> str:
    return urlparse(url).netloc.removeprefix("www.")


class SerperClient:
    """Thin client over the Serper.dev free Google Search API."""

    def __init__(self, api_key: str | None = None, timeout: float | None = None) -> None:
        self.api_key = api_key or settings.serper_api_key
        self.timeout = timeout or settings.request_timeout_seconds

    async def search(
        self, query: SerpQuery, client: httpx.AsyncClient | None = None
    ) -> list[SerpResult]:
        if not self.api_key:
            raise MissingCredentialError("SERPER_API_KEY")

        payload = {
            "q": query.keyword,
            "gl": query.country,
            "hl": query.language,
            "num": query.num_results,
        }
        headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}
        if client is not None:
            response = await client.post(SERPER_URL, headers=headers, json=payload)
        else:
            async with httpx.AsyncClient(timeout=self.timeout) as owned:
                response = await owned.post(SERPER_URL, headers=headers, json=payload)

        if response.status_code >= 400:
            raise UpstreamError("serper", response.status_code)

        data: dict[str, Any] = response.json()
        organic: list[dict[str, Any]] = data.get("organic", [])
        return [
            SerpResult(
                position=int(item.get("position", index + 1)),
                title=str(item.get("title", "")),
                link=str(item.get("link", "")),
                snippet=item.get("snippet"),
            )
            for index, item in enumerate(organic)
        ]


class GscClient:
    """Google Search Console Search Analytics client (free for verified sites)."""

    def __init__(
        self,
        access_token: str | None = None,
        site_url: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self.access_token = access_token or settings.gsc_access_token
        self.site_url = site_url or settings.gsc_site_url
        self.timeout = timeout or settings.request_timeout_seconds

    async def query(self, start_date: str, end_date: str, limit: int = 100) -> list[GscRow]:
        if not self.access_token:
            raise MissingCredentialError("GSC_ACCESS_TOKEN")
        if not self.site_url:
            raise MissingCredentialError("GSC_SITE_URL")

        url = GSC_URL_TEMPLATE.format(site=httpx.URL(self.site_url).raw_path.decode())
        payload = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": ["query", "page"],
            "rowLimit": limit,
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                url,
                headers={"Authorization": f"Bearer {self.access_token}"},
                json=payload,
            )

        if response.status_code >= 400:
            raise UpstreamError("google-search-console", response.status_code)

        data: dict[str, Any] = response.json()
        rows: list[dict[str, Any]] = data.get("rows", [])
        parsed: list[GscRow] = []
        for row in rows:
            keys: list[str] = row.get("keys", [])
            parsed.append(
                GscRow(
                    query=keys[0] if keys else "",
                    page=keys[1] if len(keys) > 1 else None,
                    clicks=int(row.get("clicks", 0)),
                    impressions=int(row.get("impressions", 0)),
                    ctr=float(row.get("ctr", 0.0)),
                    position=float(row.get("position", 0.0)),
                )
            )
        return parsed


def find_domain_position(results: list[SerpResult], domain: str) -> SerpResult | None:
    target = domain.removeprefix("www.")
    for result in results:
        if _domain_of(result.link) == target:
            return result
    return None


async def get_serp_results(
    keyword: str,
    *,
    num_results: int = 10,
    country: str = "us",
    language: str = "en",
    client: httpx.AsyncClient | None = None,
) -> list[dict[str, Any]]:
    """Return organic results as ``{position, title, url, snippet}`` dicts.

    Uses Serper.dev when ``SERPER_API_KEY`` is set (2,500 free searches per month) and falls back
    to scraping a JS-free HTML SERP so local development works with no key at all.
    """
    query = SerpQuery(keyword=keyword, country=country, language=language, num_results=num_results)
    if settings.serper_api_key:
        results = await SerperClient().search(query, client=client)
        source = "serper"
    else:
        results = await scrape_serp(
            keyword,
            limit=num_results,
            country=country,
            language=language,
            client=client,
        )
        source = "scrape"

    return [
        {
            "position": result.position,
            "title": result.title,
            "url": result.link,
            "snippet": result.snippet,
            "source": source,
        }
        for result in results[:num_results]
    ]


def to_ranking(query: SerpQuery, results: list[SerpResult]) -> RankingResult:
    match = find_domain_position(results, query.domain) if query.domain else None
    return RankingResult(
        keyword=query.keyword,
        domain=query.domain,
        position=match.position if match else None,
        url=match.link if match else None,
        results=results,
    )

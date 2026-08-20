# Engines and tools

| Engine | Path | Responsibility |
| --- | --- | --- |
| SERP | `app/modules/serp_engine` | Serper.dev search + Google Search Console rows, with a keyless HTML scrape fallback; central ranking source |
| Keyword | `app/modules/keyword_engine` | Seed expansion from SERP signals (People Also Ask + related searches), intent classification, TF-IDF/cosine clustering |
| Content | `app/modules/content_engine` | Briefs and drafts, scored by the AEO and GEO engines |
| Audit | `app/modules/audit_engine` | Technical SEO checks (title, meta, H1, alt, canonical, JSON-LD, viewport, thin content) |
| AEO | `app/modules/aeo_engine` | Answer Engine Optimization signals for ChatGPT / Perplexity extraction |
| GEO | `app/modules/geo_engine` | Generative Engine Optimization: citations, quotes, authorship, freshness, entities |
| Citation monitor | `app/modules/citation_monitor` | Probes ChatGPT, Perplexity and Gemini and records whether we are cited |
| Link | `app/modules/link_engine` | Relevance-ranked internal link suggestions with anchor text |
| Workflow | `app/modules/workflow_engine` | Autonomous agent that plans and chains every MCP tool |

## SERP endpoints

`POST /api/v1/serp/search` with `{"keyword": "...", "domain": "example.com"}` returns
`{keyword, domain, results[{position, title, url, snippet}], domain_position}`.

`get_serp_results(keyword)` in `free_serp.py` is the single entry point: it calls Serper.dev when
`SERPER_API_KEY` is set and otherwise scrapes a JS-free HTML SERP (`scrape.py`) so local
development needs no key. Scraping is best-effort — rate limits can yield an empty list.

## Keyword endpoints

- `POST /api/v1/keywords/expand` `{seed}` → `{seed, keywords[]}` — `expand_keywords()` reads
  People Also Ask and related searches from Serper, or falls back to the keyless SERP scrape.
- `POST /api/v1/keywords/cluster` `{keywords: []}` → `{clusters: [{name, keywords, intent}]}` —
  `cluster_keywords()` uses scikit-learn TF-IDF character n-grams plus cosine similarity, so no
  paid embedding API is involved.
- `POST /api/v1/keywords/research` and `/clusters` return the richer `Keyword` objects (intent,
  difficulty, opportunity).

## MCP tools

`GET /api/v1/tools` lists them, `POST /api/v1/tools/call` invokes one.

| Tool | Module |
| --- | --- |
| `get_rankings` | `app/tools/get_rankings.py` |
| `research_keywords` | `app/tools/research_keywords.py` |
| `cluster_keywords` | `app/tools/cluster_keywords.py` |
| `audit_page` | `app/tools/audit_page.py` |
| `generate_content` | `app/tools/generate_content.py` |
| `optimize_content` | `app/tools/optimize_content.py` |
| `check_citations` | `app/tools/check_citations.py` |
| `suggest_links` | `app/tools/suggest_links.py` |

Default workflow pipeline: `research_keywords → cluster_keywords → get_rankings → audit_page →
generate_content → suggest_links → check_citations`.

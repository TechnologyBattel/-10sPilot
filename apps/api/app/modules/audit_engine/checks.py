"""HTML checks used by the technical audit."""

import re

from app.modules.audit_engine.schemas import AuditIssue

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
META_DESC_RE = re.compile(
    r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"'](.*?)[\"']", re.IGNORECASE
)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
ALT_RE = re.compile(r"\balt=", re.IGNORECASE)
CANONICAL_RE = re.compile(r"<link[^>]+rel=[\"']canonical[\"']", re.IGNORECASE)
JSONLD_RE = re.compile(r"application/ld\+json", re.IGNORECASE)
VIEWPORT_RE = re.compile(r"<meta[^>]+name=[\"']viewport[\"']", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")


def extract_title(html: str) -> str | None:
    match = TITLE_RE.search(html)
    return match.group(1).strip() if match else None


def extract_meta_description(html: str) -> str | None:
    match = META_DESC_RE.search(html)
    return match.group(1).strip() if match else None


def visible_text(html: str) -> str:
    without_scripts = re.sub(
        r"<(script|style)\b.*?</\1>", " ", html, flags=re.IGNORECASE | re.DOTALL
    )
    return TAG_RE.sub(" ", without_scripts)


def run_checks(html: str) -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    title = extract_title(html)
    description = extract_meta_description(html)
    h1s = H1_RE.findall(html)
    images = IMG_RE.findall(html)

    if not title:
        issues.append(AuditIssue(check="title", severity="error", message="Missing <title>."))
    elif not 15 <= len(title) <= 65:
        issues.append(
            AuditIssue(check="title", message=f"Title length {len(title)} is outside 15-65 chars.")
        )

    if not description:
        issues.append(AuditIssue(check="meta_description", message="Missing meta description."))
    elif not 70 <= len(description) <= 165:
        issues.append(
            AuditIssue(
                check="meta_description",
                message=f"Meta description length {len(description)} is outside 70-165 chars.",
            )
        )

    if len(h1s) != 1:
        issues.append(
            AuditIssue(
                check="h1", severity="error", message=f"Found {len(h1s)} H1 tags, expected 1."
            )
        )

    missing_alt = [tag for tag in images if not ALT_RE.search(tag)]
    if missing_alt:
        issues.append(
            AuditIssue(check="image_alt", message=f"{len(missing_alt)} images without alt text.")
        )

    if not CANONICAL_RE.search(html):
        issues.append(AuditIssue(check="canonical", message="Missing canonical link."))

    if not JSONLD_RE.search(html):
        issues.append(
            AuditIssue(check="structured_data", message="No JSON-LD structured data found.")
        )

    if not VIEWPORT_RE.search(html):
        issues.append(
            AuditIssue(check="viewport", severity="error", message="Missing viewport meta tag.")
        )

    if len(visible_text(html).split()) < 300:
        issues.append(AuditIssue(check="thin_content", message="Fewer than 300 visible words."))

    return issues

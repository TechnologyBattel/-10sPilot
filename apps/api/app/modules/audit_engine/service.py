"""Technical SEO audit service."""

import httpx

from app.core.config import settings
from app.core.url_safety import assert_safe_url
from app.modules.audit_engine.checks import (
    extract_meta_description,
    extract_title,
    run_checks,
    visible_text,
)
from app.modules.audit_engine.schemas import AuditIssue, AuditReport, AuditRequest

MAX_SCORE_ISSUES = 10


class AuditService:
    def __init__(self, timeout: float | None = None) -> None:
        self.timeout = timeout or settings.request_timeout_seconds

    async def audit(self, request: AuditRequest) -> AuditReport:
        assert_safe_url(request.url)
        async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=False) as client:
            response = await client.get(request.url, headers={"User-Agent": "10sPilotBot/0.1"})

        html = response.text
        issues = run_checks(html)
        if response.status_code >= 400:
            issues.append(
                AuditIssue(
                    check="status_code",
                    severity="error",
                    message=f"Page returned HTTP {response.status_code}.",
                )
            )

        penalty = min(len(issues), MAX_SCORE_ISSUES) / MAX_SCORE_ISSUES * 100
        return AuditReport(
            url=request.url,
            status_code=response.status_code,
            score=round(100 - penalty, 2),
            issues=issues,
            title=extract_title(html),
            meta_description=extract_meta_description(html),
            word_count=len(visible_text(html).split()),
        )

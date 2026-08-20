"""Technical SEO audit endpoints."""

from fastapi import APIRouter

from app.modules.audit_engine import AuditReport, AuditRequest, AuditService

router = APIRouter()
service = AuditService()


@router.post("", response_model=AuditReport)
async def audit(request: AuditRequest) -> AuditReport:
    return await service.audit(request)

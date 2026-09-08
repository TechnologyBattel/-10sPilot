"""Technical audit routes."""

from fastapi import APIRouter, HTTPException, Request

from app.core.limiter import limiter
from app.core.url_safety import UnsafeUrlError
from app.modules.audit_engine.schemas import AuditReport, AuditRequest
from app.modules.audit_engine.service import AuditService

router = APIRouter(prefix="/api/v1/audit", tags=["audit"])


@router.post("", response_model=AuditReport)
@limiter.limit("30/minute")
async def run_audit(request: Request, req: AuditRequest) -> AuditReport:
    service = AuditService()
    try:
        return await service.audit(req)
    except UnsafeUrlError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "audit_engine ready"}

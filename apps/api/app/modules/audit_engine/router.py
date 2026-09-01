"""Technical audit routes."""

from fastapi import APIRouter, HTTPException

from app.core.url_safety import UnsafeUrlError
from app.modules.audit_engine.schemas import AuditReport, AuditRequest
from app.modules.audit_engine.service import AuditService

router = APIRouter(prefix="/api/v1/audit", tags=["audit"])


@router.post("", response_model=AuditReport)
async def run_audit(req: AuditRequest) -> AuditReport:
    service = AuditService()
    try:
        return await service.audit(req)
    except UnsafeUrlError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "audit_engine ready"}

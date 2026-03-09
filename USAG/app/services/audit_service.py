from datetime import datetime
from typing import Optional, Dict, Any

from app.db import get_database
from app.models import AuditLogCreate


async def log_event(
    request_id: str,
    user_id: Optional[str],
    role: Optional[str],
    path: str,
    method: str,
    status_code: int,
    client_ip: str,
    compliance_tag: Optional[str],
    extra: Optional[Dict[str, Any]] = None,
):
    db = get_database()
    collection = db["audit_logs"]

    audit_log = AuditLogCreate(
        request_id=request_id,
        user_id=user_id,
        role=role,
        endpoint=path,
        method=method,
        status_code=status_code,
        ip_address=client_ip,
        compliance_tag=compliance_tag,
        extra=extra or {},
    )

    document = audit_log.model_dump()
    document["role"] = role
    document["extra"] = extra or {}
    document["timestamp"] = datetime.utcnow()

    await collection.insert_one(audit_log.model_dump())
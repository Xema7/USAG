from fastapi import APIRouter, Query
from typing import Optional

from app.db.mongodb import get_database
from app.models import AuditLogInDB

router = APIRouter()

@router.get("/logs", response_model=list[AuditLogInDB])
async def get_audit_logs(
    user_id: Optional[str] = Query(None),
    endpoint: Optional[str] = Query(None),
    compliance_tag: Optional[str] = Query(None),
):
    db = get_database()
    collection = db["audit_logs"]

    filters = {}
    if user_id:
        filters["user_id"] = user_id
    if endpoint:
        filters["endpoint"] = endpoint
    if compliance_tag:
        filters["compliance_tag"] = compliance_tag

    cursor = collection.find(filters).sort("timestamp", -1).limit(100)

    logs = []
    async for document in cursor:
        document["_id"] = str(document["_id"])
        logs.append(AuditLogInDB(**document))

    return logs

print("AUDIT ROUTE HIT")
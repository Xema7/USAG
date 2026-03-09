from fastapi import APIRouter, Request
from app.services import analyze_security
from app.db.mongodb import get_database

router = APIRouter()

@router.get("/security-report")
async def security_report():

    db = get_database()
    collection = db["audit_logs"]

    cursor = collection.find().sort("timestamp", -1).limit(50)

    logs = []
    async for document in cursor:
        document["_id"] = str(document["_id"])
        logs.append(document)

    result = await analyze_security(logs)

    return result
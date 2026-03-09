from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class AuditLogBase(BaseModel):
    request_id: str
    user_id: Optional[str] = None
    role: Optional[str] = None
    endpoint: str
    method: str
    status_code: int
    ip_address: str
    compliance_tag: Optional[str] = None
    extra: Optional[Dict[str, Any]] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AuditLogCreate(AuditLogBase):
    pass

class AuditLogInDB(AuditLogBase):
    id: Optional[str] = Field(default=None, alias="_id")

    model_config = {
        "populate_by_name": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, Literal


class ProxyRequest(BaseModel):
    path: str
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
    headers: Dict[str, str] = Field(default_factory=dict)
    body: Optional[Dict[str, Any]] = None


class AIValidationRequest(BaseModel):
    content: str
    risk_level: Literal["Low", "Medium", "High"] = "Low"
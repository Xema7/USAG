from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Literal

UserRole = Literal["admin", "user", "auditor"]


class UserBase(BaseModel):
    email: EmailStr
    role: UserRole


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserInDB(UserBase):
    id: Optional[str] = Field(default=None, alias="_id")
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }

class UserResponse(UserBase):
    id: str
    created_at: datetime

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }
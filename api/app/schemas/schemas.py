from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MeOut(BaseModel):
    id: UUID
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    language: str = "en"
    consent_json: dict = {}

class IssueCreateIn(BaseModel):
    title: Optional[str] = Field(None, max_length=120)
    description: str = Field(..., max_length=2000)
    category: Optional[str] = None
    lat: float
    lng: float
    address: Optional[str] = None
    public_visibility: bool = True
    consent: bool = True

class MediaOut(BaseModel):
    id: UUID
    role: str
    url: str
    created_at: datetime

class IssueOut(BaseModel):
    id: UUID
    status: str
    severity: Optional[int] = None
    category: Optional[str] = None
    sla_due_at: Optional[datetime] = None
    lat: float
    lng: float
    address: Optional[str] = None
    title: Optional[str] = None
    description: str
    media: List[MediaOut] = []
    created_at: datetime

class IssueListOut(BaseModel):
    items: List[IssueOut]
    next_cursor: Optional[str] = None

class CommentIn(BaseModel):
    body: str = Field(..., max_length=1000)

class ReopenIn(BaseModel):
    reason: str = Field(..., max_length=500)

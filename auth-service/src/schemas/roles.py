from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class Role(BaseModel):
    id: UUID
    title: str
    created: datetime
    permissions: Optional[list] = []

    class Config:
        orm_mode = True


class Permission(Role):
    id: UUID
    category: str
    action: str
    created: datetime


class RoleCreate(BaseModel):
    title: str
    permissions: Optional[list[str]] = []

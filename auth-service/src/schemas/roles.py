from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class PermissionCreate(BaseModel):
    id: UUID
    name: str


class PermissionDb(PermissionCreate):
    action: str
    created: datetime


class Role(BaseModel):
    id: UUID
    title: str
    created: datetime
    permissions: Optional[list[PermissionDb]] = []

    class Config:
        orm_mode = True



# class PermissionResponse()

class RoleCreate(BaseModel):
    title: str
    permissions: Optional[list[str]] = []

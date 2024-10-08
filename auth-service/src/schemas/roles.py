from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from enum import Enum

class Action(Enum):
    read = 'read'
    write = 'write'
    delete = 'delete'


class Category(BaseModel):
    id: UUID
    title: str

class PermissionCreate(BaseModel):
    category: UUID
    action: Action

class PermissionDb(BaseModel):
    id: UUID
    category: Category
    action: Action
    created: datetime
    category_title: str


class Role(BaseModel):
    id: UUID
    title: str
    created: datetime
    permissions: Optional[list[PermissionDb]] = []




# class PermissionResponse()

class RoleCreate(BaseModel):
    title: str
    permissions: Optional[list[UUID]] = []

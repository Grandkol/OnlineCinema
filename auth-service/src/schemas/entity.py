from uuid import UUID
from typing import Union

from pydantic import BaseModel
from typing_extensions import Optional


class UserCreate(BaseModel):
    login: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserInDB(BaseModel):
    id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class AuthUser(BaseModel):
    login: str
    password: str


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

class RefreshToken(BaseModel):
    refresh_token: str

from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    login: str
    password: str
    first_name: str
    last_name: str


class UserInDB(BaseModel):
    id: UUID
    first_name: str
    last_name: str


class TokenInfo(BaseModel):
    access_token: str
    token_type: str

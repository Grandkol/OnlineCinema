import uuid
from datetime import datetime
from enum import unique
from datetime import datetime
from typing import Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from redis.commands.search.querystring import union
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from typing_extensions import Union
from werkzeug.security import check_password_hash, generate_password_hash



from models import Base


class User(Base):

    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    role: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[Union[str, None]] = mapped_column(nullable=True)
    first_name: Mapped[Union[str, None]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(default=True)

    def __init__(
        self, login: str, password: str, first_name: str, last_name: str
    ) -> None:
        self.login = login
        self.password = self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


    def __repr__(self) -> str:
        return f"<User {self.login}>"

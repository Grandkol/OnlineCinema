import uuid
from datetime import datetime

from sqlalchemy.sql import func
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.types import DateTime
from uuid import UUID

from werkzeug.security import check_password_hash, generate_password_hash

from db.postgres import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID_PG(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, login: str, password: str, first_name: str, last_name: str) -> None:
        self.login = login
        self.password = self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f'<User {self.login}>'


roles_permissions_table = Table(
    "roles_permissions",
    Base.metadata,
    Column('id', UUID_PG),
    Column('role_id', ForeignKey("roles.id")),
    Column('permission_id', ForeignKey("permissions.id")),
)

class Roles(Base):
    __tablename__ = 'roles'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    title: Mapped[str]
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    permissions: Mapped[list["Permissions"]] = relationship(secondary=roles_permissions_table)




class Permissions(Base):
    __tablename__ = 'permissions'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

import uuid
import enum
from datetime import datetime
from typing import Optional

from sqlalchemy.sql import func
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy import Boolean, Column, DateTime, String, Enum
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy.types import DateTime
from uuid import UUID

from db.postgres import Base


roles_permissions_table = Table(
    "roles_permissions",
    Base.metadata,
    Column('id', UUID_PG),
    Column('role_id', ForeignKey("roles.id")),
    Column('permission_id', ForeignKey("permissions.id")),
)

class Roles(Base):
    __tablename__ = 'roles'

<<<<<<< Updated upstream
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
=======

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
>>>>>>> Stashed changes
    title: Mapped[str]
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    permissions: Mapped[Optional[list["Permissions"]]] = relationship(secondary=roles_permissions_table, lazy='selectin')





class Category(Base):
    __tablename__ = 'category'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    title: Mapped[str]



class Permissions(Base):
    __tablename__ = 'permissions'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    category: Mapped[Category] = mapped_column(ForeignKey('category.id'))
    action: Mapped[str]
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

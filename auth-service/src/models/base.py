from packaging.metadata import Metadata
from pydantic.v1.schema import schema
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy.testing.suite.test_reflection import metadata


class Base(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {"schema": "auth"}

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

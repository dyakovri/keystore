from datetime import datetime
from enum import Enum
from functools import total_ordering

from sqlalchemy import JSON, DateTime, Enum as DbEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models.base import BaseDbModel


class Access(str, Enum):
    OWNER = "OWNER"
    RW = "RW"
    R = "R"


class Secret(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    create_ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    update_ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Version(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    secret_id: Mapped[int] = mapped_column(Integer, ForeignKey(Secret.id), nullable=False)
    num: Mapped[int] = mapped_column(Integer, primary_key=False, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    value: Mapped[JSON] = mapped_column(JSON, nullable=False)


class SecretOwners(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    secret_id: Mapped[int] = mapped_column(Integer, ForeignKey(Secret.id), nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False)
    access: Mapped[Access] = mapped_column(DbEnum(Access, native_enum=False))


class SecretKey(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    secret: Mapped[str] = mapped_column(String, nullable=False)

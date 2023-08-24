from enum import StrEnum
from api.models.base import BaseDbModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, JSON, ForeignKey, Enum
from datetime import datetime
from functools import total_ordering

@total_ordering
class Access(StrEnum):
    OWNER = "OWNER"
    RW = "RW"
    R = "R"

    def _is_valid_operand(self, other):
        return isinstance(other, str) and other in [e.value for e in Access]

    def __eq__(self, other: object) -> bool:
        if not self._is_valid_operand(other):
            raise TypeError()
        return other == self
    
    def __lt__(self, other: str) -> bool:
        if not self._is_valid_operand(other):
            raise TypeError()
        _levels = {"R": 0, "RW": 1, "OWNER": 2}
        _self = int(_levels[self])
        return _self.__lt__(_levels[other])


class Secret(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    create_ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    update_ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Version(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    num: Mapped[int] = mapped_column(Integer, primary_key=False, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    value: Mapped[JSON] = mapped_column(JSON, nullable=False)

class SecretOwners(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    secret_id: Mapped[int] = mapped_column(Integer, ForeignKey(Secret.id), nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False)
    access: Mapped[Access] = mapped_column(Enum(Access, native_enum=False))


class SecretKey(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    secret: Mapped[str] = mapped_column(String, nullable=False)
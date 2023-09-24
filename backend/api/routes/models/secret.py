from datetime import datetime

from api.routes.models.base import Base


class SecretPost(Base):
    name: str
    description: str


class SecretGet(SecretPost):
    create_ts: datetime
    update_ts: datetime


class SecretPut(SecretPost):
    name: str | None = None

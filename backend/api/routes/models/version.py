from api.routes.models.base import Base
from pydantic import Json


class VersionPost(Base):
    value: Json
    description: str | None = None

class VersionGet(VersionPost):
    id: int
    num: int

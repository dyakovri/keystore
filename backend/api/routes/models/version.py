from api.routes.models.base import Base


class VersionPost(Base):
    value: dict[str, str]
    description: str | None = None

class VersionGet(VersionPost):
    id: int
    num: int

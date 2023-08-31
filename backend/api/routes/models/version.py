from api.routes.models.base import Base


class VersionPost(Base):
    value: list[dict[str, str]]
    description: str | None = None


class VersionGet(VersionPost):
    id: int
    num: int

from api.routes.models.base import Base

class Version(Base):
    key: str
    value: str


class VersionPost(Base):
    value: list[Version]
    description: str | None = None


class VersionGet(VersionPost):
    id: int
    num: int

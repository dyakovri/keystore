from  api.routes.models.base import Base


class ACLGet(Base):
    owner: str
    rw: list[str]
    r: list[str]

from api.routes.models.base import Base



class ACLPost(Base):
    rw: list[str]
    r: list[str]


class ACLGet(ACLPost):
    owner: str
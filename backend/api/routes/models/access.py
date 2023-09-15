from api.routes.models.base import Base



class ACLPost(Base):
    RW: list[int]
    R: list[int]


class ACLGet(ACLPost):
    OWNER: int
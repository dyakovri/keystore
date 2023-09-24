from api.routes.models.base import Base


class Seal(Base):
    token: str


class Unseal(Seal):
    pass


class ResetToken(Base):
    old_token: str
    new_token: str

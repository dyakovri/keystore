import uuid

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db
from pydantic.type_adapter import TypeAdapter

from api.models.db import Access, Secret, SecretOwners
from api.utils.secret import get_secret_owner_by_secret_id, get_secret_owner_by_secret_name
from api.utils.security import token_security

from .models.secret import SecretGet, SecretPost, SecretPut


secret = APIRouter(prefix="/secret")


@secret.post("", response_model=SecretGet)
async def create_secret(data: SecretPost, auth=Depends(UnionAuth(scopes=[])), _=Depends(token_security)) -> SecretGet:
    if get_secret_owner_by_secret_name(db.session, data.name, auth["id"]):
        raise HTTPException(status_code=409, detail="Already exists")
    _secret = Secret(**data.model_dump(), id=uuid.uuid4())
    db.session.add(_secret)
    db.session.flush()
    _owner = SecretOwners(secret_id=_secret.id, owner_id=auth["id"], access=Access.OWNER)
    db.session.add(_owner)
    db.session.flush()
    return SecretGet(**data.model_dump(), id=str(_secret.id), create_ts=_secret.create_ts, update_ts=_secret.update_ts)


@secret.get("/{name}", response_model=SecretGet)
async def get_secret(name: str, auth=Depends(UnionAuth(scopes=[])), _=Depends(token_security)) -> SecretGet:
    _secret = (
        db.session.query(Secret)
        .join(SecretOwners)
        .filter(Secret.name == name, SecretOwners.owner_id == auth["id"])
        .one_or_none()
    )
    if not _secret:
        raise HTTPException(status_code=404, detail="Secret not found")
    return SecretGet.model_validate(_secret)


@secret.get("", response_model=list[SecretGet])
async def get_secrets(auth=Depends(UnionAuth(scopes=[])), _=Depends(token_security)) -> list[SecretGet]:
    secrets = Secret.query(session=db.session).join(SecretOwners).filter(SecretOwners.owner_id == auth["id"]).all()
    adapter = TypeAdapter(list[SecretGet])
    return adapter.validate_python(secrets)


@secret.put("/{name}", response_model=SecretGet)
async def update_secret(
    name: str, data: SecretPut, auth=Depends(UnionAuth(scopes=[])), _=Depends(token_security)
) -> SecretGet:
    _secret = (
        db.session.query(Secret)
        .join(SecretOwners)
        .filter(Secret.name == name, SecretOwners.owner_id == auth["id"])
        .one_or_none()
    )
    if not _secret:
        raise HTTPException(status_code=404, detail="Secret not found")
    _secret_owner = get_secret_owner_by_secret_id(db.session, _secret.id, auth["id"])
    if _secret_owner.access == "R":
        raise HTTPException(status_code=403, detail="Not enough scopes, RW required")
    return SecretGet.model_validate(
        Secret.update(_secret.id, **data.model_dump(exclude_unset=True), session=db.session)
    )

import importlib
from copy import deepcopy

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from api import config
from api.models.db import Access, Secret, SecretOwners, Version
from api.utils.cipher import AESCipher
from api.utils.random_string import random_string

from .models.access import ACLGet, ACLPost


acl = APIRouter(prefix="/secret/{name}/access")


@acl.get("", response_model=ACLGet)
async def get_acl(name: str, auth=Depends(UnionAuth(scopes=[]))):
    owners = db.session.query(SecretOwners).join(Secret).filter(Secret.name == name).all()
    result: dict[str, list[str] | str] = {}
    result["RW"] = []
    result["R"] = []
    for owner in owners:
        if owner.owner_id == auth["id"]:
            break
    else:
        raise HTTPException(status_code=404, detail="Secret not found")
    for owner in owners:
        if owner.access == "OWNER":
            result["OWNER"] = owner.owner_id
            continue
        result[owner.access].append(owner.owner_id)
    return result


@acl.post("", response_model=ACLGet)
async def update_acl(name: str, new: ACLPost, auth=Depends(UnionAuth(scopes=[]))):
    owner = (
        db.session.query(SecretOwners)
        .join(Secret)
        .filter(Secret.name == name, SecretOwners.owner_id == auth["id"])
        .one_or_none()
    )
    if not owner:
        raise HTTPException(status_code=404, detail="Secret not found")
    if owner.access != "OWNER":
        raise HTTPException(status_code=403, detail="ACL can be changed only by secret owner")
    secret = db.session.query(Secret).filter(Secret.name == name).one_or_none()
    db.session.query(SecretOwners).filter(SecretOwners.secret_id == secret.id, SecretOwners.access != "OWNER").delete()
    for rw in new.RW:
        db.session.add(SecretOwners(owner_id=rw, secret_id=owner.secret_id, access="RW"))
    db.session.flush()
    for r in new.R:
        db.session.add(SecretOwners(owner_id=r, secret_id=owner.secret_id, access="R"))
    db.session.flush()
    return {"OWNER": owner.owner_id, **new.model_dump()}
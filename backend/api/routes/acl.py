import importlib
from copy import deepcopy

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from api import config
from api.models.db import Access, Secret, SecretOwners, Version
from api.utils.cipher import AESCipher
from api.utils.random_string import random_string

from .models.access import ACLGet


acl = APIRouter(prefix="/secret/{name}/access")


@acl.get(response_model=ACLGet)
async def get_acl(name: str, auth=Depends(UnionAuth(scopes=[]))):
    owners = db.session.query(SecretOwners).join(Secret).filter(Secret.name == name).all()
    result: dict[str, list[str] | str] = {}
    result["r"] = []
    result["rw"] = []
    for owner in owners:
        if owner.owner_id == auth["id"]:
            break
    else:
        raise HTTPException(status_code=404, detail="Secret not found")
    for owner in owners:
        if owner.access == "owner":
            result["owner"] = owner.owner_id
            continue
        result[owner.access].append(owner.owner_id)
    return result


@acl.post(response_model=ACLGet)
async def update_acl(name: str, new: ACLGet, auth=Depends(UnionAuth(scopes=[]))):
    owner = (
        db.session.query(SecretOwners)
        .join(Secret)
        .filter(Secret.name == name, SecretOwners.owner_id == auth["id"])
        .one_or_none()
    )
    if not owner:
        raise HTTPException(status_code=404, detail="Secret not found")
    if Access(owner.access) < Access("OWNER"):
        raise HTTPException(status_code=403, detail="ACL can be changed only by secret owner")
    db.session.query(SecretOwners).join(Secret).filter(Secret.name == name).delete()
    new_owner = 5

    # result: dict[str, list[str] | str] = {}
    # result["r"] = []
    # result["rw"] = []
    # for owner in owners:
    #     if owner.owner_id == auth["id"]:
    #         break
    # else:
    #     raise HTTPException(status_code=404, detail="Secret not found")

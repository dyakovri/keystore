from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from api.models.db import Secret, SecretOwners
from api.utils.secret import get_secret_owner_by_secret_name
from api.utils.security import token_security

from .models.access import ACLGet, ACLPost


acl = APIRouter(prefix="/secret/{name}/access")


@acl.get("", response_model=ACLGet)
async def get_acl(name: str, auth=Depends(UnionAuth(scopes=[])), _=Depends(token_security)):
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
async def update_acl(name: str, new: ACLPost, auth=Depends(UnionAuth(scopes=[])), _=Depends(token_security)):
    owner = get_secret_owner_by_secret_name(db.session, name, auth["id"])
    if not owner:
        raise HTTPException(status_code=404, detail="Secret not found")
    if owner.access != "OWNER":
        raise HTTPException(status_code=403, detail="ACL can be changed only by secret owner")
    secret = db.session.query(Secret).filter(Secret.name == name).one_or_none()
    db.session.query(SecretOwners).filter(SecretOwners.secret_id == secret.id, SecretOwners.access != "OWNER").delete()
    if multiply_access := frozenset(new.RW) & frozenset(new.R):
        raise HTTPException(status_code=400, detail=f"Muliply access: {tuple(_ for _ in multiply_access)}")
    for rw in new.RW:
        if rw == owner.owner_id:
            raise HTTPException(status_code=400, detail="Owner cannot be in RW")
        db.session.add(SecretOwners(owner_id=rw, secret_id=owner.secret_id, access="RW"))
    db.session.flush()
    for r in new.R:
        if r == owner.owner_id:
            raise HTTPException(status_code=400, detail="Owner cannot be in R")
        db.session.add(SecretOwners(owner_id=r, secret_id=owner.secret_id, access="R"))
    db.session.flush()
    return {"OWNER": owner.owner_id, **new.model_dump()}

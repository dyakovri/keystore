import base64
import importlib

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from api.config import get_token
from api.models.db import Secret, SecretOwners, Version
from api.utils.cipher import AESCipher
from api.utils.random_string import random_string
from api.utils.secret import (
    decrypt_secret,
    encrypt_secret,
    get_secret_owner_by_secret_id,
    get_secret_owner_by_secret_name,
)
from api.utils.security import token_security

from .models.version import VersionGet, VersionPost


versions = APIRouter(prefix="/secret/{name}/version")


@versions.get("", response_model=list[VersionGet])
async def get_versions(name: str, auth=Depends(UnionAuth(scopes=[])), _=Depends(token_security)):
    password = get_token().decode(encoding="utf-8")
    cipher = AESCipher(password=password)
    versions = db.session.query(Version).join(Secret).filter(Secret.name == name).all()
    owner = (
        db.session.query(SecretOwners)
        .join(Secret)
        .filter(Secret.name == name, SecretOwners.owner_id == auth["id"])
        .one_or_none()
    )
    if not owner:
        raise HTTPException(status_code=404, detail="Secret not found")
    result: list[list[dict[str, str]]] = []
    for version in versions:
        _result = []
        for item in version.value:
            _result.append(decrypt_secret(cipher, item))
        result.append({"id": version.id, "num": version.num, "value": _result, "description": version.description})
    return result


@versions.get("/{number}", response_model=VersionGet)
async def get_version(number: int, name: str, auth=Depends(UnionAuth(scopes=[])), _=Depends(token_security)):
    password = get_token().decode(encoding="utf-8")
    cipher = AESCipher(password=password)
    version = db.session.query(Version).join(Secret).filter(Version.num == number, Secret.name == name).one_or_none()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    owner = get_secret_owner_by_secret_id(db.session, version.secret_id, auth["id"])
    if not owner or not version:
        raise HTTPException(status_code=404, detail="Secret not found")
    result = []
    for item in version.value:
        result.append(decrypt_secret(cipher, item))
    return {"id": version.id, "num": version.num, "value": result, "description": version.description}


@versions.post("", response_model=VersionGet)
async def create_version(name: str, data: VersionPost, auth=Depends(UnionAuth(scopes=[])), _=Depends(token_security)):
    password = get_token().decode(encoding="utf-8")
    cipher = AESCipher(password=password)
    _secret = (
        db.session.query(Secret)
        .join(SecretOwners)
        .filter(Secret.name == name, SecretOwners.owner_id == auth["id"])
        .one_or_none()
    )
    if not _secret:
        raise HTTPException(status_code=404, detail="Secret not found")
    _secret_owner = get_secret_owner_by_secret_id(db.session, _secret.id, auth["id"])
    if not _secret_owner:
        raise HTTPException(status_code=404, detail="Secret not found")
    if _secret_owner.access == "R":
        raise HTTPException(status_code=403, detail="Not enough scopes, RW required")
    encrypted_secret = []
    for item in data.value:
        encrypted_secret.append(encrypt_secret(cipher, item))
    num = db.session.query(Version).filter(Version.secret_id == _secret.id).count() + 1
    version = Version(value=encrypted_secret, secret_id=_secret.id, num=num, description=data.description)
    db.session.add(version)
    db.session.flush()
    return version

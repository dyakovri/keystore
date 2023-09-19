import importlib
from copy import deepcopy

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from api import config
from api.models.db import Access, Secret, SecretOwners, Version
from api.utils.cipher import AESCipher
from api.utils.random_string import random_string
import base64
from .models.version import VersionGet, VersionPost


versions = APIRouter(prefix="/secret/{name}/version")


@versions.get("", response_model=list[VersionGet])
async def get_versions(name: str, auth=Depends(UnionAuth(scopes=[]))):
    importlib.reload(config)
    password = config.token.value.decode(encoding = "utf-8")
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
            value: str = cipher.decrypt(base64.b64decode(item["value"]), bytes(item["salt"], encoding="utf-8"))     
            value = value.decode("utf-8")    
            value = value.removesuffix(item["salt"])
            _secret = {"key": item["key"], "value": value}
            _result.append(_secret)
        result.append({"id": version.id, "num": version.num, "value": _result, "description": version.description})
    return result


@versions.get("/{number}", response_model=VersionGet)
async def get_version(number: str, name: str, auth=Depends(UnionAuth(scopes=[]))):
    importlib.reload(config)
    password = config.token.value.decode(encoding = "utf-8")
    cipher = AESCipher(password=password)
    version = db.session.query(Version).join(Secret).filter(Version.num == number, Secret.name == name).one_or_none()
    owner = (
        db.session.query(SecretOwners)
        .filter(SecretOwners.secret_id == version.secret_id, SecretOwners.owner_id == auth["id"])
        .one_or_none()
    )
    if not owner or not version:
        raise HTTPException(status_code=404, detail="Secret not found")
    result = []
    for item in version.value:
        value: str = cipher.decrypt(base64.b64decode(item["value"]), bytes(item["salt"], encoding="utf-8"))     
        value = value.decode("utf-8")    
        value = value.removesuffix(item["salt"])
        _secret = {"key": item["key"], "value": value}
        result.append(_secret)
    return {"id": version.id, "num": version.num, "value": result, "description": version.description}


@versions.post("", response_model=VersionGet)
async def create_version(name: str, data: VersionPost, auth=Depends(UnionAuth(scopes=[]))):
    importlib.reload(config)
    password = config.token.value.decode(encoding = "utf-8")
    cipher = AESCipher(password=password)
    assert password
    _secret = (
        db.session.query(Secret)
        .join(SecretOwners)
        .filter(Secret.name == name, SecretOwners.owner_id == auth["id"])
        .one_or_none()
    )
    if not _secret:
        raise HTTPException(status_code=404, detail="Secret not found")
    _secret_owner = (
        db.session.query(SecretOwners)
        .filter(SecretOwners.secret_id == _secret.id, SecretOwners.owner_id == auth["id"])
        .one()
    )
    if _secret_owner.access == "R":
        raise HTTPException(status_code=403, detail="Not enough scopes, RW required")
    encrypted_secret = []
    for item in data.value:
        salt = random_string()
        value = cipher.encrypt(bytes(item.value, "utf-8"), bytes(salt, "utf-8"))
        value = base64.b64encode(value).decode("utf-8")
        encrypted_secret.append({"key": item.key, "value": value, "salt": salt})
    num = db.session.query(Version).filter(Version.secret_id == _secret.id).count() + 1
    version = Version(value=encrypted_secret, secret_id=_secret.id, num=num, description=data.description)
    db.session.add(version)
    db.session.flush()
    return version

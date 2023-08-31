import importlib
from copy import deepcopy

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from api import config
from api.models.db import Access, Secret, SecretOwners, Version
from api.utils.cipher import AESCipher
from api.utils.random_string import random_string

from .models.version import VersionGet, VersionPost


versions = APIRouter(prefix="/secret/{name}/version")


@versions.get("", response_model=list[VersionGet])
async def get_versions(name: str, auth=Depends(UnionAuth(scopes=[]))):
    importlib.reload(config)
    cipher = AESCipher(password=config.token.value)
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
            _secret = {"key": item["key"], "value": cipher.decrypt(item["value"], item["salt"])}
            _result.append(_secret)
        result.append(_result)
    return result


@versions.get("/{number}", response_model=VersionGet)
async def get_version(number: str, name: str, auth=Depends(UnionAuth(scopes=[]))):
    importlib.reload(config)
    cipher = AESCipher(password=config.token.value)
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
        _secret = {"key": item["key"], "value": cipher.decrypt(item["value"], item["salt"])}
        result.append(_secret)
    return result


@versions.post("", response_model=VersionGet)
async def create_version(name: str, data: VersionPost, auth=Depends(UnionAuth(scopes=[]))):
    importlib.reload(config)
    cipher = AESCipher(password=config.token.value)
    _secret = (
        db.session.query(Secret)
        .join(SecretOwners)
        .filter(Secret.name == name, SecretOwners.owner_id == auth["id"])
        .one_or_none()
    )
    if not _secret:
        raise HTTPException(status_code=404, detail="Secret not found")
    update_scope = Access("RW")
    _secret_owner = (
        db.session.query(SecretOwners)
        .filter(SecretOwners.secret_id == _secret.id, SecretOwners.owner_id == auth["id"])
        .one()
    )
    if Access(_secret_owner.access) < update_scope:
        raise HTTPException(status_code=403, detail="Not enough scopes, RW required")
    for item in data.value:
        salt = random_string()
        item["value"] = cipher.encrypt(item["value"], salt)
        item["salt"] = salt
    num = db.session.query(Version).filter(Version.secret_id == _secret.id).count() + 1
    version = Version(**data.model_dump(), secret_id=_secret.id, num=num)
    db.session.add(version)
    db.session.flush()

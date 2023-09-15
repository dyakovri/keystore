import hashlib

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from api import config
from api.models.db import SecretKey
from api.utils.random_string import random_string

from .models.security import Seal


security = APIRouter(prefix="")


def hash_password(password: str, salt: str = "") -> str:
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str, salt: str = "") -> bool:
    """Проверяет, что хеш пароля совпадает с хешем из БД"""
    return hash_password(password, salt) == hashed_password


@security.post("/install", response_model=Seal)
async def install(_=Depends(UnionAuth(scopes=["keystore.installation"]))):
    if db.session.query(SecretKey).filter(SecretKey.id == 1).one_or_none():
        raise HTTPException(status_code=403, detail="Secret key already exists")
    with config.token.get_lock():
        secret = random_string()
        config.token.value = bytes(secret, encoding="utf-8")
    _secret = SecretKey(id=1, secret=hash_password(secret))
    db.session.add(_secret)
    db.session.flush()
    return Seal(token=config.token.value)


@security.post("/seal", response_model=Seal)
async def seal(_token: Seal, _=Depends(UnionAuth(scopes=["keystore.installation"]))):
    hashed = db.session.query(SecretKey).filter(SecretKey.id == 1).one_or_none()
    if not hashed:
        raise HTTPException(status_code=400, detail="System hasn't initialized")
    if not validate_password(_token.token, hashed.secret):
        raise HTTPException(status_code=403, detail="Incorrect token")
    with config.token.get_lock():
        config.token.value = b"/"
    return Seal(token=_token.token)


@security.post("/unseal", response_model=Seal)
async def unseal(_token: Seal, _=Depends(UnionAuth(scopes=["keystore.installation"]))):
    hashed = db.session.query(SecretKey).filter(SecretKey.id == 1).one_or_none()
    if not hashed:
        raise HTTPException(status_code=400, detail="System hasn't initialized")
    if not validate_password(_token.token, hashed.secret):
        raise HTTPException(status_code=403, detail="Incorrect token")
    with config.token.get_lock():
        config.token.value = bytes(_token.token, encoding="utf-8")
    return Seal(token=_token.token)

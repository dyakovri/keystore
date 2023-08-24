from fastapi import APIRouter, Depends, HTTPException
from .models.security import Seal
from auth_lib.fastapi import UnionAuth
from api.utils.random_string import random_string
import hashlib
from fastapi_sqlalchemy import db
from api.models.db import SecretKey
from api import config

security = APIRouter(prefix="")


def hash_password(password: str, salt: str = "") -> str:
        enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
        return enc.hex()


def validate_password(password: str, hashed_password: str, salt: str = "") -> bool:
        """Проверяет, что хеш пароля совпадает с хешем из БД"""
        return hash_password(password, salt) == hashed_password


@security.post("/install", response_model=Seal)
async def install(_ = Depends(UnionAuth(scopes=["keystore.installation"]))):
    if db.session.query(SecretKey).filter(SecretKey.id == 1).one_or_none():
         raise HTTPException(status_code=403, detail="Secret key already exists")
    with config.token.get_lock():
        config.token.value = random_string()
    _secret = SecretKey(id=1, secret=hash_password(config.token.value))
    db.session.add(_secret)
    db.session.flush()
    return Seal(token=config.token.value)


@security.post("/seal", response_model=Seal)
async def seal(_token: Seal, _ = Depends(UnionAuth(scopes=["keystore.installation"]))):
    hashed = db.session.query(SecretKey).filter(SecretKey.id == 1).one_or_none()
    if not hashed:
         raise HTTPException(status_code=400, detail="System hasn't initialized")
    if not validate_password(_token.token, hashed.secret):
         raise HTTPException(status_code=403, detail="Incorrect token")
    with config.token.get_lock():
        config.token.value = ""
    return Seal(token=_token)


@security.post("/unseal", response_model=Seal)
async def unseal(_token: Seal,  _ = Depends(UnionAuth(scopes=["keystore.installation"]))):
    hashed = db.session.query(SecretKey).filter(SecretKey.id == 1).one_or_none()
    if not hashed:
        raise HTTPException(status_code=400, detail="System hasn't initialized")
    if not validate_password(_token.token, hashed.secret):
        raise HTTPException(status_code=403, detail="Incorrect token")
    with config.token.get_lock():
        config.token.value = _token.token
    return Seal(token=_token)

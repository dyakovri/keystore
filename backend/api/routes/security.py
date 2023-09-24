import hashlib
import importlib
import multiprocessing
import os

from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from api.config import change_token, get_token, init_token, seal_token
from api.models.db import SecretKey
from api.utils.cipher import hash_password, validate_password
from api.utils.random_string import random_string
from api.utils.security import token_security

from .models.security import Seal


security = APIRouter(prefix="")


@security.post("/install", response_model=Seal)
async def install(_=Depends(UnionAuth(scopes=["keystore.installation"]))):
    if db.session.query(SecretKey).filter(SecretKey.id == 1).one_or_none():
        raise HTTPException(status_code=403, detail="Secret key already exists")
    secret = init_token()
    _secret = SecretKey(id=1, secret=hash_password(secret))
    db.session.add(_secret)
    db.session.flush()
    return Seal(token=secret)


@security.post("/seal", response_model=Seal)
async def seal(_token: Seal, _=Depends(UnionAuth(scopes=["keystore.installation"]))):
    hashed = db.session.query(SecretKey).filter(SecretKey.id == 1).one_or_none()
    if not hashed:
        raise HTTPException(status_code=400, detail="System hasn't initialized")
    if not validate_password(_token.token, hashed.secret):
        raise HTTPException(status_code=403, detail="Incorrect token")
    seal_token()
    return Seal(token=_token.token)


@security.post("/unseal", response_model=Seal)
async def unseal(_token: Seal, _=Depends(UnionAuth(scopes=["keystore.installation"]))):
    hashed = db.session.query(SecretKey).filter(SecretKey.id == 1).one_or_none()
    if not hashed:
        raise HTTPException(status_code=400, detail="System hasn't initialized")
    if not validate_password(_token.token, hashed.secret):
        raise HTTPException(status_code=403, detail="Incorrect token")
    change_token(_token.token)
    return Seal(token=_token.token)

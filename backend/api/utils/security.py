import importlib

from fastapi.exceptions import HTTPException

from api.config import get_token


def token_security():
    if get_token() == b'':
        raise HTTPException(status_code=403, detail="Instance locked")

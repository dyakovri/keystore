import importlib

from api import config
from fastapi.exceptions import HTTPException


def token_security():
    importlib.reload(config)
    if config.token.value == b"/":
        raise HTTPException(status_code=403, detail="Instance locked")

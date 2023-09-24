import base64

from sqlalchemy.orm import Session

from api.models.db import Secret, SecretOwners

from .cipher import AESCipher
from .random_string import random_string


def decrypt_secret(cipher: AESCipher, item: dict[str, str]) -> dict[str, str]:
    value: str = cipher.decrypt(base64.b64decode(item["value"]), bytes(item["salt"], encoding="utf-8"))
    value = value.removesuffix(bytes(item["salt"], encoding="utf-8"))
    try:
        value = value.decode("utf-8")
    except:
        raise Exception(value)
    return {"key": item["key"], "value": value}


def encrypt_secret(cipher: AESCipher, item: dict[str, str]) -> dict[str, str]:
    salt = random_string()
    value = cipher.encrypt(bytes(item.value, "utf-8"), bytes(salt, "utf-8"))
    value = base64.b64encode(value).decode("utf-8")
    return {"key": item.key, "value": value, "salt": salt}


def get_secret_owner_by_secret_name(session: Session, name: str, user_id: int) -> SecretOwners | None:
    return (
        session.query(SecretOwners)
        .join(Secret)
        .filter(Secret.name == name, SecretOwners.owner_id == user_id)
        .one_or_none()
    )


def get_secret_owner_by_secret_id(session: Session, secret_id: str, user_id: int) -> SecretOwners:
    return (
        session.query(SecretOwners)
        .filter(SecretOwners.secret_id == secret_id, SecretOwners.owner_id == user_id)
        .one_or_none()
    )

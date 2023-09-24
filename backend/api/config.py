"""
Файл с зашаренной переменной между инстансами гуникорна

Если переменная равна b"/" то считатется, что она не задана
"""

from ctypes import c_char_p
from multiprocessing import Value
from multiprocessing.managers import BaseManager

from .utils.random_string import random_string


token = b''
data = {}


def init_token():
    global token
    secret = random_string()
    token = bytes(secret, encoding="utf-8")
    return secret


def change_token(val: str):
    global token
    token = bytes(val, encoding="utf-8")
    return token


def seal_token():
    global token
    token = "/"
    return token


def get_token():
    return token

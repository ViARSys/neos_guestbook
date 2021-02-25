from os import environ
from typing import Dict
from utils import hash_password


class CONFIG:
    PORT = int(environ.get("PORT", "8080"))
    BASEURL = ""
    DATABASE = "data.db"
    APP_SALT = "CHANGE THIS FOR PROD"
    USERS: Dict[str, str] = {
        "username": hash_password(APP_SALT, "some password"),
        # etc
        # you can specify a static hash here instead of typing a password in
    }

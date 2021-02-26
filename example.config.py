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

    SPREADSHEET = "1gxm0xk7OHL5Sj9bsQSUEek_38Y-XIK-OX_MYTrg1Y0E"

    GOOGLE_AUTH_OBJECT = {
        "type": "service_account",
        # etc
    }

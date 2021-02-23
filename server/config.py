from os import environ


class CONFIG:
    PORT = int(environ.get("PORT", "8080"))
    BASEURL = ""
    DATABASE = "data.db"
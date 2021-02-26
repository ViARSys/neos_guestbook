from os import environ


class CONFIG:
    PORT = int(environ.get("PORT", "8080"))
    BASEURL = ""

    SPREADSHEET = "1gxm0xk7OHL5Sj9bsQSUEek_38Y-XIK-OX_MYTrg1Y0E"
    GOOGLE_AUTH_OBJECT = {
        "type": "service_account",
        # etc
    }

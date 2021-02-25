from typing import Iterable
from models import Message
from urllib import parse

from sanic import Sanic

from sanic.request import Request
from sanic.response import json, text
from sanic_httpauth import HTTPBasicAuth


import database as db
import utils

from config import CONFIG

app = Sanic(name="neos_guestbook")
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username: str, password: str):
    return username in CONFIG.USERS and CONFIG.USERS.get(username) == utils.hash_password(CONFIG.APP_SALT, password)


def format_for_notes(data: Iterable[Iterable]) -> str:
    f = ""
    for i in data:
        f += ",".join([parse.quote(str(j)) for j in i])
        f += ",\r\n"
    return f


@app.route(f"{CONFIG.BASEURL}/new", methods=["POST"])
async def new(request: Request):
    if not await utils.validate_username(request.json["user"]):
        return text("BAD", status=400)
    message = Message.from_new(request.json)
    await db.saveMessage(message)
    return text("OK")


@app.route(f"{CONFIG.BASEURL}/json/messages")
async def json_get_messages(request: Request):
    notes = await db.getMessagesByWorld(request.args["world"][0])
    return json([note.as_dict for note in notes])


@app.route(f"{CONFIG.BASEURL}/neos/messages")
async def neos_get_messages(request: Request):
    notes = await db.getMessagesByWorld(request.args["world"][0])
    notes = [(note.user, note.message) for note in notes]
    return text(format_for_notes(notes))


@app.route(f"{CONFIG.BASEURL}/worlds")
async def json_get_all_worlds(request: Request):
    worlds = await db.getListOfWorlds()
    return json(worlds)


@app.route(f"{CONFIG.BASEURL}/json/message/<mid:int>", methods=["DELETE"])
@auth.login_required
async def delete_message(request: Request, mid: int):
    await db.deleteMessage(mid)
    return text("OK")


@app.listener("after_server_start")
async def startup(app, loop):
    await db.setup()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG.PORT)

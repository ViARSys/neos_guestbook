from typing import Iterable
from models import Message
from urllib import parse

from sanic import Sanic

from sanic.request import Request
from sanic.response import json, text

import database as db

from config import CONFIG

app = Sanic(name="neos_guestbook")


def format_for_notes(data: Iterable[Iterable]) -> str:
    f = ""
    for i in data:
        f += ",".join([parse.quote(str(j)) for j in i])
        f += ",\r\n"
    return f


@app.route(f"{CONFIG.BASEURL}/new", methods=["POST"])
async def new(request: Request):
    message = Message.from_new(request.json)
    await db.saveMessage(message)
    return text("OK")


@app.route(f"{CONFIG.BASEURL}/neos/messages/")
async def getMessages(request: Request):
    notes = await db.getMessagesByWorld(request.args["world"][0])
    notes = [(note.user, note.message) for note in notes]
    return text(format_for_notes(notes))


@app.listener("after_server_start")
async def startup(app, loop):
    await db.setup()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG.PORT)

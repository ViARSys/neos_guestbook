from models import Message

from sanic import Sanic

from sanic.request import Request
from sanic.response import json, text


from database.GoogleSheets import GoogleSpreadsheet
import utils

from config import CONFIG

app = Sanic(name="neos_guestbook")
db = GoogleSpreadsheet()


@app.route(f"{CONFIG.BASEURL}/new", methods=["POST"])
async def new(request: Request):
    if not await utils.validate_username(request.json["user"]):
        return text("BAD", status=400)
    message = Message.from_new(request.json)
    await db.saveMessage(message)
    return text("OK")


@app.route(f"{CONFIG.BASEURL}/neos/messages")
async def neos_get_messages(request: Request):
    notes = await db.getMessagesByWorld(request.args["world"][0])
    notes = [(note.user, note.message) for note in notes]
    return text(utils.format_for_notes(notes))


@app.route(f"{CONFIG.BASEURL}/worlds")
async def json_get_all_worlds(request: Request):
    worlds = await db.getListOfWorlds()
    return json(worlds)


@app.listener("after_server_start")
async def startup(sanic_app, loop):
    await db.setup()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG.PORT)

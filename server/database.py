from typing import List
from config import CONFIG
import aiosqlite
from models import Message


session: aiosqlite.Connection = None


async def saveMessage(message: Message) -> None:
    await session.execute(
        "INSERT INTO messages (timestamp, world, message, user) VALUES (?, ?, ?, ?)", message.as_tuple
    )
    await session.commit()


async def getMessagesByWorld(world: str) -> List[Message]:
    res = await session.execute("SELECT timestamp, world, message, user from messages WHERE world=?", (world,))
    return [Message.from_row(data) for data in await res.fetchall()]


async def getListOfWorlds() -> List[str]:
    res = await session.execute("SELECT DISTINCT world from messages")
    return [each[0] for each in await res.fetchall()]


async def setup():
    global session
    session = await aiosqlite.connect(CONFIG.DATABASE)
    await session.executescript(open("schema.sql").read())

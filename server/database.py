from typing import List, Tuple
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


async def getListOfWorlds() -> List[Tuple[str, int]]:
    res = await session.execute("SELECT world,count(*) FROM messages WHERE world is not null GROUP BY world")
    return [(each[0], each[1]) for each in await res.fetchall()]


async def deleteMessage(timestamp: int):
    await session.execute("DELETE FROM messages WHERE timestamp=?", (timestamp,))
    await session.commit()


async def setup():
    global session
    session = await aiosqlite.connect(CONFIG.DATABASE)
    await session.executescript(open("schema.sql").read())

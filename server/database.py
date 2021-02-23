from typing import List
from config import CONFIG
import aiosqlite
from models import Message


async def saveMessage(message: Message) -> None:
    async with aiosqlite.connect(CONFIG.DATABASE) as session:
        await session.execute(
            "INSERT INTO messages (timestamp, world, message, user) VALUES (?, ?, ?, ?)", message.as_tuple
        )
        await session.commit()


async def getMessagesByWorld(world: str) -> List[Message]:
    async with aiosqlite.connect(CONFIG.DATABASE) as session:
        res = await session.execute("SELECT timestamp, world, message, user from messages WHERE world=?", (world,))

        return [Message.from_row(data) for data in await res.fetchall()]


async def setup():
    async with aiosqlite.connect(CONFIG.DATABASE) as session:
        await session.executescript(open("schema.sql").read())

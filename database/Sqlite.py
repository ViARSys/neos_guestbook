from database import AbstractDatabase
from typing import List
import aiosqlite
from collections import Counter
from typing import Counter as _Counter

from config import CONFIG
from models import Message


class SqliteDatabase(AbstractDatabase):
    session: aiosqlite.Connection = None

    async def saveMessage(self, message: Message) -> None:
        await self.session.execute(
            "INSERT INTO messages (timestamp, world, message, user) VALUES (?, ?, ?, ?)", message.as_tuple
        )
        await self.session.commit()

    async def getMessagesByWorld(self, world: str) -> List[Message]:
        res = await self.session.execute(
            "SELECT timestamp, world, user, message from messages WHERE world=? ORDER BY timestamp DESC", (world,)
        )
        return [Message.from_row(data) for data in await res.fetchall()]

    async def getListOfWorlds(self) -> _Counter[str]:
        res = await self.session.execute("SELECT world,count(*) FROM messages WHERE world is not null GROUP BY world")
        return Counter(
            {each[0]: each[1] for each in await res.fetchall()},
        )

    async def deleteMessage(self, timestamp: int):
        await self.session.execute("DELETE FROM messages WHERE timestamp=?", (timestamp,))
        await self.session.commit()

    async def setup(self):
        self.session = await aiosqlite.connect(CONFIG.DATABASE)
        await self.session.executescript(open("schema.sql").read())

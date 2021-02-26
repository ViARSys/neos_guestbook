from typing import List
from aiogoogle.resource import GoogleAPI
import aiosqlite
from collections import Counter
from typing import Counter as _Counter
from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from config import CONFIG
from models import Message


class AbstractDatabase:
    async def saveMessage(self, message: Message) -> None:
        raise NotImplementedError

    async def getMessagesByWorld(self, world: str) -> List[Message]:
        raise NotImplementedError

    async def getListOfWorlds(self) -> _Counter[str]:
        raise NotImplementedError

    async def deleteMessage(self, timestamp: int):
        raise NotImplementedError

    async def setup():
        raise NotImplementedError


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


class GoogleSpreadsheet(AbstractDatabase):
    aiogoogle: Aiogoogle = None
    sheets: GoogleAPI = None

    creds = ServiceAccountCreds(scopes=["https://www.googleapis.com/auth/spreadsheets"], **CONFIG.GOOGLE_AUTH_OBJECT)

    async def saveMessage(self, message: Message) -> None:
        await self.aiogoogle.as_service_account(
            self.sheets.spreadsheets.values.append(
                json=dict(
                    range="A:D",
                    values=[[message.timestamp.timestamp(), message.world, message.user, message.message]],
                ),
                spreadsheetId=CONFIG.SPREADSHEET,
                range="A:D",
                valueInputOption="RAW",
            )
        )

    async def getListOfWorlds(self) -> _Counter[str]:
        res = await self.aiogoogle.as_service_account(
            self.sheets.spreadsheets.values.get(spreadsheetId=CONFIG.SPREADSHEET, range="B:B")
        )
        worlds = Counter([v[0] for v in res["values"]])
        return worlds

    async def getMessagesByWorld(self, world: str) -> List[Message]:
        res = await self.aiogoogle.as_service_account(
            self.sheets.spreadsheets.values.get(spreadsheetId=CONFIG.SPREADSHEET, range="A:D")
        )
        rows = res["values"]
        data = [Message.from_row(row) for row in rows if row[1] == world]
        data.sort(key=lambda msg: msg.timestamp.timestamp())
        return data

    async def deleteMessage(self, timestamp: int):
        raise NotImplementedError("cannot delete row from google sheets backend")

    async def setup(self):
        self.aiogoogle = Aiogoogle(service_account_creds=self.creds)
        self.sheets = await self.aiogoogle.discover("sheets", "v4")

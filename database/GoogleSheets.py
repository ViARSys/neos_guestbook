from database import AbstractDatabase
from typing import List
from aiogoogle.resource import GoogleAPI

from collections import Counter
from typing import Counter as _Counter
from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from config import CONFIG
from models import Message


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

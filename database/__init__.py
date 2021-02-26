from typing import List
from typing import Counter as _Counter

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

import aiohttp
from typing import Iterable
from urllib import parse


async def validate_username(username: str) -> bool:
    async with aiohttp.ClientSession() as session:
        res = await session.get(f"https://www.neosvr-api.com/api/users/{username}")
        return res.ok


def format_for_notes(data: Iterable[Iterable]) -> str:
    ret = ""
    for i in data:
        ret += ",".join([parse.quote(str(j)) for j in i])
        ret += ",\r\n"
    return ret

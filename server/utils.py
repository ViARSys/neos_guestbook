import aiohttp
import hashlib


async def validate_username(username: str) -> bool:
    async with aiohttp.ClientSession() as session:
        res = await session.get(f"https://www.neosvr-api.com/api/users/{username}")
        return res.ok


def hash_password(salt, password):
    salted = password + salt
    return hashlib.sha512(salted.encode("utf8")).hexdigest()
import aiohttp


async def validate_username(username: str) -> bool:
    async with aiohttp.ClientSession() as session:
        res = await session.get(f"https://neosvr-api.com/api/users/{username}")
        return res.ok()

import aiohttp
import asyncio

from pprint import pprint


async def get_data():

    async with aiohttp.ClientSession().get(
        "http://127.0.0.1:8000/api/v1/persons/search?query=Star"
    ) as response:
        body = await response.json()
    pprint(body)


asyncio.run(get_data())

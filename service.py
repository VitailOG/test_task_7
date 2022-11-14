import asyncio
from typing import Any

import httpx
import bson

from bs4 import BeautifulSoup, Tag
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from config import settings
from db import TotalAdvertisement


URL = 'https://www.olx.ua/d/uk/aleksandrovka_665/q-%D1%82%D0%B5%D0%BB%' \
      'D0%B5%D1%84%D0%BE%D0%BD/?search%5Border%5D=filter_float_price:desc'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}


async def fetch(
        client: httpx.AsyncClient,
        client_mongo: AsyncIOMotorCollection,
        _id: bson.objectid.ObjectId
) -> None:
    resp = await client.get(URL)
    soup = BeautifulSoup(resp.content, 'html.parser')
    total = soup.find('h3', class_='css-pqvw3x-Text eu5v0x0').next_element.text
    title = soup.find_all('h6', class_='css-1pvd0aj-Text eu5v0x0')
    await client_mongo.update_one({'_id': _id}, {'$push': {"data": validate_date(int(total.split()[2]), title[:5])}})


def validate_date(total: int, top_advertisement: Tag) -> dict[str, Any]:
    """new"""
    data = TotalAdvertisement(
        total=total,
        top_advertisement=[element.text for element in top_advertisement]
    )
    return data.dict()


async def start() -> None:
    client_mongo = AsyncIOMotorClient(settings.MONGO_URI)
    statistic = client_mongo.beanie_db.statistic
    async with httpx.AsyncClient(headers=HEADERS) as client:
        await asyncio.gather(
            *[fetch(client, statistic, _['_id']) async for _ in statistic.find({})]
        )


async def main() -> None:
    while True:
        await start()
        await asyncio.sleep(3)


asyncio.run(main())

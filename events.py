from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from db import Statistic
from config import settings


async def main():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(client.beanie_db, document_models=[Statistic])

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core import settings
from typing import Optional

client: Optional[AsyncIOMotorClient] = None
database: Optional[AsyncIOMotorDatabase] = None


async def connect_to_mongo():
    global client, database

    client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        maxPoolSize=10,
        minPoolSize=1,
        serverSelectionTimeoutMS=5000,
    )
    database = client[settings.MONGODB_DB_NAME]


async def close_mongo_connection():
    global client

    if client:
        client.close()


def get_database() -> AsyncIOMotorDatabase:
    if database is None:
        raise RuntimeError("MongoDB not initialized.")

    return database
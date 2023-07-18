from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)

from app.config import Settings

settings = Settings()
database_url = settings.DATABASE_URL


class DatabaseConnectionHandler:
    def __init__(self, collection_name: str, connection_string: str = database_url):
        self._collection_name = collection_name
        self._connection_string = connection_string
        self.client = self._create_client()
        self.db: AsyncIOMotorDatabase = self.client.get_database()
        self.collection: AsyncIOMotorCollection = self.db[collection_name]

    def _create_client(self):
        return AsyncIOMotorClient(self._connection_string)

    async def __aenter__(self):
        self.db = self.client.get_database()
        self.collection = self.db[self._collection_name]
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

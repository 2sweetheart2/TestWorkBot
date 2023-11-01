import motor.motor_asyncio
import asyncio


class AsyncMongoDB:
    def __init__(self, db_url, db_name):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
        self.db = self.client[db_name]

    async def insert_data(self, collection_name, data):
        collection = self.db[collection_name]
        result = await collection.insert_one(data)
        return result.inserted_id

    async def find_data(self, collection_name, query):
        collection = self.db[collection_name]
        cursor = collection.find(query)
        results = []
        async for document in cursor:
            results.append(document)
        return results

    async def find_one_data(self, collection_name, query):
        collection = self.db[collection_name]
        document = await collection.find_one(query)
        return document

    async def close(self):
        self.client.close()

    async def find(self, collection_name):
        collection = self.db[collection_name]
        cursor = collection.find()
        results = []
        async for document in cursor:
            results.append(document)
        return results

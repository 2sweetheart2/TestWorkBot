import asyncio


from db_files.db import AsyncMongoDB


async def main():
    db = AsyncMongoDB("mongodb://swht.su:27017", "mydatabase")

    documents = await db.find("work")
    for document in documents:
        print(document)

    await db.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

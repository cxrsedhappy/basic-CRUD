import asyncio
import psutil
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

DATABASE_URL = 'sqlite+aiosqlite:///test.db'
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_sessions_with_context_manager():
    async with AsyncSessionLocal() as session:
        await session.execute(text("SELECT 1"))


async def create_sessions_without_context_manager():
    session = AsyncSessionLocal()
    try:
        await session.execute(text("SELECT 1"))
    finally:
        await session.close()


def memory_usage():
    process = psutil.Process()
    return process.memory_info().rss


async def main():
    start_mem = memory_usage()
    tasks = [create_sessions_without_context_manager() for _ in range(1000)]
    await asyncio.gather(*tasks)
    end_mem = memory_usage()
    print(f"No ContextManager: {end_mem - start_mem} bytes")

    # UNCOMMENT THIS AND COMMENT ABOVE
    # start_mem = memory_usage()
    # tasks = [create_sessions_with_context_manager() for _ in range(1000)]
    # await asyncio.gather(*tasks)
    # end_mem = memory_usage()
    # print(f"ContextManager: {end_mem - start_mem} bytes")

    # Memory usage is the same
    # Context manager is just syntaxes sugar
    # Each method uses the same amount of space
    # Tested with 600 entities
    # No ContextManager: 14106624 bytes
    # ContextManager: 13176832 bytes


if __name__ == "__main__":
    asyncio.run(main())

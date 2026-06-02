import asyncpg
from config import settings

async def connect_to_db():
    return await asyncpg.create_pool(
        dsn=settings.database_url_for_raw_sql,
        min_size=5,
        max_size=20,
        command_timeout = 60
    )
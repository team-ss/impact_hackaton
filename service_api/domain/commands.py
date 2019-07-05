from typing import Optional

import asyncpg
import asyncpgsa
from sqlalchemy.schema import CreateTable

from constans import DEFAULT_DB_NAME
from service_api.domain.models import models


async def create_db(host: str, port: int, user: str, password: Optional[str] = None,
                    name: str = DEFAULT_DB_NAME) -> str:
    conn = await asyncpg.connect(host=host, port=port, user=user, password=password, database='postgres')
    q = f"CREATE DATABASE {name}"
    await conn.fetchrow(q)
    await conn.close()
    return f'postgresql://{user}:{password}@{host}:{port}/{name}'


async def drop_db(host: str, port: int, user: str, password: Optional[str] = None,
                  name: str = DEFAULT_DB_NAME):
    conn = await asyncpg.connect(host=host, port=port, user=user, password=password, database='postgres')
    q = f"DROP DATABASE {name}"
    try:
        await conn.fetchrow(q)
    except Exception:
        pass
    finally:
        await conn.close()


async def init_db(db_uri: str) -> None:
    pool = await asyncpgsa.create_pool(db_uri)
    async with pool.acquire() as conn:
        for table in models:
            q = CreateTable(table)
            await conn.execute(q)

import json
import os
from typing import Optional

import asyncpg
import asyncpgsa
from sqlalchemy.schema import CreateTable, DropTable

from constans import DEFAULT_DB_NAME, POLLUTION_DATA_FILENAME
from service_api.domain.models import models


async def create_db(host: str, port: int, user: str, password: Optional[str] = None,
                    name: str = DEFAULT_DB_NAME) -> str:
    conn = await asyncpg.connect(host=host, port=port, user=user, password=password, database='postgres')
    q = f"CREATE DATABASE {name}"
    db_uri = f'postgresql://{user}:{password}@{host}:{port}/{name}'
    await conn.fetchrow(q)
    await conn.close()
    return db_uri


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


async def drop_tables(db_uri: str) -> None:
    pool = await asyncpgsa.create_pool(db_uri)
    async with pool.acquire() as conn:
        for table in models:
            q = DropTable(table)
            await conn.execute(q)


async def init_db(db_uri: str) -> None:
    pool = await asyncpgsa.create_pool(db_uri)
    async with pool.acquire() as conn:
        for table in models:
            q = CreateTable(table)
            await conn.execute(q)
        await load_data(conn, POLLUTION_DATA_FILENAME)


async def load_data(conn, filename):
    data = dict_from_json_file(filename) or {}
    sample_data = data.get('data', {})
    for table in models:
        records = sample_data[0].get(table.name, list())
        for record in records:
            await conn.execute(table.insert().values(**record))


def dict_from_json_file(filename):
    file_name = os.path.join(os.path.join(os.path.dirname(__file__), 'files'), filename)

    def _model_convert(dct):
        for key, value in dct.items():
            if key in ['Model', 'Description']:
                dct[key] = str(value)
        return dct

    with open(file_name) as fin:
        return json.load(fin, object_hook=_model_convert)

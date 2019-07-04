import pandas as pd

from constans import FILES_DIR
from service_api.services import RedisCacheManager


class DataFrameCacheLoader(RedisCacheManager):
    """
    If you want to get pandas DF:

    from service_api.domain.data_frames import DataFrameCacheLoader
    data = await DataFrameCacheLoader().get_auto_df()

    """

    @classmethod
    async def get_auto_df(cls):
        return pd.read_msgpack(await cls.conn.get("auto_pollution_df"))

    @classmethod
    async def get_train_df(cls):
        pass

    @classmethod
    async def get_plane_df(cls):
        pass

    @classmethod
    async def load(cls, filename: list, ext='csv'):
        for name in filename:
            df = pd.read_csv(f'{FILES_DIR}/{name}.{ext}', encoding='utf-8')
            await cls.conn.set(f'{name}_df', df.to_msgpack(compress='zlib'))

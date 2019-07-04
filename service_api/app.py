from sanic import Sanic

from constans import DF_FILE_NAMES
from service_api import api
from service_api.config import AppConfig
from service_api.domain.data_frames import DataFrameCacheLoader
from service_api.services import RedisCacheManager

app = Sanic(__name__)
app.config.from_object(AppConfig)

api.load_api(app)


@app.listener('before_server_start')
async def setup_redis(app, loop):
    await RedisCacheManager.get_conn(app.config.REDIS_URL)
    await DataFrameCacheLoader.load(filename=DF_FILE_NAMES)


@app.listener('before_server_stop')
async def close_redis(app, loop):
    await RedisCacheManager.close_conn()

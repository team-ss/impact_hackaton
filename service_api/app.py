from sanic import Sanic
from asyncpgsa import pg

from service_api import api
from service_api.config import AppConfig
from service_api.services import RedisCacheManager

app = Sanic(__name__)
app.config.from_object(AppConfig)

api.load_api(app)


@app.listener('before_server_start')
async def setup_db(app, loop):
    await RedisCacheManager.get_conn(app.config.REDIS_URL)
    await pg.init(app.config.DB_URI)


@app.listener('before_server_stop')
async def close_redis(app, loop):
    await RedisCacheManager.close_conn()

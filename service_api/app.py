from sanic import Sanic

from service_api import api
from service_api.config import AppConfig


app = Sanic(__name__)
app.config.from_object(AppConfig)

api.load_api(app)

from sanic import Blueprint
from sanic import Sanic

from service_api.resources import SmokeResource
from service_api.resources.route_resource import RouteResource


def load_api(app: Sanic):
    api_v1 = Blueprint('v1', strict_slashes=False)

    api_v1.add_route(SmokeResource.as_view(), '/smoke')
    api_v1.add_route(RouteResource.as_view(), '/route')

    app.blueprint(api_v1)

from http import HTTPStatus

from sanic.response import json

from service_api.resources import BaseResource
from service_api.domain.forms import RouteForm


class RouteResource(BaseResource):

    async def post(self, request):
        data, _ = RouteForm().load(request.json)
        return json(data, HTTPStatus.OK)

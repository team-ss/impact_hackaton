from http import HTTPStatus

from sanic.response import json

from service_api.resources import BaseResource
from service_api.domain.forms import DirectionForm


class DirectionResource(BaseResource):

    async def post(self, request):
        data, _ = DirectionForm().load(request.json)
        return json(data, HTTPStatus.OK)

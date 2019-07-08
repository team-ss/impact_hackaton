from http import HTTPStatus

from sanic.response import json

from service_api.resources import BaseResource
from service_api.domain.forms import DirectionForm
from service_api.services.googleapiclient import GoogleAPIClient


class DirectionResource(BaseResource):

    async def post(self, request):
        data, _ = DirectionForm().load(request.json)
        path = GoogleAPIClient.get_direction(origin=data['origin'],
                                             destination=data['destination'])
        return json(path, HTTPStatus.OK)

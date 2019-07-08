import os
from typing import Dict

from service_api.services import BaseRestClient


class GoogleAPIClient(BaseRestClient):
    @classmethod
    async def get_direction(cls, origin: str, destination: str) -> Dict:
        url = 'https://maps.googleapis.com/maps/api/directions/json'
        api_key = os.getenv('API_KEY')
        path = await cls.get(url=url, origin=origin, destination=destination, key=api_key)

        return path

import json
import os
from typing import Dict

from impact_hackaton.service_api.services import BaseRestClient


class GoogleAPIClient(BaseRestClient):
    @classmethod
    def get_direction(cls, origin: str, destination: str) -> Dict:
        url = 'https://maps.googleapis.com/maps/api/directions/json'
        api_key = os.getenv('API_KEY')
        path = cls.get(url=url, origin=origin, destination=destination, key=api_key)

        return json.loads(path)

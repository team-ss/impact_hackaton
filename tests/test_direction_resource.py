import json

from tests import BaseTestCase


class DirectionResourceTest(BaseTestCase):

    def test_direction_resource_success(self):
        body = {
            "start_city": "10.2",
            "end_city": "30.2",
            "date": "2019-02-02"
        }
        _, response = self.app.post('/route', data=json.dumps(body))

        self.assertEqual(200, response.status)

from asynctest import TestCase
from service_api.app import app


class BaseTestCase(TestCase):

    def setUp(self):
        self.app = app.test_client


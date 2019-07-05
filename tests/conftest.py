import os
import sys

import pytest

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))

from service_api.domain.commands import create_db, drop_db, init_db


@pytest.yield_fixture
def app():
    from service_api.app import app
    yield app


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))


@pytest.fixture(autouse=True)
def setup_db(loop):
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', 5432)
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD')
    name = os.getenv('DB_NAME')
    uri = f'postgresql://{host}:{password}@{port}:{user}/{name}'
    loop.run_until_complete(drop_db(host=host, port=port, user=user, password=password, name='test'))
    loop.run_until_complete(init_db(uri))

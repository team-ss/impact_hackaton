import os
import asyncio

from sanic_script import Manager

from service_api.app import app
from service_api.domain.commands import init_db, create_db

manager = Manager(app)


@manager.command
def create_database():
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', 5432)
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    uri = asyncio.run(create_db(host=host, port=port, user=user, password=password))
    asyncio.run(init_db(uri))


@manager.command
def runserver():
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8000)),
        workers=int(os.environ.get('WEB_CONCURRENCY', 1)),
        debug=bool(os.environ.get('DEBUG', '')))


if __name__ == '__main__':
    manager.run()

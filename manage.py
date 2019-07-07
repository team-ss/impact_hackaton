import os
import asyncio

from sanic_script import Manager

from service_api.app import app
from service_api.domain.commands import init_db, create_db, get_db_variables

manager = Manager(app)


@manager.command
def create_database():
    host, port, user, password, _ = get_db_variables()
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

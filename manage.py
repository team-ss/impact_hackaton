import os

from sanic_script import Manager

from service_api.app import app

manager = Manager(app)


@manager.command
def runserver():
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8000)),
        workers=int(os.environ.get('WEB_CONCURRENCY', 1)),
        debug=bool(os.environ.get('DEBUG', '')))


if __name__ == '__main__':
    manager.run()

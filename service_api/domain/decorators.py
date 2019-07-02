import asyncio

from sanic.log import logger


def asyncio_task(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        task = loop.create_task(coro(*args, **kwargs))
        task.add_done_callback(check_exceptions)

    return wrapper


def check_exceptions(task):
    if task.exception:
        logger.error(task.exception)

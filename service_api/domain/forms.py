from http import HTTPStatus

from marshmallow import Schema, fields
from sanic.exceptions import abort
from sanic.log import logger


class BaseForm(Schema):

    def handle_error(self, error, data):
        logger.error(f"exception: {error} for request: {data}")
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, error)


class DirectionForm(BaseForm):
    origin = fields.String(required=True)
    destination = fields.String(required=True)
    # date = fields.Date(required=True)

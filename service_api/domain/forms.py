from http import HTTPStatus

from marshmallow import Schema, fields
from sanic.exceptions import abort
from sanic.log import logger


class CustomFloat(fields.Float):
    default_error_messages = {"invalid": "Not valid, must be float (coordinate)"}


class BaseForm(Schema):

    def handle_error(self, error, data):
        logger.error(f"exception: {error} for request: {data}")
        abort(HTTPStatus.BAD_REQUEST, error)


class DirectionForm(BaseForm):
    start_city = CustomFloat(required=True)
    end_city = CustomFloat(required=True)
    date = fields.Date(required=True)

from typing import Iterable

from api.errors import bp
from flask import jsonify, make_response


class NotAuthorized(Exception):
    def get_json_repr(self):
        return str(self)


@bp.app_errorhandler(NotAuthorized)
def respond_not_authorized(e: NotAuthorized):
    return jsonify({"error": e.get_json_repr()}), 401


class JSONValidationError(Exception):
    def __init__(self, errors: Iterable[Exception]):
        self.exceptions = list(errors)

    def get_json_repr(self):
        return {"errors": [x.message for x in self.exceptions]}


@bp.app_errorhandler(JSONValidationError)
def respond_not_authorized_JSONValidationError(e: JSONValidationError):
    return jsonify(e.get_json_repr()), 400


class IdNotFoundException(Exception):
    def get_json_repr(self):
        return str(self)


@bp.app_errorhandler(IdNotFoundException)
def respond_not_authorized_IdNotFoundException(e: IdNotFoundException):
    return jsonify({"error": e.get_json_repr()}), 400


class InvalidId(Exception):
    def get_json_repr(self):
        return str(self)


@bp.app_errorhandler(InvalidId)
def respond_not_authorized_InvalidId(e: InvalidId):
    return jsonify({"error": e.get_json_repr()}), 400


@bp.app_errorhandler(404)
def not_found_404(error):
    return make_response(jsonify({"error": "Not Found"})), 404


@bp.app_errorhandler(401)
def not_found_401(error):
    return (
        make_response(
            jsonify(
                {
                    "error": "Missing or Malformed authentication. HTTP authorization header should be of the form 'Bearer [JWT]'"
                }
            )
        ),
        401,
    )

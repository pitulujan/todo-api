#!venv/bin/python

import jwt
from api import app, auth, conn, public_key
from api.errors.api_errors import (
    IdNotFoundException,
    JSONValidationError,
    NotAuthorized,
)
from api.json_validators import (
    iterate_properties_deletetask,
    iterate_properties_newtask,
    iterate_properties_updatetask,
)
from flask import abort, g, jsonify, request


@auth.verify_password
def verify_password(username_or_token, password):

    auth_header = request.headers.get("Authorization", None)

    if auth_header is None:
        raise NotAuthorized("Missing Token or username/password")
    token = None

    try:
        auth_type, token = auth_header.strip().split(" ")
    except:  # noqa : E722
        abort(401)
    if auth_type.lower() == "basic":

        user = conn.find_user(username_or_token)
        if user is None or not user.check_password(password):
            raise NotAuthorized("Wrong username or password")
        g.user = user
        return True

    elif auth_type.lower() == "bearer":

        user = verify_auth_token(token)
        if user is None:
            abort(401)
        g.user = user
        return True
    else:
        abort(401)


def verify_auth_token(token):

    try:
        payload = jwt.decode(token, public_key, algorithms=["RS256"])

    except jwt.DecodeError:
        return None
    except jwt.ExpiredSignatureError:
        raise NotAuthorized("Token Expired")
    user = conn.find_user(_id=payload["user_id"])
    return user


@app.route("/todo/api/v1.0/tasks/token", methods=["GET"])
@auth.login_required
def get_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token})


@app.route("/todo/api/v1.0/tasks", methods=["GET"])
@auth.login_required
def get_tasks():
    tasks = conn.find_task()
    return jsonify({"tasks": tasks})


@app.route("/todo/api/v1.0/tasks/<string:task_id>", methods=["GET"])
@auth.login_required
def get_task(task_id):
    tasks = conn.find_task(id_=task_id)
    if len(tasks) == 0:
        raise IdNotFoundException("Id not found")

    return jsonify({"tasks": tasks})


@app.route("/todo/api/v1.0/tasks", methods=["POST"])
@auth.login_required
def create_task():
    if not request.json:
        abort(400)
    request_json = request.get_json(force=True)
    parse_errors = iterate_properties_newtask(request_json)

    if len(parse_errors) > 0:
        raise JSONValidationError(parse_errors)

    new_task = conn.create_task(
        request_json["title"],
        request_json["description"],
        request_json["done"],
    )
    return jsonify({"task": new_task}), 201


@app.route("/todo/api/v1.0/tasks", methods=["PUT"])
@auth.login_required
def update_task():

    request_json = request.get_json(force=True)
    parse_errors = iterate_properties_updatetask(request_json)
    task_to_update = {}

    if len(parse_errors) > 0:
        raise JSONValidationError(parse_errors)
    task = conn.find_task(_id=request_json["_id"])
    if len(task) == 0:
        raise IdNotFoundException("Id not found")
    task = task[0]

    task_to_update["done"] = request_json["done"]
    if request_json.get("title"):
        task_to_update["title"] = task["title"] = request_json["title"]
    if request_json.get("description"):
        task_to_update["description"] = task["description"] = request_json[
            "description"
        ]
    task = conn.update_task(task[0], task_to_update)
    return jsonify({"task": task})


@app.route("/todo/api/v1.0/tasks", methods=["DELETE"])
@auth.login_required
def delete_task():

    request_json = request.get_json(force=True)
    parse_errors = iterate_properties_deletetask(request_json)

    if len(parse_errors) > 0:
        raise JSONValidationError(parse_errors)

    task = conn.find_task(_id=request_json["_id"])
    if len(task) == 0:
        raise IdNotFoundException("Id not found")

    deleted_task = conn.delete_task(task)

    return jsonify({"result": True, "task": deleted_task})

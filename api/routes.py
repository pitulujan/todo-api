#!venv/bin/python
from flask import Flask, jsonify, abort, make_response, g, request
from typing import Any
import jwt
from time import time
from api import app, auth, private_key, public_key, db
from api.models import User, Tasks, get_user, get_user_by_id, get_tasks_list
from api.errors.api_errors import (
    NotAuthorized,
    JSONValidationError,
    IdNotFoundException,
)
from api.json_validators import (
    iterate_properties_updatetask,
    iterate_properties_newtask,
    iterate_properties_deletetask,
)
from flasgger.utils import swag_from


@auth.verify_password
def verify_password(username_or_token, password):

    auth_header = request.headers.get("Authorization", None)

    if auth_header is None:
        abort(401)
    token = None

    try:
        auth_type, token = auth_header.strip().split(" ")
    except:
        abort(401)
    if auth_type.lower() == "basic":

        user = get_user(username_or_token)
        if user is None or not user.check_password(password):
            return False
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
    user = get_user_by_id(_id=payload["user_id"])
    return user


@app.route("/todo/api/v1.0/tasks/token", methods=["GET"])
@auth.login_required
def get_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token})


@app.route("/todo/api/v1.0/tasks", methods=["GET"])
@auth.login_required
def get_tasks():
    tasks = get_tasks()
    return jsonify({"tasks": tasks})


@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods=["GET"])
@auth.login_required
def get_task(task_id):
    query_task = Tasks.query.filter_by(task_id=task_id).first()
    if query_task is None:
        raise IdNotFoundException("Id not found")

    return jsonify({"tasks": query_task.get_rep()})


@app.route("/todo/api/v1.0/tasks", methods=["POST"])
@auth.login_required
def create_task():
    if not request.json:
        abort(400)
    request_json = request.get_json(force=True)
    parse_errors = iterate_properties_newtask(request_json)

    if len(parse_errors) > 0:
        raise JSONValidationError(parse_errors)

    new_task = Tasks(
        title=request_json["title"],
        description=request_json["description"],
        done=request_json["done"],
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"task": new_task.get_rep()}), 201


@app.route("/todo/api/v1.0/tasks", methods=["PUT"])
@auth.login_required
def update_task():

    request_json = request.get_json(force=True)
    parse_errors = iterate_properties_updatetask(request_json)

    if len(parse_errors) > 0:
        raise JSONValidationError(parse_errors)

    task_to_update = Tasks.query.filter_by(task_id=request_json["id"]).first()
    if task_to_update is None:
        raise IdNotFoundException("Id not found")

    task_to_update.done = request_json["done"]
    if request_json.get("title"):
        task_to_update.title = request_json["title"]
    if request_json.get("description"):
        task_to_update.description = request_json["description"]

    db.session.commit()

    return jsonify({"task": task_to_update.get_rep()})


@app.route("/todo/api/v1.0/tasks", methods=["DELETE"])
@auth.login_required
def delete_task():

    request_json = request.get_json(force=True)
    parse_errors = iterate_properties_deletetask(request_json)

    if len(parse_errors) > 0:
        raise JSONValidationError(parse_errors)

    task_to_delete = Tasks.query.filter_by(task_id=request_json["id"]).first()
    if task_to_delete is None:
        raise IdNotFoundException("Id not found")
    task = task_to_delete.get_rep()
    db.session.delete(task_to_delete)
    db.session.commit()
    return jsonify({"result": True, "task": task})

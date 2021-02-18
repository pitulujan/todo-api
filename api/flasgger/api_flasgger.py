from api.flasgger import bp_flasgger
from flask import Flask, jsonify, abort, make_response, g, request
from api import app, auth, private_key, public_key, conn
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
from bson.objectid import ObjectId


@bp_flasgger.route("/todo/api/v0.1/tasks", methods=["GET"])
@auth.login_required
def get_tasks():
    tasks = conn.find_task()
    return jsonify({"tasks": tasks})


@bp_flasgger.route("/todo/api/v0.1/tasks/token", methods=["GET"])
@auth.login_required
def get_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token})


@bp_flasgger.route("/todo/api/v0.1/tasks/<string:task_id>", methods=["GET"])
@auth.login_required
def get_task(task_id):
    tasks = conn.find_task(_id=task_id)
    if len(tasks) == 0:
        raise IdNotFoundException("Id not found")

    return jsonify({"tasks": tasks})


@bp_flasgger.route("/todo/api/v0.1/tasks", methods=["POST"])
@auth.login_required
def create_task():
    if not request.json:
        abort(400)
    request_json = request.get_json(force=True)
    parse_errors = iterate_properties_newtask(request_json)

    if len(parse_errors) > 0:
        raise JSONValidationError(parse_errors)

    new_task = conn.create_task(
        request_json["title"], request_json["description"], request_json["done"]
    )
    return jsonify({"task": new_task}), 201


@bp_flasgger.route("/todo/api/v0.1/tasks", methods=["PUT"])
@auth.login_required
def update_task():

    request_json = request.get_json(force=True)
    parse_errors = iterate_properties_updatetask(request_json)

    if len(parse_errors) > 0:
        raise JSONValidationError(parse_errors)
    task = conn.find_task(_id=request_json["_id"])
    if len(task) == 0:
        raise IdNotFoundException("Id not found")
    task_to_update = {}
    task_to_update["done"] = request_json["done"]
    if request_json.get("title"):
        task_to_update["title"] = request_json["title"]
    if request_json.get("description"):
        task_to_update["description"] = request_json["description"]
    task = conn.update_task(task[0], task_to_update)
    return jsonify({"task": task})


@bp_flasgger.route("/todo/api/v0.1/tasks", methods=["DELETE"])
@auth.login_required
def delete_task():

    request_json = request.get_json(force=True)
    parse_errors = iterate_properties_deletetask(request_json)

    if len(parse_errors) > 0:
        raise JSONValidationError(parse_errors)

    task = conn.find_task(_id=request_json["_id"])
    if len(task) == 0:
        raise IdNotFoundException("Id not found")

    deleted_task = conn.delete_task(task[0])

    return jsonify({"result": True, "task": deleted_task})

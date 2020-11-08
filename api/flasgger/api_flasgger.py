from api.flasgger import bp_flasgger
from flask import Flask, jsonify, abort, make_response, g, request
from typing import Iterable
from flasgger.utils import swag_from
from api import app, auth, private_key, public_key, db
from api.models import User, get_tasks_list
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
    tasks = get_tasks_list()
    return jsonify({"tasks": tasks})


@bp_flasgger.route("/todo/api/v0.1/tasks/token", methods=["GET"])
# @swag_from('yml/login_specs.yml', methods=['GET'])
@auth.login_required
def get_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token})


@bp_flasgger.route("/todo/api/v0.1/tasks/<string:task_id>", methods=["GET"])
# @swag_from("yml/get_task_by_id.yml",methods=['GET'])
@auth.login_required
def get_task(task_id):
    tasks = get_tasks_list(task_id)
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

    new_task = {
        "title": request_json["title"],
        "description": request_json["description"],
        "done": request_json["done"],
    }

    db.tasks_bucket.insert_one(new_task)
    new_task["id"] = str(new_task["_id"])
    new_task.pop("_id", None)

    return jsonify({"task": new_task}), 201


@bp_flasgger.route("/todo/api/v0.1/tasks", methods=["PUT"])
@auth.login_required
def update_task():

    request_json = request.get_json(force=True)
    parse_errors = iterate_properties_updatetask(request_json)

    if len(parse_errors) > 0:
        raise JSONValidationError(parse_errors)
    task = get_tasks_list(request_json["id"])
    if len(task) == 0:
        raise IdNotFoundException("Id not found")
    task = task[0]
    task_to_update = {}
    task_to_update["done"] = task["done"] = request_json["done"]
    if request_json.get("title"):
        task_to_update["title"] = task["title"] = request_json["title"]
    if request_json.get("description"):
        task_to_update["description"] = task["description"] = request_json[
            "description"
        ]

    db.tasks_bucket.update_one(
        {"_id": ObjectId(request_json["id"])}, {"$set": task_to_update}
    )

    return jsonify({"task": task})


@bp_flasgger.route("/todo/api/v0.1/tasks", methods=["DELETE"])
@auth.login_required
def delete_task():

    request_json = request.get_json(force=True)
    parse_errors = iterate_properties_deletetask(request_json)

    if len(parse_errors) > 0:
        raise JSONValidationError(parse_errors)

    task = get_tasks_list(request_json["id"])
    if len(task) == 0:
        raise IdNotFoundException("Id not found")

    db.tasks_bucket.delete_one({"_id": ObjectId(request_json["id"])})

    return jsonify({"result": True, "task": task})

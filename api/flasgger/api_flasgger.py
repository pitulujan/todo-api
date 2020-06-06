from api.flasgger import bp_flasgger
from flask import Flask, jsonify, abort, make_response, g, request
from typing import Iterable
from flasgger.utils import swag_from
from api import app, auth, private_key, public_key, db
from api.models import User, Tasks
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


@bp_flasgger.route("/todo/api/v0.1/tasks", methods=["GET"])
#@swag_from('yml/tasks_specs.yml',methods=['GET'])
@auth.login_required
def get_tasks():
    query_tasks = Tasks.query.all()

    tasks = []

    for task in query_tasks:
        tasks.append(task.get_rep())

    return jsonify({"tasks": tasks})


@bp_flasgger.route("/todo/api/v0.1/tasks/token" ,methods=["GET"])
#@swag_from('yml/login_specs.yml', methods=['GET'])
@auth.login_required
def get_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token})

@bp_flasgger.route("/todo/api/v0.1/tasks/<int:task_id>", methods=["GET"])
#@swag_from("yml/get_task_by_id.yml",methods=['GET'])
@auth.login_required
def get_task(task_id):
    query_task = Tasks.query.filter_by(task_id=task_id).first()
    if query_task is None:
        raise IdNotFoundException("Id not found")

    return jsonify({"tasks": query_task.get_rep()})


@bp_flasgger.route("/todo/api/v0.1/tasks", methods=["POST"])
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


@bp_flasgger.route("/todo/api/v0.1/tasks", methods=["PUT"])
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


@bp_flasgger.route("/todo/api/v0.1/tasks", methods=["DELETE"])
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
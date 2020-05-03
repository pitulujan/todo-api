#!venv/bin/python
from flask import Flask, jsonify, abort, make_response, g, request
from typing import Any
import jwt
from time import time 
from api import app,auth, tasks,users,private_key,public_key
from api.models import User
from api.errors.api_errors import NotAuthorized,JSONValidationError,IdNotFoundException
from api.json_validators import iterate_properties_updatetask, iterate_properties_newtask,iterate_properties_deletetask

@auth.verify_password
def verify_password(username_or_token, password):

    auth_header =  request.headers.get("Authorization", None)

    if auth_header is None:
        abort(401)
    token = None 

    try:
        auth_type,token = auth_header.strip().split(" ")
    except:
        abort(401)
    if auth_type.lower() == "basic":

        user = [
            user
            for user in users
            if user._get_username() == username_or_token
            and user._get_password() == password
        ]
        if not user:
            return False

        g.user = user[0]
        return True
    
    elif auth_type.lower() == "bearer":
        user = verify_auth_token(token)
        if user is None:
            abort(401)
        g.user = user[0]
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

    user = [user for user in users if user._get_id() == payload["user_id"]]
    return user


@app.route("/todo/api/v1.0/tasks/token", methods=["GET"])
@auth.login_required
def get_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token})


@app.route("/todo/api/v1.0/tasks", methods=["GET"])
@auth.login_required
def get_tasks():
    return jsonify({"tasks": tasks})


@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods=["GET"])
@auth.login_required
def get_task(task_id):
    task = [task for task in tasks if task["id"] == task_id]
    if len(task) == 0:
        raise IdNotFoundException("Id not found")
    return jsonify({"task": task[0]})


@app.route("/todo/api/v1.0/tasks", methods=["POST"])
@auth.login_required
def create_task():
    if not request.json:
        abort(400)
    request_json = request.get_json(force=True)
    parse_errors = iterate_properties_newtask(request_json)

    if len(parse_errors) > 0: 
        raise JSONValidationError(parse_errors)
    task = {
        "id": tasks[-1]["id"] + 1,
        "title": request_json["title"],
        "description" : request_json["description"],
        "done": request_json["done"],
    }
    tasks.append(task)
    return jsonify({"task": task}), 201


@app.route('/todo/api/v1.0/tasks', methods=['PUT'])
@auth.login_required
def update_task():

    request_json = request.get_json(force=True)
    parse_errors = iterate_properties_updatetask(request_json)

    if len(parse_errors) > 0: 
        raise JSONValidationError(parse_errors)

    task_to_update = [task for task in tasks if task["id"] == request_json['id']]
    if len(task_to_update) == 0:
        raise IdNotFoundException("Id not found")

    task_to_update[0]["done"] = request_json["done"]
    if request_json.get('title'):
        task_to_update[0]["title"] = request_json["title"]
    if request_json.get('description'):
        task_to_update[0]["description"] = request_json["description"]

    return jsonify({"task": task_to_update[0]})


@app.route('/todo/api/v1.0/tasks', methods=['DELETE'])
@auth.login_required
def delete_task():

    request_json = request.get_json(force=True)
    parse_errors = iterate_properties_deletetask(request_json)

    if len(parse_errors) > 0: 
        raise JSONValidationError(parse_errors)

    task_to_delete = [task for task in tasks if task["id"] == request_json['id']]
    if len(task_to_delete) == 0:
        raise IdNotFoundException("Id not found")
    tasks.remove(task_to_delete[0])
    return jsonify({'result': True, "task" : task_to_delete[0]})



from api.flasgger import bp_flasgger
from flask import make_response, jsonify, g
from typing import Iterable
from flasgger.utils import swag_from
from api import auth
from api.models import User, Tasks


@bp_flasgger.route("/todo/api/v1.0/tasks", methods=["GET"])
# @swag_from('yml/tasks_specs.yml',methods=['GET'])
@auth.login_required
def get_tasks():
    query_tasks = Tasks.query.all()

    tasks = []

    for task in query_tasks:
        tasks.append(task.get_rep())

    return jsonify({"tasks": tasks})


@bp_flasgger.route("/todo/api/v1.0/tasks/token", methods=["GET"])
# @swag_from('yml/login_specs.yml', methods=['GET'])
@auth.login_required
def get_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token})

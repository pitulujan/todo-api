from api import db, private_key
import jwt
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from api.errors.api_errors import InvalidId


class User:
    def __init__(self, username, password, id, admin=False):
        self.username = username
        self.password_hash = password
        self.id = id
        self.admin = admin

    # def set_password(self, password):
    #   self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=600):
        payload = {"user_id": self.id, "exp": time() + expiration}
        return jwt.encode(payload, private_key, algorithm="RS256").decode("utf-8")


def get_user(username):
    user = db.users.find_one({"username": username})
    if user is not None:
        user = User(user["username"], user["password"], str(user["_id"]), user["admin"])

    return user


def get_user_by_id(_id):
    user = db.users.find_one({"_id": ObjectId(_id)})
    if user is not None:
        user = User(user["username"], user["password"], str(user["_id"]), user["admin"])

    return user


def get_tasks_list(_id=None):
    tasks = []
    if _id is not None:
        try:
            tasks_mongo = db.tasks_bucket.find_one({"_id": ObjectId(_id)})
        except:
            raise InvalidId("Not supported Id type")

        if tasks_mongo is not None:
            task = {
                "title": tasks_mongo["title"],
                "description": tasks_mongo["description"],
                "id": str(tasks_mongo["_id"]),
                "done": tasks_mongo["done"],
            }
            tasks.append(task)
    else:

        tasks_mongo = db.tasks_bucket.find({})

        for t in tasks_mongo:
            task = {
                "title": t["title"],
                "description": t["description"],
                "id": str(t["_id"]),
                "done": t["done"],
            }
            tasks.append(task)
    return tasks

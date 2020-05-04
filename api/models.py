from api import db
import jwt
from time import time
from werkzeug.security import generate_password_hash, check_password_hash


private_key = open("jwt-key").read()


class User(db.Model):

    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    id = db.Column(db.Integer, primary_key=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=600):
        payload = {"user_id": self.id, "exp": time() + expiration}
        return jwt.encode(payload, private_key, algorithm="RS256").decode("utf-8")


class Tasks(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128))
    title = db.Column(db.String(128))
    done = db.Column(db.Boolean)

    def get_rep(self):
        return {
            "title": self.title,
            "description": self.description,
            "id": self.task_id,
            "done": self.done,
        }

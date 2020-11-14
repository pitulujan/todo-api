from api import private_key
import jwt
from time import time
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self,_id, username, password,  admin=False):
        self.username = username
        self.password_hash = password
        self.id = _id
        self.admin = admin

    # def set_password(self, password):
    #   self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=600):
        payload = {"user_id": self.id, "exp": time() + expiration}
        return jwt.encode(payload, private_key, algorithm="RS256").decode("utf-8")



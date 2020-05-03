import jwt
from time import time

private_key = open("jwt-key").read()

class User:
    def __init__(self, username: str, password: str, id: int):
        self.username = username
        self.password = password
        self.id = id

    def _get_username(self):
        return self.username

    def _get_password(self):
        return self.password

    def _get_id(self):
        return self.id

    def generate_auth_token(self, expiration=600):
        payload = {"user_id": self.id, "exp": time() + expiration}
        return jwt.encode(payload, private_key, algorithm="RS256").decode("utf-8")
from flask import Flask
from api.models import User
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()


tasks = [
    {
        "id": 1,
        "title": u"Buy Groceries",
        "description": "Milk,Cheese, Pizza,Fruit,Tylenol",
        "done": False,
    },
    {
        "id": 2,
        "title": u"Learn French",
        "description": "Get your ass to work",
        "done": False,
    },
]



pitu = User("pitu", "tuvieja", 1)
julian = User("julian", "tuvieja", 2)
users = [pitu, julian]

private_key = open("jwt-key").read()
public_key = open("jwt-key.pub").read()

from api.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from api import routes


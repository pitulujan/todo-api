from flask import Flask
from flask_httpauth import HTTPBasicAuth
from sql_config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
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


private_key = open("jwt-key").read()
public_key = open("jwt-key.pub").read()

from api.errors import bp as errors_bp

app.register_blueprint(errors_bp)

from api import routes, models

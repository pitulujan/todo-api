from flask import Flask
from flask_httpauth import HTTPBasicAuth
from config import Config
from mongo_conn import get_conn
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
import yaml

data = open("database_data.txt", "r")
data = dict(zip(["username", "password", "db_name"], data.read().split(":")))
app = Flask(__name__)
app.config.from_object(Config)
db = get_conn(data["username"], data["password"], data["db_name"])
auth = HTTPBasicAuth()

private_key = open("jwt-key").read()
public_key = open("jwt-key.pub").read()

from api.errors import bp as errors_bp
from api.flasgger import bp_flasgger as flasgger_bp

app.register_blueprint(errors_bp)
app.register_blueprint(flasgger_bp)

with open("api/flasgger/yml/swagger_config.yml", "r") as conf:
    swag = Swagger(app, template=yaml.safe_load(conf))


from api import routes

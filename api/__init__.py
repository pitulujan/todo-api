from flask import Flask
from flask_httpauth import HTTPBasicAuth
from config import Config
from mongo_conn import get_conn
from flasgger import Swagger
import yaml
from dotenv import load_dotenv
import os
from repos import Repository
from repos.mongo import MongoRepository


load_dotenv(".env")

app = Flask(__name__)
app.config.from_object(Config)
auth = HTTPBasicAuth()

private_key = open("jwt-key").read()
public_key = open("jwt-key.pub").read()

from api.services import Service
db = Service()

from api.errors import bp as errors_bp
from api.flasgger import bp_flasgger as flasgger_bp

app.register_blueprint(errors_bp)
app.register_blueprint(flasgger_bp)

with open("api/flasgger/yml/swagger_config.yml", "r") as conf:
    swag = Swagger(app, template=yaml.safe_load(conf))


from api import routes

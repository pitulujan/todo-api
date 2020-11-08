from flask import Flask
from flask_httpauth import HTTPBasicAuth
from config import Config
from mongo_conn import get_conn
from flasgger import Swagger
import yaml
from dotenv import load_dotenv
import os

load_dotenv(".env")

app = Flask(__name__)
app.config.from_object(Config)
db = get_conn(
    os.environ["MONGO_USER"], os.environ["MONGO_PASS"], os.environ["MONGO_DB"]
)
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

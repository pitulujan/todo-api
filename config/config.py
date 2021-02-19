import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {"title": "Playing Around API", "uiversion": 3, "openapi": "3.0.2"}

from flask import Blueprint

bp_flasgger = Blueprint("flasgger_bp", __name__)

from api.flasgger import api_flasgger

from flask import Blueprint

vehicles_bp = Blueprint("vechicles", __name__)

from . import routes
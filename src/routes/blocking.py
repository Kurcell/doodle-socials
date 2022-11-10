from flask import Blueprint
from ..models.models import Blocking

blocking_bp = Blueprint('blocking', __name__)

@blocking_bp.route("/blocking", methods=['GET'])
def readAll():
    return "Blocking."
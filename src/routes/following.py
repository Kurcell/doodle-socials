from flask import Blueprint
from ..models.models import Following

following_bp = Blueprint('following', __name__)

@following_bp.route("/following", methods=['GET'])
def readAll():
    return "Following."
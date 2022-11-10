from flask import Blueprint, jsonify
from ..models.models import User

user_bp = Blueprint('users', __name__)

@user_bp.route("/users", methods=['GET'])
def getUsers():
    return jsonify(User.query.all())

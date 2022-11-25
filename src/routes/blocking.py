from flask import Blueprint, jsonify, request
from ..models.models import Blocking, User

blocking_bp = Blueprint('blocking', __name__)

@blocking_bp.route("/blocking", methods=['GET'])
def readAll():
    return "Blocking."

@blocking_bp.route("/blocks", methods=['GET'])
def readMany():
    blocks = [
        {
            'uid': i.uid,
            'username': i.username,
            'screenname': i.screenname,
        }
        for i in Blocking.query.join(User, Blocking.blocked_uid == User.uid).add_columns(User.uid, User.screenname, User.username).all()
    ]
    return jsonify(blocks)

@blocking_bp.route("/block", methods=['POST'])
def create():
    req = request.get_json()
    return jsonify(Blocking.create(req.get('user_id')))

@blocking_bp.route("/block/<int:id>", methods=['DELETE'])
def delete(id):
    return jsonify(Blocking.delete(id))
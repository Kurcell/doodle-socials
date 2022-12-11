from flask import Blueprint, jsonify, request
from ..models.models import Follows, User

following_bp = Blueprint('following', __name__)

@following_bp.route("/follows", methods=['GET'])
def readMany():
    follows = [
        {
            'uid': i.uid,
            'username': i.username,
            'screenname': i.screenname,
        }
        for i in Follows.query.join(User, Follows.followee_uid == User.uid).add_columns(User.uid, User.screenname, User.username).all()
    ]
    return jsonify(follows)

@following_bp.route("/follow", methods=['POST'])
def create():
    req = request.get_json()
    return jsonify(Follows.create(req.get('user_id')))

@following_bp.route("/follow/<int:id>", methods=['DELETE'])
def delete(id):
    return jsonify(Follows.delete(id))
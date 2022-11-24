from flask import Blueprint
from ..models.models import Following

following_bp = Blueprint('following', __name__)

@following_bp.route("/following", methods=['GET'])
def readAll():
    return "Following."

@following_bp.route("/follows", methods='[GET]')
def readMany():
    follows = [
        {
            'uid': i.uid,
            'username': i.username,
            'screenname': i.screenname,
        }
        for i in Following.query.join(User, Following.followed_uid == User.uid).add_columns(User.uid, User.screenname, User.username).all()
    ]
    return jsonify(follows)

@following_bp.route("/follow", methods=['POST'])
def create():
    req = request.get_json()
    return jsonify(Following.create(req.get('user_id')))

@following_bp.route("/follow/<int:id>", methods=['DELETE'])
def delete(id):
    return jsonify(Following.delete(id))
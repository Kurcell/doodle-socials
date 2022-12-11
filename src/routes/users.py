from flask import Blueprint, jsonify, request
from ..models.models import User, Follows
from flask_jwt_extended import (jwt_required, current_user)

user_bp = Blueprint('users', __name__)

@user_bp.route("/user/<int:id>", methods=['GET'])
def readOne(id):
    return jsonify(User.query.filter_by(uid = id).one())

@user_bp.route("/users", methods=['GET'])
def readMany():
    return jsonify(User.query.all())

@user_bp.route("/user/follow", methods=['GET'])
@jwt_required()
def follow():
    follower_id = current_user.uid
    followee_id = request.args.get('uid')
    exists = Follows.query.filter_by(follower_id = follower_id, followee_id = followee_id).first()
    if exists is None:
        return jsonify(Follows.create(follower_id, followee_id)), 201
    else:
        return jsonify(Follows.delete(exists.follow_id)), 200

@user_bp.route("/user", methods=['POST'])
def create():
    req = request.get_json()
    return jsonify(User.create(req.get('username'), req.get('screenname'), req.get('profile'), req.get('password'), req.get('email'))), 201

@user_bp.route("/user/<int:id>", methods=['PUT'])
def update(id):
    req = request.get_json()
    return jsonify(User.update(id, req.get('username'), req.get('screenname'), req.get('profile'), req.get('password'), req.get('email')))

@user_bp.route("/user/<int:id>", methods=['DELETE'])
def delete(id):
    return jsonify(User.delete(id))

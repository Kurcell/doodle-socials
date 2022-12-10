from flask import Blueprint, jsonify, request
from ..models.models import User

user_bp = Blueprint('users', __name__)

@user_bp.route("/user/<int:id>", methods=['GET'])
def readOne(id):
    return jsonify(User.query.filter_by(uid = id).one())

@user_bp.route("/users", methods=['GET'])
def readMany():
    return jsonify(User.query.all())

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

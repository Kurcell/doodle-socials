from flask import Blueprint, jsonify, request
from ..models.models import Post, User

post_bp = Blueprint('posts', __name__)

@post_bp.route("/post/<int:id>", methods=['GET'])
def readOne(id):
    return jsonify(Post.query.filter_by(pid = id).one())

@post_bp.route("/posts", methods=['GET'])
def readMany():
    posts = [
        {
            'uid': i.uid,
            'username': i.username,
            'screenname': i.screenname,
            'pid': i.pid,
            'createdat': i.createdat
        }
        for i in Post.query.join(User, Post.user_id == User.uid).add_columns(User.uid, User.screenname, User.username, Post.pid, Post.createdat).all()
    ]
    return jsonify(posts)

@post_bp.route("/post", methods=['POST'])
def create():
    req = request.get_json()
    return jsonify(Post.create(req.get('user_id')))

@post_bp.route("/post/<int:id>", methods=['PUT'])
def update(id):
    req = request.get_json()
    return jsonify(Post.update(id, req.get('user_id')))

@post_bp.route("/post/<int:id>", methods=['DELETE'])
def delete(id):
    return jsonify(Post.delete(id))

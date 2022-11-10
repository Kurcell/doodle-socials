from flask import Blueprint, jsonify, request
from ..models.models import Post, User
from ..__init__ import db

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
    print(posts)
    return jsonify(posts)

@post_bp.route("/post", methods=['POST'])
def create():
    req = request.get_json()

    Post.create(req['user_id'])

    return "Created."

@post_bp.route("/post/<int:id>", methods=['DELETE'])
def delete(id):
    print(Post.delete(id))
    return "Deleted."
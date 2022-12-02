from flask import Blueprint, jsonify, request
from ..models.models import Likes, Post, User
from .. import db

likes_bp = Blueprint('likes', __name__)

@likes_bp.route("/like/<int:id>", methods=['GET'])
def readOne(id):
    return jsonify(Likes.query.filter_by(like_id = id).one())

@likes_bp.route("/likes", methods=['GET'])
def readMany():
    return jsonify(Likes.query.all())

@likes_bp.route("/like/<int:uid>/<int:id>", methods=['PUT'])
def update(uid, id):
    req = request.get_json()
    user = User.query.filter_by(uid = id).one()
    exists = db.session.query.filter_by(user.uid = id).scalar()
    if exists is None:
        post = Post.query.filter_by(id = id).one()
        new_like = Like(user.uid, post.pid)
        db.session.add(new_like)
        db.session.commit()
        return f"Added a like! The post now has {post.likes}!"
    else:
        post = Post.query.filter_by(id = id).one()
        db.session.delete(post)
        db.session.commit()
        return f"Removed your like! The post now has {post.likes}!"
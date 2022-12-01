from flask import Blueprint, jsonify, request
from ..models.models import Post, User
from .. import db

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

@post_bp.route("post/<int:uid>/like/<int:id>", methods=['PUT'])
def update(uid, id):
    req = request.get_json()
    user = User.query.filter_by(uid = id).one()
    exists = db.session.query(user.uid).filter_by(username=user.username).scalar()
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




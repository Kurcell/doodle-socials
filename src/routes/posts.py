from flask import Blueprint, jsonify, request
from ..models.models import Post, User, Likes, Following
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
            'doodle_id': i.doodle_id,
            'likes': i.likes,
            'createdat': i.createdat
        }
        for i in Post.query.join(User, Post.user_id == User.uid).add_columns(User.uid, User.screenname, User.username, Post.pid, Post.doodle_id, Post.likes, Post.createdat).all()
    ]
    return jsonify(posts)

@post_bp.route("/post", methods=['POST'])
def create():
    req = request.get_json()
    return jsonify(Post.create(req.get('user_id'), req.get('doodle_id')))

@post_bp.route("/post/<int:id>", methods=['PUT'])
def update(id):
    req = request.get_json()
    return jsonify(Post.update(id, req.get('user_id'), req.get('doodle_id')))

@post_bp.route("/post/<int:id>", methods=['DELETE'])
def delete(id):
    return jsonify(Post.delete(id))

@post_bp.route("/post/like", methods=['PUT'])
def update_like():
    req = request.get_json()
    uid = req.get('uid')
    pid = req.get('pid')
    exists = Likes.query.filter_by(liking_user = uid, liked_post = pid).first()
    if exists is None:
        post = Post.query.filter_by(pid = pid).one()
        post.likes += 1
        return jsonify(Likes.create(uid, pid))
    else:
        post = Post.query.filter_by(pid = pid).one()
        post.likes -= 1
        if post.likes < 0:
            post.likes = 0
        return jsonify(Likes.delete(exists.like_id))

@post_bp.route("/post/like/check/<int:uid>/<int:id>", methods=['GET'])
def check_if_liked(uid, id):
    like = Likes.query.filter_by(liking_user = uid, liked_post = id).first()
    return "False" if like None else "True"

@post_bp.route("/posts/discover", methods=['GET'])
def discover():
    uid = request.args.get('uid')
    page = request.args.get('page')
    posts = [
        {
            'uid': i.uid,
            'username': i.username,
            'screenname': i.screenname,
            'pid': i.pid,
            'doodle_id': i.doodle_id,
            'likes': i.likes,
            'createdat': i.createdat
        }
        for i in Post.query.join(User, Post.user_id == User.uid).add_columns(User.uid, User.screenname, User.username, Post.pid, Post.doodle_id, Post.likes, Post.createdat).order_by(Post.likes.desc()).offset(page or 0).limit(1).all()
    ]
    return jsonify(posts)

@post_bp.route("/posts/following", methods=['GET'])
def following():
    uid = request.args.get('uid')
    page = request.args.get('page')
    posts = [
        {
            'uid': i.uid,
            'username': i.username,
            'screenname': i.screenname,
            'pid': i.pid,
            'doodle_id': i.doodle_id,
            'likes': i.likes,
            'createdat': i.createdat
        }
        for i in Post.query.join(User, Post.user_id == User.uid).add_columns(User.uid, User.screenname, User.username, Post.pid, Post.doodle_id, Post.likes, Post.createdat).order_by(Post.likes.desc()).offset(page or 0).limit(1).all()
    ]
    return jsonify(posts)







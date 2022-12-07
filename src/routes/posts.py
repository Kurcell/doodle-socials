from flask import Blueprint, jsonify, request
from ..models.models import Post, User, Likes
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

@post_bp.route("/post/like/<int:id>", methods=['PUT'])
def update_like(id):
    req = request.get_json()
    uid = req.get('user_id')
    pid = req.get('pid')
    like_id = req.get('like_id')
    exists = Likes.query.filter_by(like_id = like_id).first() # first instead of one so it can be None, otherwise program fails
    if exists is None:
        print("doesnt exist") 
        post = Post.query.filter_by(pid = id).one()
        # print("found post, creating like")
        post.likes += 1
        return jsonify(Likes.create(req.get('user_id'), req.get('pid')))
    else:
        print("exists") 
        print(exists)
        post = Post.query.filter_by(pid = id).one()
        # print("found post, removing like")
        post.likes -= 1
        if post.likes < 0:
            post.likes = 0
        # print("removed like")
        return jsonify(Likes.delete(exists.like_id))







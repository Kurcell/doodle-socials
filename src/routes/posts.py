from flask import Blueprint, jsonify, request
from ..models.models import Post, User, Likes, Follows
from flask_jwt_extended import (jwt_required, current_user)
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
    return jsonify(Post.create(req.get('user_id'), req.get('doodle_id'))), 201

@post_bp.route("/post/<int:id>", methods=['PUT'])
def update(id):
    req = request.get_json()
    return jsonify(Post.update(id, req.get('user_id'), req.get('doodle_id')))

@post_bp.route("/post/<int:id>", methods=['DELETE'])
def delete(id):
    return jsonify(Post.delete(id))

@post_bp.route("/post/like", methods=['GET'])
@jwt_required()
def post_like():
    uid = current_user.uid or request.args.get('uid')
    pid = request.args.get('pid')
    exists = Likes.query.filter_by(liking_user = uid, liked_post = pid).first()
    if exists is None:
        post = Post.query.filter_by(pid = pid).one()
        post.likes += 1
        return jsonify(Likes.create(uid, pid)), 201
    else:
        post = Post.query.filter_by(pid = pid).one()
        post.likes -= 1
        if post.likes < 0:
            post.likes = 0
        return jsonify(Likes.delete(exists.like_id)), 200

@post_bp.route("/post/like/check/<int:uid>/<int:id>", methods=['GET'])
def check_if_liked(uid, id):
    like = Likes.query.filter_by(liking_user = uid, liked_post = id).first()
    return "False" if like == None else "True"

@post_bp.route("/posts/discover", methods=['GET'])
@jwt_required()
def post_discover():
    uid = current_user.uid or request.args.get('uid')
    page = request.args.get('page')
    posts = [
        {
            'uid': i.uid,
            'username': i.username,
            'screenname': i.screenname,
            'liked': i.liked,
            'pid': i.pid,
            'doodle_id': i.doodle_id,
            'likes': i.likes,
            'createdat': i.createdat
        }
        for i in db.session.execute("""select users.uid, users.username, users.screenname, post.pid, post.doodle_id, post.likes, likes.like_id IS NOT NULL as liked, post.createdat
            from post
            left join likes on post.pid = likes.liked_post and likes.liking_user = :uid
            inner join users on post.user_id = users.uid
            left outer join follows on follows.follower_id = :uid and follows.followee_id = post.user_id
            where follow_id is null and users.uid != :uid
            order by post.likes desc
            limit 1
            offset :page;
        """, {'uid': uid, 'page': page or 0}).all()
        ]

    return jsonify(posts)

@post_bp.route("/posts/following", methods=['GET'])
@jwt_required()
def post_following():
    uid = current_user.uid or request.args.get('uid')
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
        for i in db.session.execute("""select users.uid, users.username, users.screenname, post.pid, post.doodle_id, post.likes, likes.like_id IS NOT NULL as liked, post.createdat
            from post
            left join likes on post.pid = likes.liked_post and likes.liking_user = :uid
            inner join users on post.user_id = users.uid
            inner join follows on follows.followee_id = post.user_id and follows.follower_id = :uid
            order by post.likes desc
            limit 1
            offset :page;
        """, {'uid': uid, 'page': page or 0}).all()
        ]
    return jsonify(posts)

@post_bp.route("/posts/portfolio", methods=['GET'])
@jwt_required()
def post_portfolio():
    uid = current_user.uid
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
        for i in db.session.execute("""select users.uid, users.username, users.screenname, post.pid, post.doodle_id, post.likes, likes.like_id IS NOT NULL as liked, post.createdat
            from post
            left join likes on post.pid = likes.liked_post and likes.liking_user = :uid
            inner join users on post.user_id = users.uid
            where post.user_id = :uid
            order by post.likes desc
            limit 1
            offset :page;
        """, {'uid': uid, 'page': page or 0}).all()
        ]
    return jsonify(posts)







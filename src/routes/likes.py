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

# @likes_bp.route("/like/<int:id>", methods=['PUT'])
# def update(id):
#     req = request.get_json()
#     uid = req.get('user_id')
#     pid = req.get('pid')
#     # user = User.query.filter_by(uid = id).one()
#     exists = Likes.query.filter_by(like_id = id).one()
#     # print(req.get('user_id'))
#     # print(isinstance(req.get('user_id'), str))
#     # print(req.get('pid'))
#     # print(exists)
#     # print(exists.liked_post)
#     if exists is None:
#         print("doesnt exist") 
#         post = Post.query.filter_by(pid = pid).one()
#         post.likes += 1
#         return jsonify(Likes.create(req.get('user_id'), req.get('pid')))
#     else:
#         print("exists") 
#         print(exists)
#         post = Post.query.filter_by(pid = exists.liked_post).one()
#         post.likes -= 1
#         if posts.like < 0:
#             post.likes = 0
#         return jsonify(Likes.delete(id))

from flask import Blueprint
from ..models.models import Post

post_bp = Blueprint('posts', __name__)

@post_bp.route("/posts", methods=['GET'])
def readAll():
    return "Posts."
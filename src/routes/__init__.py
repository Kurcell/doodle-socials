from .auth import auth_bp
from .users import user_bp
from .posts import post_bp
from .following import following_bp
from .likes import likes_bp

def init_app(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(following_bp)
    app.register_blueprint(likes_bp)
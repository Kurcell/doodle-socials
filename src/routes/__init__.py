from .gen import gen_bp
from .users import user_bp
from .posts import post_bp
from .following import following_bp
from .blocking import blocking_bp
# ...

def init_app(app):
    app.register_blueprint(gen_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(following_bp)
    app.register_blueprint(blocking_bp)
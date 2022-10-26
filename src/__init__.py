"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Database setup
db = SQLAlchemy()

def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object('src.config.Config')

    db.init_app(app)

    with app.app_context():
        from src.models.models import User, Post, Canvas, Blocking, Following
        db.create_all()

        return app
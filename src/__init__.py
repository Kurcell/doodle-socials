import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

load_dotenv()

# Database setup
db = SQLAlchemy()

def create_app():
    from . import models, routes

    app = Flask(__name__, instance_relative_config=False)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app_ctx = app.app_context()
    app_ctx.push()
    current_app.config["ENV"]

    models.init_app(app)
    routes.init_app(app)

    # with app.app_context():
    #     from src.models.models import User, Post, Blocking, Following
    #     db.create_all()

    return app

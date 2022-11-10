import os
from flask import Flask, current_app, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

from dotenv import load_dotenv

load_dotenv()

# Database setup
db = SQLAlchemy()


def create_app():
    from . import models, routes

    app = Flask(__name__, instance_relative_config=False)
    CORS(app)

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Just a Doodle API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
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

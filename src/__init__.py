import os
from flask import Flask, current_app, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()

# Database setup
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    CORS(app, supports_credentials=True)

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
    
    app.config['JWT_SECRET_KEY'] = os.getenv('DATABASE_URL')
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config['JWT_CSRF_CHECK_FORM'] = True
    app.config['SECRET_KEY'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app_ctx = app.app_context()
    app_ctx.push()
    current_app.config["ENV"]

    from . import models, routes
    models.init_app(app)
    routes.init_app(app)

    jwt = JWTManager(app) 

    # Register a callback function that takes whatever object is passed in as the
    # identity when creating JWTs and converts it to a JSON serializable format.
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.uid

    # Register a callback function that loads a user from your database whenever
    # a protected route is accessed. This should return any python object on a
    # successful lookup, or None if the lookup failed for any reason (for example
    # if the user has been deleted from the database).
    from .models.models import User
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(uid=identity).first()

    # with app.app_context():
    #     from src.models.models import User, Post, Blocking, Following
    #     db.create_all()

    return app

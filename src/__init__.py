from functools import wraps
import os, jwt
from flask import Flask, current_app, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
# from flask_login import LoginManager

from dotenv import load_dotenv
load_dotenv()

def token_required(func):
    # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
        @wraps(func)
        def decorated(*args, **kwargs):
            token = request.args.get('token')
            if not token:
                return jsonify({'Alert!': 'Token is missing!'}), 401

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
            # You can use the JWT errors in exception
            # except jwt.InvalidTokenError:
            #     return 'Invalid token. Please log in again.'
            except:
                return jsonify({'Message': 'Invalid token'}), 403
            return func(*args, **kwargs)
        return decorated

# Database setup
db = SQLAlchemy()

def create_app():
    from . import models, routes

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
    
    app.config['SECRET_KEY'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app_ctx = app.app_context()
    app_ctx.push()
    current_app.config["ENV"]

    # login_manager = LoginManager()
    # login_manager.init_app(app)

    models.init_app(app)
    routes.init_app(app)

    # from .models.models import User
    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))  

    # with app.app_context():
    #     from src.models.models import User, Post, Blocking, Following
    #     db.create_all()

    return app

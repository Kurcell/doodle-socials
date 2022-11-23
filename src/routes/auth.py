from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from ..models.models import User
from ..__init__ import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/", methods=['GET'])
def hello():
    return "Welcome to Dudol's Social API!"

@auth_bp.route("/hello", methods=['GET'])
@login_required
def helloUser():
    return "Hello, " + current_user.username

@auth_bp.route("/verify", methods=['GET'])
def verify():
    if current_user.is_authenticated:
        user = {
            'uid': current_user.uid,
            'username' : current_user.username,
            'screenname' : current_user.screenname
            }
        return { 'auth': True, 'user': user }
    return { 'auth': False, 'user': None}

@auth_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return {
            'message': 'User currently logged in.'
        }

    req = request.get_json()
    email = req['email']
    password = req['password']
    remember = True if req['remember'] else False

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        login_user(user, remember)
        return {
            'id': user.uid
        }

    return {
            'message': 'Please check your login credentials and try again.'
        }

@auth_bp.route('/register', methods=['POST'])
def register():
    req = request.get_json()
    email = req['email']
    username = req['username']
    screenname = req['screenname']
    profile = req.get('profile')
    password = generate_password_hash(req['password'], method='sha256')

    # create new user with form data, password hashed so it isn't plain text
    new_user = User.create(username, screenname, profile, password, email)

    login_user(new_user)
    
    return {
            'id': new_user.uid
    }, 201

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return {
            'message':  'Logging out.'
    }


from flask import Blueprint, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from ..models.models import User
from ..__init__ import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/", methods=['GET'])
@login_required
def hello():
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
    username = req['password']
    screenname = req['screenname']
    password = req['password']

    user = User.query.filter_by(email=email).first() # query to find if user exists by email
    if user:
        return {
            'message':  'User already exists. Go to Login.'
        }

    # create new user with form data, password hashed so it isn't plain text
    new_user = User(email=email, username=username, screenname=screenname, password = generate_password_hash(password, method='sha256'))
    
    #add new user to db
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    
    return {
            'message':  'Signed up as a new user!'
    }

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return {
            'message':  'Logging out.'
    }

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (jwt_required, get_jwt_identity,
                                create_access_token, create_refresh_token, 
                                set_access_cookies, set_refresh_cookies, 
                                unset_jwt_cookies, current_user)
from ..models.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/", methods=['GET'])
def hello():
    return "Welcome to Dudol's Social API!"

@auth_bp.route("/hello", methods=['GET'])
@jwt_required()
def helloUser():
    return jsonify("Hello, " + current_user.username)

@auth_bp.route("/verify", methods=['GET'])
@jwt_required()
def verify():
    return jsonify({ 
        'user': 
        {
            'uid': current_user.uid,
            'username': current_user.username, 
            'screenname': current_user.screenname
        }   
     })

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(email=email).one_or_none()

    if email != user.email or not check_password_hash(user.password, password):
        return jsonify({'login': False}), 401

    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    resp = jsonify({'login': True})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 200

@auth_bp.route('/register', methods=['POST'])
def register():
    req = request.get_json()
    email = req['email']
    username = req['username']
    screenname = req['screenname']
    profile = req.get('profile')
    password = generate_password_hash(req['password'], method='sha256')

    user = User.create(username, screenname, profile, password, email)

    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    resp = jsonify({'login': True})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return jsonify({'register': True}), 201

@auth_bp.route('/logout')
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200

from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from ..models.models import User
from ..__init__ import db


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return "User currently logged in."

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        login_user(user, remember)
        return 'Logged in.'
    
    return 'Please check your login credentials and try again.'

@auth_bp.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    username = request.form.get('username')
    screenname = request.form.get('screenname')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # query to find if user exists by email
    if user:
        return 'User already exists. Go to Login.'

    # create new user with form data, password hashed so it isn't plain text
    new_user = User(email=email, username=username, screenname=screenname, password = generate_password_hash(password, method='sha256'))
    
    #add new user to db
    db.session.add(new_user)
    db.session.commit()

    return 'Signed up as a new user!'

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logging out.'


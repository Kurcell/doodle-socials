from dataclasses import dataclass
from flask import Flask, jsonify, render_template, request, url_for, redirect, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from datetime import datetime
import string

# app_ctx = app.app_context()
# app_ctx.push()
# current_app.config["ENV"]


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gxsfadrohqpnss:010bf417fdce3c2640007c67f4054326277b39d16958a568984054cb6fa8cb24@ec2-18-207-37-30.compute-1.amazonaws.com:5432/d5h4drurgvgtk6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# def app_context():
#     app = Flask(__name__)
#     with app.app_context():
#         yield


@dataclass
class User(db.Model):
    __tablename__ = "users"

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    screenname = db.Column(db.String(200), unique=False, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    createdat = db.Column(db.DateTime(200), default=datetime.utcnow)
    users_post = db.relationship('Post', backref='user')

@dataclass
class Post(db.Model):
    __tablename__ = "post"
    
    pid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
    canvas_pid = db.relationship('Canvas', backref='post')

@dataclass 
class Canvas(db.Model):
    __tablename__ = "canvas"
    
    cid = db.Column(db.Integer, primary_key=True)
    instructions = db.Column(db.String(500), nullable=False) 
    post_id = db.Column(db.Integer, db.ForeignKey('post.pid'))

@dataclass
class Blocking(db.Model):
    __tablename__ = "blocking"

    blocking_id = db.Column(db.Integer, primary_key=True) # to be used for query optimazation
    blockee_uid = db.Column(db.Integer, nullable=False)
    blocked_uid = db.Column(db.Integer, nullable=False)

@dataclass
class Following(db.Model):
    __tablename__ = "following"

    following_id = db.Column(db.Integer, primary_key=True) # to be used for query optimazation
    followee_uid = db.Column(db.Integer, nullable= False)
    followed_uid = db.Column(db.Integer, nullable= False)


@app.route("/users", methods=['GET'])
def display_all():
    return jsonify(User.query.all())

# @app.route('/new', methods = ['GET', 'POST'])
# def new():
#     if request.method == 'POST':
#         if not request.form['username'] or not request.form['screenname'] or not request.form['password']:
#             flash('Please enter all the required fields.', 'error')
#         else:
#             user = user(request.form['username'], request.form['screnname'], request.form['password'])

#             db.session.add(user)
#             db.session.commit()
#             flash('User added succesfully')
#             return redirect(url_for('display_all'))
#         return render_template('new.html')


if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)


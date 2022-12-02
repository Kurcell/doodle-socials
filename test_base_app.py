from dataclasses import dataclass
from flask import Flask, jsonify, render_template, request, url_for, redirect, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from datetime import datetime
import string



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gxsfadrohqpnss:010bf417fdce3c2640007c67f4054326277b39d16958a568984054cb6fa8cb24@ec2-18-207-37-30.compute-1.amazonaws.com:5432/d5h4drurgvgtk6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_ctx = app.app_context()
app_ctx.push()
current_app.config["ENV"]


db = SQLAlchemy(app)

@dataclass
class User(db.Model):
    __tablename__ = "users"
    uid: int 
    username: string
    screenname: string
    password: string
    email: string
    createdat: string

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    screenname = db.Column(db.String(200), unique=False, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    createdat = db.Column(db.DateTime(200), default=datetime.utcnow)
    users_post = db.relationship('Post', backref='user')


    def __init__(self, username, screenname, password, email):
        self.username = username
        self.screenname = screenname
        self.password = password
        self.email = email

    def __repr__(self):
        return f'<User {self.username}, {self.screenname}, {self.password}, {self.email}>'

@dataclass
class Post(db.Model):
    __tablename__ = "post"

    pid: int
    content: string
    user_id: int
    canvas_pid: string
    
    pid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
    canvas_pid = db.relationship('Canvas', backref='post')

    def __init__(self, pid, user_id, content):
        self.pid = pid
        self.uid = user_id
        self.content = content

@dataclass
class Canvas(db.Model):
    __tablename__ = "canvas"

    cid: int
    instructions: string
    post_id: int
    
    cid = db.Column(db.Integer, primary_key=True)
    instructions = db.Column(db.String(500), nullable=False) 
    post_id = db.Column(db.Integer, db.ForeignKey('post.pid'))

    def __init__(self, cid, post_id, instructions):
        self.cid = cid
        self.post_id = post_id
        self.instructions = instructions

@dataclass
class Blocking(db.Model):
    __tablename__ = "blocking"

    blocking_id = db.Column(db.Integer, primary_key=True) # to be used for query optimazation
    blockee_uid = db.Column(db.Integer, nullable=False)
    blocked_uid = db.Column(db.Integer, nullable=False)

    def __init__(self, blocking_id, blockee_uid, blocked_uid):
        self.blocking_id = blocking_id
        self.blockee_uid = blockee_uid
        self.blocked_uid = blocked_uid

@dataclass
class Following(db.Model):
    __tablename__ = "following"

    following_id = db.Column(db.Integer, primary_key=True) # to be used for query optimazation
    followee_uid = db.Column(db.Integer, nullable= False)
    followed_uid = db.Column(db.Integer, nullable= False)

    def __init__(self, following_id, followee_uid, followed_uid):
        self.following_id = following_id
        self.followee_uid = followed_uid
        self.followed_uid = followed_uid

@dataclass
class Likes(db.Model):
    __tablename__ = "likes"

    like_id: int
    liking_user: int
    liked_post: int

    like_id = db.Column(db.Integer, primary_key=True)
    liking_user = db.Column(db.Integer, db.ForeignKey('users.uid'))
    liked_post = db.Column(db.Integer, db.ForeignKey('post.pid'))

    @staticmethod
    def create(liking_user, liked_post):
        """
        Create new instance of a user liking a post
        """
        new_follow = Following(followee_uid, followed_uid)
        db.session.add(new_follow)
        db.session.commit()

    @staticmethod
    def delete(like_id):
        """
        Delete user liking a post
        """
        follow = Following.query.filter_by(following_id = following_id).one()
        db.session.delete(follow)
        db.session.commit()



@app.route("/users", methods=['GET'])
def display_all():
    return jsonify(User.query.all())

@app.route("/test", methods=['GET'])
def test():
    return "Hahaha"



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
    db.create_all()
    app.run(debug=True)

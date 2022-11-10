from .. import db
from dataclasses import dataclass
from datetime import datetime
import string

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

    @staticmethod
    def create(username, screenname, password, email):
        """
        Create new user
        """
        new_user = User(username, screenname, password, email)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def get_users():
        """
        return: list of user details
        """
        users = [
            {
                'uid': i.id,
                'username': i.username,
                'screenname': i.screenname,
                'password': i.password,
                'email': i.email,
                'creatdat': i.creatdat, # there was a comma here, he will be missed
            }
            for i in User.query.order_by('id').all
        ]
        return users

@dataclass
class Post(db.Model):
    __tablename__ = "post"

    pid: int
    user_id: int
    createdat: datetime
    
    pid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
    createdat = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, pid, user_id, createdat):
        self.pid = pid
        self.user_id = user_id
        self.createdat = createdat

    @staticmethod
    def create(user_id):
        """
        Create new post
        """
        post = Post(None, user_id, None)
        db.session.add(post)
        db.session.commit()

    @staticmethod
    def delete(pid):
        """
        Delete existing post
        """
        post = Post.query.filter_by(pid = pid).one()
        db.session.delete(post)
        db.session.commit()

# @dataclass 
# class Canvas(db.Model):
#     __tablename__ = "canvas"
    
#     cid = db.Column(db.Integer, primary_key=True)
#     instructions = db.Column(db.String(500), nullable=False) 
#     post_id = db.Column(db.Integer, db.ForeignKey('post.pid'))

#     @staticmethod
#     def create(content, user_id, canvas_pid):
#         """
#         Create new canvas
#         """
#         new_canvas = Canvas(instructions, post_id)
#         db.session.add(new_canvas)
#         db.session.commit()

@dataclass
class Blocking(db.Model):
    __tablename__ = "blocking"

    blocking_id: int
    blockee_uid: int
    blocked_uid: int

    blocking_id = db.Column(db.Integer, primary_key=True) # to be used for query optimazation
    blockee_uid = db.Column(db.Integer, nullable=False)
    blocked_uid = db.Column(db.Integer, nullable=False)

    @staticmethod
    def create(blockee_uid, blocked_uid):
        """
        Create new instance of a user blocking another user
        """
        new_block = Blocking(blockee_uid, blocked_uid)
        db.session.add(new_block)
        db.session.commit()

@dataclass
class Following(db.Model):
    __tablename__ = "following"

    following_id: int
    followee_uid: int
    followed_uid: int

    following_id = db.Column(db.Integer, primary_key=True) # to be used for query optimazation
    followee_uid = db.Column(db.Integer, nullable= False)
    followed_uid = db.Column(db.Integer, nullable= False)

    @staticmethod
    def create(followee_uid, followed_uid):
        """
        Create new instance of a user following another user
        """
        new_follow = Following(followee_uid, followed_uid)
        db.session.add(new_follow)
        db.session.commit()



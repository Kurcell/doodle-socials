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
    profile: string
    password: string
    email: string
    createdat: string

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    screenname = db.Column(db.String(200), nullable=False)
    profile = db.Column(db.String())
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200),unique=True, nullable=False)
    createdat = db.Column(db.DateTime(200), nullable=False, default=datetime.utcnow)
    users_post = db.relationship('Post', backref='user')

    def __init__(self, username, screenname, profile, password, email):
        self.username = username
        self.screenname = screenname
        self.profile = profile
        self.password = password
        self.email = email

    @staticmethod
    def create(username, screenname, profile, password, email):
        """
        Create new user
        """
        new_user = User(username, screenname, profile, password, email)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    @staticmethod
    def update(uid, username, screenname, profile, password, email):
        """
        Update existing user
        """
        user = User.query.filter_by(uid = uid).one()
        user.username = username if username is not None else user.username
        user.screenname = screenname if screenname is not None else user.screenname
        user.profile = profile if profile is not None else user.profile
        user.password = password if password is not None else user.password
        user.email = email if email is not None else user.email
        db.session.commit()
        return user
    
    @staticmethod
    def delete(uid):
        """
        Delete existing user
        """
        user = User.query.filter_by(uid = uid).one()
        db.session.delete(user)
        db.session.commit()
        return user

@dataclass
class Post(db.Model):
    __tablename__ = "post"

    pid: int
    user_id: int
    doodle_id: int
    createdat: datetime
    likes: int
    
    pid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
    doodle_id = db.Column(db.Integer)
    createdat = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)


    def __init__(self, pid, user_id, doodle_id, createdat, likes):
        self.pid = pid
        self.user_id = user_id
        self.doodle_id = doodle_id
        self.createdat = createdat
        self.likes = likes

    @staticmethod
    def create(user_id, doodle_id):
        """
        Create new post
        """
        post = Post(None, user_id, doodle_id, None, 0)
        db.session.add(post)
        db.session.commit()
        return post
    
    @staticmethod
    def update(pid, user_id,doodle_id,):
        """
        Update existing post
        """
        post = Post.query.filter_by(pid = pid).one()
        post.user_id = user_id if user_id is not None else post.user_id
        post.doodle_id = doodle_id if doodle_id is not None else post.doodle_id
        db.session.commit()
        return post

    @staticmethod
    def delete(pid):
        """
        Delete existing post
        """
        post = Post.query.filter_by(pid = pid).one()
        db.session.delete(post)
        db.session.commit()
        return post

@dataclass
class Blocking(db.Model):
    __tablename__ = "blocking"

    blocking_id: int
    blockee_uid: int
    blocked_uid: int

    blocking_id = db.Column(db.Integer, primary_key=True) # to be used for query optimazation
    blockee_uid = db.Column(db.Integer, nullable=False)
    blocked_uid = db.Column(db.Integer, nullable=False)

    def __init__(self, blocking_id, blockee_uid, blocked_uid):
        self.blocking_id = blocking_id
        self.blockee_uid = blockee_uid
        self.blocked_uid = blocked_uid


    @staticmethod
    def create(blockee_uid, blocked_uid):
        """
        Create new instance of a user blocking another user
        """
        block = Blocking(blockee_uid, blocked_uid)
        db.session.add(block)
        db.session.commit()
        return block
    
    @staticmethod
    def delete(blocking_id):
        """
        Delete blocking of a user
        """
        block = Blocking.query.filter_by(blocking_id= blocking_id).one()
        db.session.delete(block)
        db.session.commit()
        return block

@dataclass
class Following(db.Model):
    __tablename__ = "following"

    following_id: int
    followee_uid: int
    followed_uid: int

    following_id = db.Column(db.Integer, primary_key=True) # to be used for query optimazation
    followee_uid = db.Column(db.Integer, nullable= False)
    followed_uid = db.Column(db.Integer, nullable= False)

    def __init__(self, following_id, followee_uid, followed_uid):
        self.following_id = following_id
        self.followee_uid = followee_uid
        self.followed_uid = followed_uid

    @staticmethod
    def create(followee_uid, followed_uid):
        """
        Create new instance of a user following another user
        """
        follow = Following(followee_uid, followed_uid)
        db.session.add(follow)
        db.session.commit()
        return follow

    @staticmethod
    def delete(following_id):
        """
        Delete following of a user
        """
        follow = Following.query.filter_by(following_id = following_id).one()
        db.session.delete(follow)
        db.session.commit()
        return follow


@dataclass
class Likes(db.Model):
    __tablename__ = "likes"

    like_id: int
    liking_user: int
    liked_post: int

    like_id = db.Column(db.Integer, primary_key=True)
    liking_user = db.Column(db.Integer, nullable=False)
    liked_post = db.Column(db.Integer, nullable=False)

    def __init__(self, like_id, liking_user, liked_post):
        self.like_id = like_id
        self.liking_user = liking_user
        self.liked_post = liked_post


    @staticmethod
    def create(liking_user, liked_post):
        """
        Create new instance of a user liking a post
        """
        like= Likes(None, liking_user, liked_post)
        db.session.add(like)
        db.session.commit()
        return like

    @staticmethod
    def delete(like_id):
        """
        Delete user liking a post
        """
        like = Likes.query.filter_by(like_id = like_id).one()
        db.session.delete(like)
        db.session.commit()
        return like

from dataclasses import dataclass
import string
from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime

# basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] =\
#         'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gxsfadrohqpnss:010bf417fdce3c2640007c67f4054326277b39d16958a568984054cb6fa8cb24@ec2-18-207-37-30.compute-1.amazonaws.com:5432/d5h4drurgvgtk6'
# the intent is to use postgresql as the database engine, need to ask

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@dataclass
class User(db.Model):
    __tablename__ = "users"

    uid: int
    username: string
    screenname: string
    password: string
    createdat: datetime

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    screenname = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    #blocking_uid
    #following_uid
    createdat = db.Column(db.DateTime(200), default = datetime.utcnow)


    def __init__(self, username, screenname, password, email, createdat):
        self.username = username
        self.screenname = screenname
        self.password = password
        self.email = email
        self.createdat = createdat

@dataclass
class Post(db.Model):
    __tablename__ = "Posts"

    pid: int
    uid: int 
    content: string
    
    pid = db.column(db.Integer, primary_key=True)
    user_id = db.column(db.Integer, db.ForeignKey('user.uid'))
    content = db.Column(db.String(500), nullable=False)

    def __init__(self, pid, user_id, content):
        self.pid = pid
        self.uid = user_id
        self.content = content


@dataclass 
class Canvas(db.Model):
    __tablename__ = "Canvas"

    cid: int
    post_id: int 
    content: string
    
    cid = db.column(db.Integer, primary_key=True)
    post_id = db.column(db.Integer, db.ForeignKey('post.user_id'))
    instructions = db.Column(db.String(500), nullable=False) 

    def __init__(self, cid, post_id, instructions):
        self.cid = cid
        self.post_id = post_id
        self.instructions = instructions




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


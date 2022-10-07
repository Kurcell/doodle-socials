from dataclasses import dataclass
import string
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gxsfadrohqpnss:010bf417fdce3c2640007c67f4054326277b39d16958a568984054cb6fa8cb24@ec2-18-207-37-30.compute-1.amazonaws.com:5432/d5h4drurgvgtk6'
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
    createdat = db.Column(db.DateTime(200), default = datetime.utcnow)

@app.route('/', methods=['GET'])
def index():
    return 'Badabing baby.'

@app.route('/users', methods=['GET'])
def users():
     return jsonify(User.query.all())

if __name__ == "__main__":
    app.run(debug=True)


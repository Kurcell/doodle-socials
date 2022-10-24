import os

class Config:
    ENV = 'env'
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))
    SQLALCHEMY_DATABASE_URI = 'postgresql://gxsfadrohqpnss:010bf417fdce3c2640007c67f4054326277b39d16958a568984054cb6fa8cb24@ec2-18-207-37-30.compute-1.amazonaws.com:5432/d5h4drurgvgtk6'
    SQLALCHEMY_TRACK_MODIFICATIONS= False
"""
Inserting dummy data into tables
"""

from src import init_app
from src.models.models import User, Post, Following, Blocking

def insert_dummy_data():
    app = init_app()
    with app.app_context():
        User.create('hogwash', 'HolyAnthony123', '123', 'an.thony@ymail.com')
        
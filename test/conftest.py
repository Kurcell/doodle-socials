import pytest
from src import create_app, db
from src.models.models import User, Post, Follows, Likes

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        'JWT_SECRET_KEY': 'doodle-secret-api'
    })

    with app.app_context():
        db.create_all()
        data_setup()

    yield app

    db.drop_all()

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def data_setup():
        db.session.add(User('purcell',
            'Kevin',
            'https://abdielcortes.github.io/capstone-website/images/kevin.jpeg',
            'HipsDontLie97',
            'kevin.purcell@upr.edu'
        ))
        db.session.add(Post(1, 1))
        db.session.add(Post(1, 2))
        db.session.add(Post(1, 3))
        db.session.add(Post(1, 4))
        
        db.session.add(User('puig',
            'Theo',
            'https://abdielcortes.github.io/capstone-website/images/theo.jpeg',
            'WillyWonderland23',
            'theo.puig@upr.edu'
        ))
        db.session.add(Post(2, 5))
        db.session.add(Post(2, 6))
        db.session.add(Post(2, 7))
        db.session.add(Post(2, 8))

        db.session.add(User('cortes',
            'Abdiel',
            'https://abdielcortes.github.io/capstone-website/images/abdiel.jpg',
            'Godmode225',
            'abdiel.cortes@upr.edu'
        ))
        db.session.add(Post(3, 9))
        db.session.add(Post(3, 10))
        db.session.add(Post(3, 11))
        db.session.add(Post(3, 12))

        db.session.add(User('tua',
            'Jose',
            'https://abdielcortes.github.io/capstone-website/images/jose.jpg',
            'KeqingSimp44',
            'jose.tua@upr.edu'
        ))
        db.session.add(Post(4, 13))
        db.session.add(Post(4, 14))
        db.session.add(Post(4, 15))
        db.session.add(Post(4, 16))

        db.session.add(Follows(1, 2))
        db.session.add(Follows(1, 3))
        db.session.add(Follows(2, 3))
        db.session.add(Follows(3, 2))
        db.session.add(Follows(4, 1))
        db.session.add(Follows(4, 2))
        db.session.add(Follows(4, 3))

        db.session.commit()
import pytest
from src import create_app, db
from src.models.models import User

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
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
        user1 = User('wakawaka',
            'Shakira',
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRrNuITVVbAt4BzGSgIdaVY2n9v2xH4uJSVxw&usqp=CAU',
            'HipsDontLie2',
            'lolelole@ooo.com'
        )
        user2 = User('alealejandro',
            'Lady Gaga',
            'https://images-prod.dazeddigital.com/640/0-58-1080-720/azure/dazed-prod/1320/8/1328021.jpg',
            'BadRomance83',
            'papapapa@razzi.com'
        )
        user3 = User('toxic',
            'Britney Spears',
            'https://cdn.justjared.com/wp-content/uploads/headlines/2021/01/britney-spears-justin-timberlake-jean-outfit-anniversary.jpg',
            'DeminEverything',
            'womanizer@2007.com'
        )
        user4 = User('rocketman',
            'Elton John',
            'https://i.guim.co.uk/img/media/41977eef3a48fff6707e501c019a54bdb7d41a41/9_69_7324_4395/master/7324.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=b08a33cf9ec842cfa6f7ab74fedba4f4',
            'SaturdayN1ght',
            'Gnomeo@yellowbrickroad.com'
        )
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(user4)
        db.session.commit()
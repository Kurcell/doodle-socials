from src.models.models import User
from werkzeug.security import check_password_hash

def test_user_create(client):
    """
    GIVEN a user data model
    WHEN a user's create function is called
    THEN check that the function leads to the creation of a user if the request is proper
    """

    user = User.create('ferdinand', 'franz', 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Franz_ferdinand.jpg/1200px-Franz_ferdinand.jpg', 'justoneguy', 'austria@hungary.com')

    assert user.screenname == 'franz'
    assert check_password_hash(user.password, 'justoneguy')


def test_user_update(client):
    """
    GIVEN a user data model
    WHEN a user's update function is called
    THEN check that the function leads to the modification of a user if the request is proper
    """

    user = User.update(6, None, "oops", None, None, None)

    assert user.screenname == 'oops'
    assert user.username == 'ferdinand'
    

def test_user_delete(client):
    """
    GIVEN a user data model
    WHEN a user's delete function is called
    THEN check that the function leads to the deletion of a user if the request is proper
    """

    user = User.delete(6)

    assert user.uid == 6

import pytest
from src.models.models import User
from werkzeug.security import check_password_hash

@pytest.fixture(scope="module")
def user():
    user = User('Milestone23', 'Hilbert', 'https://google.com', 'password', 'hillybobbert53@gmail.com')
    return user

def test_user_create(user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    assert user.username == 'Milestone23'
    assert user.screenname == 'Hilbert'
    assert user.profile == 'https://google.com'
    assert user.email == 'hillybobbert53@gmail.com'
    assert check_password_hash(user.password, 'password')

def test_user_update(user):
    """
    GIVEN an existing User
    WHEN this User is updated
    THEN check that the updated fields and only the updated fields have changed
    """
    assert False
    
def test_user_delete(user):
    """
    GIVEN an existing User
    WHEN this User is deleted
    THEN check that the user is no longer in the database
    """
    assert False
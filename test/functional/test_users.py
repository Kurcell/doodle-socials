import json

def test_user_readMany(client):
    """
    GIVEN a test client
    WHEN the readMany route for users is called
    THEN assure that valid requests return valid responses
    """

    response = client.get('/users')
    users = json.loads(response.data)

    assert len(users) == 4
    assert response.status == '200 OK'


def test_user_readOne(client):
    """
    GIVEN a test client
    WHEN the readOne route for users is called
    THEN check that valid requests return valid responses
    """
    response = client.get('/user/2')
    user = json.loads(response.data)
    
    assert user.get('username') == 'puig'
    assert response.status == '200 OK'

def test_user_follow(client):
    """
    GIVEN a test client
    WHEN the follow route for users is called
    THEN check that valid requests return valid reponses
    """

    log_in_data = {
        'email': 'kevin.purcell@upr.edu',
        'password': 'HipsDontLie97'
    }
    client.post('login', json=log_in_data)

    response = client.get('/user/follow?uid=4')
    follow = json.loads(response.data)
    print(follow)
    
    assert follow.get('follower_id') == 1 and follow.get('followee_id') == 4
    assert response.status == '201 CREATED'

    response = client.get('/user/follow?uid=4')
    unfollow = json.loads(response.data)

    print(unfollow)
    assert unfollow.get('follower_id') == 1 and unfollow.get('followee_id') == 4
    assert response.status == '200 OK'

def test_user_create(client):
    """
    GIVEN a test client
    WHEN the create route for users is called
    THEN check that valid requests return valid reponses
    """

    request_data = {
        'username': 'boingo',
        'screenname': 'oingo',
        'email': 'oingo@boingo.com',
        'password': 'besberr',
        'profile': 'https://static.wikia.nocookie.net/jjba/images/a/a0/Oingo_Boingo_Brothers_Adventure.jpg/revision/latest?cb=20180820171318'
    }

    response = client.post('/user', json=request_data)
    user = json.loads(response.data)
    
    assert user.get('username') == 'boingo'
    assert response.status == '201 CREATED'


def test_user_update(client):
    """
    GIVEN a test client
    WHEN the update route for users is called
    THEN check that valid requests return valid reponses
    """
    request_data = {
        'screenname': 'Kevin Y.'
    }

    response = client.put('/user/1', json=request_data)
    user = json.loads(response.data)
    
    assert user.get('screenname') == 'Kevin Y.'
    assert user.get('username') == 'purcell'
    assert response.status == '200 OK'


def test_user_delete(client):
    """
    GIVEN a test client
    WHEN the update route for users is called
    THEN check that valid requests return valid reponses
    """

    response = client.delete('/user/3')
    user = json.loads(response.data)
    
    assert user.get('username') == 'cortes'
    assert response.status == '200 OK'
    
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
    
    assert user.get('username') == 'alealejandro'
    assert response.status == '200 OK'

def test_user_create(client):
    """
    GIVEN a test client
    WHEN the create route for users in called
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
    WHEN the update route for users in called
    THEN check that valid requests return valid reponses
    """
    request_data = {
        'screenname': 'Gnomeo'
    }

    response = client.put('/user/4', json=request_data)
    user = json.loads(response.data)
    
    assert user.get('screenname') == 'Gnomeo'
    assert user.get('username') == 'rocketman'
    assert response.status == '200 OK'

def test_user_delete(client):
    """
    GIVEN a test client
    WHEN the update route for users in called
    THEN check that valid requests return valid reponses
    """

    response = client.delete('/user/3')
    user = json.loads(response.data)
    
    assert user.get('username') == 'toxic'
    assert response.status == '200 OK'
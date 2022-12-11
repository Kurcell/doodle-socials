import json

def test_post_readMany(client):
    """
    GIVEN a test client
    WHEN the readMany route for posts is called
    THEN assure that valid requests return valid responses
    """

    response = client.get('/posts')
    posts = json.loads(response.data)

    assert response.status == '200 OK'
    assert len(posts) > 0
    

def test_post_readOne(client):
    """
    GIVEN a test client
    WHEN the readOne route for posts is called
    THEN check that valid requests return valid responses
    """
    response = client.get('/post/2')
    post = json.loads(response.data)
    
    assert response.status == '200 OK'

def test_post_discover(client):
    """
    GIVEN a test client
    WHEN the discover route for posts is called
    THEN check that valid requests return valid responses
    """
    log_in_data = {
        'email': 'kevin.purcell@upr.edu',
        'password': 'HipsDontLie97'
    }
    client.post('login', json=log_in_data)

    response = client.get('/posts/discover')
    posts = json.loads(response.data)

    assert response.status == '200 OK'
    assert len(posts) > 0 


def test_post_following(client):
    """
    GIVEN a test client
    WHEN the following route for posts is called
    THEN check that valid requests return valid responses
    """
    log_in_data = {
        'email': 'kevin.purcell@upr.edu',
        'password': 'HipsDontLie97'
    }
    client.post('login', json=log_in_data)

    response = client.get('/posts/following')
    posts = json.loads(response.data)

    assert response.status == '200 OK'
    assert len(posts) > 0

def test_post_like(client):
    """
    GIVEN a test client
    WHEN the like route for posts is called
    THEN check that valid requests return valid responses
    """
    log_in_data = {
        'email': 'kevin.purcell@upr.edu',
        'password': 'HipsDontLie97'
    }
    logged_in = client.post('login', json=log_in_data)

    assert json.loads(logged_in.data).get('login')

    response = client.get('/post/like?pid=5')
    like = json.loads(response.data)

    assert response.status == '201 CREATED'
    assert like.get('liked_post') == 5 and like.get('liking_user') == 1

    response = client.get('/post/like?pid=5')
    like = json.loads(response.data)

    assert response.status == '200 OK'
    assert like.get('liked_post') == 5 and like.get('liking_user') == 1


def test_post_create(client):
    """
    GIVEN a test client
    WHEN the create route for posts in called
    THEN check that valid requests return valid reponses
    """

    request_data = {
        'user_id': 1,
        'doodle_id': 1
    }

    response = client.post('/post', json=request_data)
    post = json.loads(response.data)
    
    assert response.status == '201 CREATED'
    assert post.get('user_id') == 1 and post.get('doodle_id') == 1


def test_post_update(client):
    """
    GIVEN a test client
    WHEN the update route for posts in called
    THEN check that valid requests return valid reponses
    """
    request_data = { 'doodle_id': 2}

    response = client.put('/post/1', json=request_data)
    post = json.loads(response.data)

    assert response.status == '200 OK'
    assert post.get('pid') == 1 and post.get('doodle_id') == 2
    

def test_post_delete(client):
    """
    GIVEN a test client
    WHEN the update route for posts in called
    THEN check that valid requests return valid reponses
    """

    response = client.delete('/post/2')
    post = json.loads(response.data)
    
    assert response.status == '200 OK'
    assert post.get('pid') == 2

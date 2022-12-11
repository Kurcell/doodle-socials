
def test_general_greet(client):
    """
    GIVEN a test client
    WHEN the general greeting route '/' is called
    THEN check that the response is the greeting
    """

    response = client.get('/')

    assert response.status == '200 OK'
    assert response.data == b"Welcome to Dudol's Social API!"


def test_auth_login(client):
    """
    GIVEN a test client
    WHEN the login route for auth is called
    THEN check for the correct response and that the user is logged in
    """
    logged_out = client.get('verify')

    assert logged_out.status == '401 UNAUTHORIZED'

    incorrect_log_in_data = {
        'email': 'kevin.purcell@upr.edu',
        'password': 'HiPsDontLie97'
    }

    log_in = client.post('login', json=incorrect_log_in_data)

    assert log_in.status == '401 UNAUTHORIZED'

    correct_log_in_data = {
        'email': 'kevin.purcell@upr.edu',
        'password': 'HipsDontLie97'
    }

    log_in = client.post('login', json=correct_log_in_data)

    assert log_in.status == '200 OK'

    logged_in = client.get('verify')

    assert logged_in.status == '200 OK'


def test_auth_logout(client):
    """
    GIVEN a test client
    WHEN the logout route for auth is called
    THEN check for the correct response and that the user is logged out
    """

    logged_in = client.get('verify')

    assert logged_in.status == '200 OK'

    log_out = client.post('logout')  

    assert log_out.status == '200 OK'

    logged_out = client.get('verify')

    assert logged_out.status == '401 UNAUTHORIZED'

__author__ = "Itai Dotan"


def test_home_no_name(client):
    rv = client.get('/')
    assert b'Welcome to this site' in rv.data


def test_new_friend_logged(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.get('/new_friend',  follow_redirects=True)
    assert b'Welcome itai' in rv.data


def test_new_friend_not_logged(client):
    rv = client.get('/new_friend',  follow_redirects=True)
    assert b'Login' in rv.data

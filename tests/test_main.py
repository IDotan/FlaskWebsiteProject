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
    assert b'Remember me' in rv.data


def test_about(client):
    rv = client.get('/about')
    assert b'Site about' in rv.data


def test_about_logged(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.get('/about')
    assert b'Site about' in rv.data

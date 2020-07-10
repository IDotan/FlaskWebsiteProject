import os
import tempfile
import pytest
import shutil
from flaskr import create_app


app = create_app()


@pytest.fixture
def client():
    os.rename(r"./flaskr/users.db", r"./flaskr/back.db")
    shutil.copy(r"./flaskr/test.db", r"./flaskr/users.db")

    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])
    os.remove(r"./flaskr/users.db")
    os.rename(r"./flaskr/back.db", r"./flaskr/users.db")


def test_home_no_name(client):
    rv = client.get('/')
    assert b'Welcome to this site' in rv.data


def test_log_in_page(client):
    rv = client.get('/login')
    assert b'Remember me' in rv.data


def test_login_page_post(client):
    rv = client.post('/login', data=dict(username="itai2", psw="Hello*1234"), follow_redirects=True)
    assert b'Good to see you again, itai' in rv.data


def test_logout(client):
    rv = client.get('/logout',  follow_redirects=True)
    assert b'Welcome to this site' in rv.data


def test_register_page_post_worng_info(client):
    rv = client.post('/login', data=dict(username="itai2", psw="12345"), follow_redirects=True)
    assert b'Wrong login information' in rv.data
    rv = client.post('/login', data=dict(username="itai", psw="Hello*1234"), follow_redirects=True)
    assert b'Wrong login information' in rv.data


def test_register_page_post(client):
    rv = client.post('/register', data=dict(username="itai", psw="1234", email="test@test.com", fname='name',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'one or more of your info use invalid character' in rv.data


def test_register_page_post1(client):
    rv = client.post('/register', data=dict(username="itai3", psw="1234", email="test@test.com", fname='name',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'one or more of your info use invalid character' in rv.data


def test_register_page_post2(client):
    rv = client.post('/register', data=dict(username="itai2", psw="Hello*1234", email="test@test.com", fname='name',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'User name already exists' in rv.data


def test_register_page_post3(client):
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="i@i.com", fname='name',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'Email address already in use' in rv.data


def test_register_page_post4(client):
    """ name error raise """
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='name~',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'one or more of your info use invalid character' in rv.data


def test_register_page_post5(client):
    """ name error raise """
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='n~ame',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'one or more of your info use invalid character' in rv.data


def test_register_page_post6(client):
    """ name error raise """
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='na{me',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'one or more of your info use invalid character' in rv.data


def test_register_page_post7(client):
    """ name error raise """
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='nam]e',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'one or more of your info use invalid character' in rv.data


def test_register_page_post8(client):
    """ name error raise """
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='na:me',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'one or more of your info use invalid character' in rv.data


def test_register_page_post9(client):
    """ gender error raise """
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='name',
                                            lname="name", gender=3), follow_redirects=True)
    assert b'one or more of your info use invalid character' in rv.data


def test_register_page_post_valid(client):
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='name',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'Welcome name' in rv.data
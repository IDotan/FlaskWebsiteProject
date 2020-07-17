def test_log_in_page(client):
    rv = client.get('/login')
    assert b'Login' in rv.data


def test_register_page(client):
    rv = client.get('/register')
    assert b'Create Account' in rv.data


def test_login_page_post_remember_on(client):
    rv = client.post('/login', data=dict(username="itai2", psw="Hello*1234", remember="on"), follow_redirects=True)
    assert b'Good to see you again, itai' in rv.data


def test_login_page_post_no_remember(client):
    rv = client.post('/login', data=dict(username="itai2", psw="Hello*1234"), follow_redirects=True)
    assert b'Good to see you again, itai' in rv.data


def test_logout(client):
    rv = client.get('/logout',  follow_redirects=True)
    assert b'Welcome to this site' in rv.data


def test_login_page_post_wrong_info(client):
    rv = client.post('/login', data=dict(username="itai2", psw="12345"), follow_redirects=True)
    assert b'Wrong login information' in rv.data
    rv = client.post('/login', data=dict(username="itai", psw="Hello*1234"), follow_redirects=True)
    assert b'Wrong login information' in rv.data


# info already in use
def test_register_page_post_user_taken(client):
    rv = client.post('/register', data=dict(username="itai2", psw="Hello*1234", email="test@test.com", fname='name',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'User name already exists' in rv.data


def test_register_page_post_email_taken(client):
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="i@i.com", fname='name',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'Email address already in use' in rv.data


# invalid info
def test_register_page_post_invalid_psw(client):
    rv = client.post('/register', data=dict(username="itai3", psw="1234", email="test@test.com", fname='name',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'one or more of your info is invalid' in rv.data


def test_register_page_post_invalid_psw2(client):
    """ gender error raise """
    rv = client.post('/register', data=dict(username="itai3", psw="כשכ*1234", email="test@test.com", fname='name',
                                            lname="name", gender='1'), follow_redirects=True)
    assert b'one or more of your info is invalid' in rv.data


def test_register_page_post_invalid_name(client):
    """ name error raise """
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='name~',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'one or more of your info is invalid' in rv.data


def test_register_page_post_invalid_name2(client):
    """ name error raise """
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='n~ame',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'one or more of your info is invalid' in rv.data


def test_register_page_post_invalid_name3(client):
    """ name error raise """
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='na{me',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'one or more of your info is invalid' in rv.data


def test_register_page_post_invalid_name4(client):
    """ name error raise """
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='nam]e',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'one or more of your info is invalid' in rv.data


def test_register_page_post_invalid_last_name(client):
    """ name error raise """
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='name',
                                            lname="nam[e", gender=1), follow_redirects=True)
    assert b'one or more of your info is invalid' in rv.data


def test_register_page_post_invalid_gender(client):
    """ gender error raise """
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='name',
                                            lname="name", gender=3), follow_redirects=True)
    assert b'one or more of your info is invalid' in rv.data


def test_register_page_post_invalid_gender2(client):
    """ gender error raise """
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='name',
                                            lname="name", gender='hey'), follow_redirects=True)
    assert b'one or more of your info is invalid' in rv.data


def test_register_page_post_invalid_email(client):
    """ gender error raise """
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="t.com", fname='name',
                                            lname="name", gender='1'), follow_redirects=True)
    assert b'one or more of your info is invalid' in rv.data


def test_register_page_post_invalid_username(client):
    """ gender error raise """
    rv = client.post('/register', data=dict(username="He12*", psw="Hello*1234", email="test@test.com", fname='name',
                                            lname="name", gender='1'), follow_redirects=True)
    assert b'one or more of your info is invalid' in rv.data


def test_register_page_post_invalid_username2(client):
    """ gender error raise """
    rv = client.post('/register', data=dict(username="He Ho", psw="Hello*1234", email="test@test.com", fname='name',
                                            lname="name", gender='1'), follow_redirects=True)
    assert b'one or more of your info is invalid' in rv.data


def test_register_page_post_invalid_username3(client):
    """ gender error raise """
    rv = client.post('/register', data=dict(username="itai", psw="Hello*1234", email="test@test.com", fname='name',
                                            lname="name", gender='1'), follow_redirects=True)
    assert b'one or more of your info is invalid' in rv.data


# valid register
def test_register_page_post_valid(client):
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='name',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'Welcome name' in rv.data
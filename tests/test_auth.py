__author__ = "Itai Dotan"


def test_log_in_page(client):
    rv = client.get('/login')
    assert b'Remember me' in rv.data


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


def test_register_page_post_invalid_name_to_long(client):
    """ name error raise """
    test_string = "hahadfhaghahaghaghagaghhhagahha"
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='name',
                                            lname=test_string, gender=1), follow_redirects=True)
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


def test_register_page_user_id_available_to_short(client):
    rv = client.post('/userIDAvailable', data=dict(usernameCheck='itai'))
    assert b'"valid":"no"' in rv.data


def test_register_page_user_id_available_not_valid_char(client):
    rv = client.post('/userIDAvailable', data=dict(usernameCheck='itai54*'))
    assert b'"valid":"no"' in rv.data


def test_register_page_user_id_available_already_in_use(client):
    rv = client.post('/userIDAvailable', data=dict(usernameCheck='itai2'))
    assert b'"valid":"no"' in rv.data


def test_register_page_user_id_available_valid(client):
    rv = client.post('/userIDAvailable', data=dict(usernameCheck='itai23'))
    assert b'"valid":"yes"' in rv.data


def test_register_page_email_available_not_mail(client):
    rv = client.post('/emailAvailable', data=dict(emailCheck='notAMail'))
    assert b'"valid":"no"' in rv.data


def test_register_page_email_available_not_mail2(client):
    rv = client.post('/emailAvailable', data=dict(emailCheck='notAMail@'))
    assert b'"valid":"no"' in rv.data


def test_register_page_email_available_not_mail3(client):
    rv = client.post('/emailAvailable', data=dict(emailCheck='notAMail@the'))
    assert b'"valid":"no"' in rv.data


def test_register_page_email_available_not_mail4(client):
    rv = client.post('/emailAvailable', data=dict(emailCheck='notAMail@the.'))
    assert b'"valid":"no"' in rv.data


def test_register_page_email_available_already_taken(client):
    rv = client.post('/emailAvailable', data=dict(emailCheck='i@i.com'))
    assert b'"valid":"no"' in rv.data


def test_register_page_email_available_valid(client):
    rv = client.post('/emailAvailable', data=dict(emailCheck='i2@i.com'))
    assert b'"valid":"yes"' in rv.data


# valid register
def test_register_page_post_valid(client):
    rv = client.post('/register', data=dict(username="itai3", psw="Hello*1234", email="test@test.com", fname='name',
                                            lname="name", gender=1), follow_redirects=True)
    assert b'Welcome name' in rv.data

from flaskr.models import UsersToDo, User
import os
from io import BytesIO

__author__ = "Itai Dotan"


def test_not_profile(client):
    rv = client.get('/profile', follow_redirects=True)
    assert b'Login' in rv.data


def test_logged_profile(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.get('/profile', follow_redirects=True)
    assert b'Current password' in rv.data


def test_logged_profile_change_password_wrong_current(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.post('/psw_change', data=dict(old_psw='nope', new_psw="Good*1234", confirm_psw="Good*1234"),
                     follow_redirects=True)
    assert b'Current password incorrect' in rv.data


def test_logged_profile_change_password_same(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.post('/psw_change', data=dict(old_psw='Hello*1234', new_psw="Hello*1234", confirm_psw="Good*1234"),
                     follow_redirects=True)
    assert b'be the same as the old password' in rv.data


def test_logged_profile_change_password_invalid_new(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.post('/psw_change', data=dict(old_psw='Hello*1234', new_psw="nope", confirm_psw="Good*1234"),
                     follow_redirects=True)
    assert b'New password is invalid' in rv.data


def test_logged_profile_change_password_no_match(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.post('/psw_change', data=dict(old_psw='Hello*1234', new_psw="Good*1234", confirm_psw="nope"),
                     follow_redirects=True)
    assert b'match the confirm password' in rv.data


def test_logged_profile_change_password(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.post('/psw_change', data=dict(old_psw='Hello*1234', new_psw="Good*1234", confirm_psw="Good*1234"),
                     follow_redirects=True)
    assert b'Your password was changed' in rv.data
    rv = client.post('/psw_change', data=dict(old_psw='Good*1234', new_psw="Hello*1234", confirm_psw="Hello*1234"),
                     follow_redirects=True)
    assert b'Your password was changed' in rv.data


def test_upload(client):
    client.post('/login', data=dict(username="delete_test", psw="Hello*1234"))
    pic = str(os.getcwd()) + r'\flaskr\static\img\randomProfile\2.jpg'
    with open(pic, 'rb') as jpg:
        rv = client.post('/upload_pic', data=dict(file=jpg),
                         content_type='multipart/form-data', follow_redirects=True)
    rv = client.get('/profile')
    assert b'user_pic_3.jpg' in rv.data
    client.post('/login', data=dict(username="delete_test", psw="Hello*1234"))
    pic2 = str(os.getcwd()) + r'\flaskr\static\img\randomProfile\3.jpg'
    with open(pic2, 'rb') as jpg:
        client.post('/upload_pic', data=dict(file=jpg),
                    content_type='multipart/form-data', follow_redirects=True)
    rv = client.get('/profile')
    assert b'user_pic_3.jpg' in rv.data


def test_upload_no_file(client):
    client.post('/login', data=dict(username="delete_test", psw="Hello*1234"))
    rv = client.post('/upload_pic', data=dict(hey="hey"),
                     content_type='multipart/form-data', follow_redirects=True)
    assert b'No file part' in rv.data


def test_upload_not_valid_file(client):
    client.post('/login', data=dict(username="delete_test", psw="Hello*1234"))
    pic = str(os.getcwd()) + r'\flaskr\test.txt'
    with open(pic, 'rb') as jpg:
        rv = client.post('/upload_pic', data=dict(file=jpg),
                         content_type='multipart/form-data', follow_redirects=True)
    assert b'Not allowed file type' in rv.data


def test_random_pic(client):
    client.post('/login', data=dict(username="delete_test", psw="Hello*1234"))
    rv = client.post('random_pic', follow_redirects=True)
    assert b'1.jpg' not in rv.data


def test_random_pic_pre_upload(client):
    client.post('/login', data=dict(username="delete_test", psw="Hello*1234"))
    pic = str(os.getcwd()) + r'\flaskr\static\img\randomProfile\3.jpg'
    with open(pic, 'rb') as jpg:
        client.post('/upload_pic', data=dict(file=jpg),
                    content_type='multipart/form-data', follow_redirects=True)
    rv = client.post('random_pic', follow_redirects=True)
    assert b'3.jpg' not in rv.data


def test_random_pic_multi(client):
    client.post('/login', data=dict(username="delete_test", psw="Hello*1234"))
    client.post('/random_pic', follow_redirects=True)
    temp = User.query.filter_by(user_name="delete_test").first().user_pic
    client.post('/random_pic', follow_redirects=True)
    temp2 = User.query.filter_by(user_name="delete_test").first().user_pic
    assert temp != temp2


def test_delete_wrong_password(client):
    client.post('/login', data=dict(username="delete_test", psw="Hello*1234"))
    rv = client.post('/delete_account', data=dict(delete_psw='Good*1234'),
                     follow_redirects=True)
    assert b'Current password incorrect' in rv.data


def test_delete_with_upload_pic(client):
    client.post('/login', data=dict(username="delete_test", psw="Hello*1234"))
    pic = str(os.getcwd()) + r'\flaskr\static\img\randomProfile\4.jpg'
    with open(pic, 'rb') as jpg:
        client.post('/upload_pic', data=dict(file=jpg),
                    content_type='multipart/form-data', follow_redirects=True)
    user_id = User.query.filter_by(user_name="delete_test").first().id
    client.post('/addJq', data=dict(toDoItem='delete_todo_test'))
    client.post('/addJq', data=dict(toDoItem='delete_todo_test2'))
    client.post('/addJq', data=dict(toDoItem='delete_todo_test3'))
    rv = client.post('/delete_account', data=dict(delete_psw='Hello*1234'), follow_redirects=True)
    assert b'bye' in rv.data
    assert UsersToDo.query.filter_by(user_id=user_id).all() == []
    assert User.query.filter_by(user_name="delete_test").first() is None


def test_delete_random_pic(client):
    client.post('/login', data=dict(username="delete_test", psw="Hello*1234"))
    user_id = User.query.filter_by(user_name="delete_test").first().id
    rv = client.post('/delete_account', data=dict(delete_psw='Hello*1234'), follow_redirects=True)
    assert b'bye' in rv.data
    assert UsersToDo.query.filter_by(user_id=user_id).all() == []
    assert User.query.filter_by(user_name="delete_test").first() is None

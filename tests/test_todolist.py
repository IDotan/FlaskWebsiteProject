__author__ = "Itai Dotan"

note_1 = None
note_2 = None


def test_not_logged(client):
    rv = client.get('/toDoList')
    assert b'Todo List' in rv.data


def test_logged(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.get('/toDoList')
    assert b'Todo List' in rv.data


# add tests
def test_not_logged_add(client):
    rv = client.post('/addJq', data=dict(note="hey"))
    assert b'reload' in rv.data


def test_logged_add_empty(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.post('/addJq', data=dict(toDoItem=" "))
    assert b'nope' in rv.data


def test_logged_add_too_long(client):
    long_str = 'test test test test test test test test test test test ' \
               'test test test test test test test test test test'
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.post('/addJq', data=dict(toDoItem=long_str))
    assert b'reload' in rv.data


def test_logged_add_100(client):
    long_str = 'test test test test test test test test test test test test test test test test test test test tests'
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.post('/addJq', data=dict(toDoItem=long_str))
    global note_1
    temp_sting = str(rv.data)
    note_1 = temp_sting[-5]
    assert b'yep' in rv.data
    assert b'test test test test test test test test test test test ' \
           b'test test test test test test test test tests' in rv.data


def test_logged_add_hey(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.post('/addJq', data=dict(toDoItem='hey'))
    global note_2
    temp_sting = str(rv.data)
    note_2 = temp_sting[-5]
    assert b'yep' in rv.data
    assert b'hey' in rv.data


def test_logged_added_showing(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.get('/toDoList')
    assert b'hey' in rv.data
    assert b'test test test test test test test test test test test ' \
           b'test test test test test test test test tests' in rv.data


# complete tests
def test_not_logged_complete(client):
    rv = client.post('/completeJQ', data=dict(note_id=note_2))
    assert b'reload' in rv.data


def test_wrong_user_complete(client):
    client.post('/login', data=dict(username="admin", psw="Hello*1234"))
    rv = client.post('/completeJQ', data=dict(note_id=note_2, note_text='hey'))
    assert b'nope' in rv.data


def test_logged_complete(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.get('/toDoList')
    assert b'class=\'not-marked\'' in rv.data
    rv = client.post('/completeJQ', data=dict(note_id=note_2, note_text="hey"))
    assert b'yep' in rv.data
    rv = client.get('/toDoList')
    assert b'class=\'marked\'' in rv.data


def test_logged_uncomplete(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.get('/toDoList')
    assert b'class=\'marked\'' in rv.data
    rv = client.post('/completeJQ', data=dict(note_id=note_2, note_text='hey'))
    assert b'yep' in rv.data
    rv = client.get('/toDoList')
    assert b'class=\'marked\'' not in rv.data


# delete tests
def test_not_logged_delete(client):
    rv = client.post('/deleteJQ', data=dict(note_id=note_1))
    assert b'reload' in rv.data


def test_wrong_user_delete(client):
    client.post('/login', data=dict(username="admin", psw="Hello*1234"))
    rv = client.post('/deleteJQ', data=dict(note_id=note_2, note_text='hey'))
    assert b'nope' in rv.data


def test_logged_delete(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    long_str = 'test test test test test test test test test test test test test test test test test test test tests'
    rv = client.post('/deleteJQ', data=dict(note_id=note_1, note_text=long_str))
    assert b'yep' in rv.data
    rv = client.get('/toDoList')
    assert b'test test test test test test test test test test test ' \
           b'test test test test test test test test tests' not in rv.data


def test_logged_delete_hey_wrong_text(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.post('/deleteJQ', data=dict(note_id=note_2, note_text="bye"))
    assert b'nope' in rv.data
    rv = client.get('/toDoList')
    assert b'hey' in rv.data


def test_logged_delete_hey(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"))
    rv = client.post('/deleteJQ', data=dict(note_id=note_2, note_text="hey"))
    assert b'yep' in rv.data
    rv = client.get('/toDoList')
    assert b'hey' not in rv.data

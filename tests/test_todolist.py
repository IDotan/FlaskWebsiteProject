def test_not_logged(client):
    rv = client.get('/toDoList')
    assert b'Todo List' in rv.data


def test_logged(client):
    client.post('/login', data=dict(username="itai2", psw="Hello*1234"), follow_redirects=True)
    rv = client.get('/toDoList')
    assert b'Todo List' in rv.data

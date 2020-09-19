import os
import pytest
import shutil
from flaskr import create_app

__author__ = "Itai Dotan"


def pytest_sessionstart():
    shutil.copy(r"./flaskr/test.db", r"./flaskr/test_this.db")
    if os.path.exists('email.ini'):
        os.rename('email.ini', 'email_bck.ini')


def pytest_sessionfinish():
    os.remove(r"./flaskr/test_this.db")
    if os.path.exists('email.ini'):
        os.remove('email.ini')
    if os.path.exists('email_bck.ini'):
        os.rename('email_bck.ini', 'email.ini')


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_this.db'
    app.config['SQLALCHEMY_BINDS'] = {'UsersToDo': 'sqlite:///test_toDo.db'}
    with app.test_client() as client:
        app.teardown_request
        yield client


@pytest.fixture
def client(app):
    return app

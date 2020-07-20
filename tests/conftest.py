import os
import pytest
import shutil
from flaskr import create_app

__author__ = "Itai Dotan"


@pytest.fixture
def app():
    os.rename(r"./flaskr/users.db", r"./flaskr/back.db")
    shutil.copy(r"./flaskr/test.db", r"./flaskr/users.db")

    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        app.teardown_request
        yield client

    os.remove(r"./flaskr/users.db")
    os.rename(r"./flaskr/back.db", r"./flaskr/users.db")


@pytest.fixture
def client(app):
    return app


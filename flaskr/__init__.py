from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__author__ = "Itai Dotan"

users_db = SQLAlchemy()
toDoList_db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = b'jd*gtjh#58idty7'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_BINDS'] = {'UsersToDo': 'sqlite:///users_toDo.db'}
    users_db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .todolist import toDoList as toDoList_blueprint
    app.register_blueprint(toDoList_blueprint)

    from .profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    return app

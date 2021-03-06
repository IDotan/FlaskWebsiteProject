"""
| set up the sql data base
"""
from . import users_db, toDoList_db

__author__ = "Itai Dotan"


class User(users_db.Model):
    """
    | set the column for users_db
    """
    id = users_db.Column(users_db.Integer, primary_key=True)
    email = users_db.Column(users_db.String(100), unique=True)
    user_name = users_db.Column(users_db.String(100), unique=True)
    password = users_db.Column(users_db.String(100))
    first_name = users_db.Column(users_db.String(30))
    last_name = users_db.Column(users_db.String(30))
    gender = users_db.Column(users_db.Integer)  # 1.Male 2.Female
    psw_reset = users_db.Column(users_db.String(10))
    psw_reset_time = users_db.Column(users_db.Integer)
    user_pic = users_db.Column(users_db.String(100))
    user_pic_name = users_db.Column(users_db.String(100))


class UsersToDo(toDoList_db.Model):
    """
    | set the column for toDoList_db
    """
    __bind_key__ = 'UsersToDo'
    id = toDoList_db.Column(toDoList_db.Integer, primary_key=True)
    user_id = toDoList_db.Column(toDoList_db.Integer)
    text = toDoList_db.Column(toDoList_db.String(100))
    complete = toDoList_db.Column(toDoList_db.Boolean)

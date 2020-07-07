from . import users_db

__author__ = "Itai Dotan"


class User(users_db.Model):
    id = users_db.Column(users_db.Integer, primary_key=True)
    email = users_db.Column(users_db.String(100), unique=True)
    user_name = users_db.Column(users_db.String(100), unique=True)
    password = users_db.Column(users_db.String(100))
    first_name = users_db.Column(users_db.String(1000))
    last_name = users_db.Column(users_db.String(1000))
    gender = users_db.Column(users_db.Integer)  # 1.Male 2.Female
    psw_reset = users_db.Column(users_db.String(1000))
    psw_reset_time = users_db.Column(users_db.Integer)


from flask import Blueprint, render_template, g
from .auth import check_session

__author__ = "Itai Dotan"

main = Blueprint('main', __name__)


@main.route('/')
@check_session
def index():
    name = ""
    if g.user is not None:
        name = g.user.first_name
    return render_template('home.html', name=name)


@main.route('/new_friend')
def new_friend():
    return render_template('new_friend.html')
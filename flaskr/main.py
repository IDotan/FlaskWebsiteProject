from flask import Blueprint, render_template, g, url_for
from .auth import check_session, login_required

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
@check_session
@login_required
def new_friend():
    pic = g.user.user_pic
    name = g.user.first_name
    return render_template('new_friend.html', profile_pic=pic, name=name)

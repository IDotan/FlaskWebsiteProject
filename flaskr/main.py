from flask import Blueprint, render_template, g
from .auth import check_session, login_required

__author__ = "Itai Dotan"

main = Blueprint('main', __name__)


@main.route('/')
@check_session
def index():
    """
    | render the home page
    :return: render template 'home.html' with name value of the user
    """
    name = ""
    if g.user is not None:
        name = g.user.first_name
    return render_template('home.html', name=name)


@main.route('/new_friend')
@check_session
@login_required
def new_friend():
    """
    | render the new friend page
    :return: render template 'home.html' with the user name and pic as values
    """
    pic = g.user.user_pic
    name = g.user.first_name
    return render_template('new_friend.html', profile_pic=pic, name=name)


@main.route('/about')
@check_session
def about():
    name = ""
    if g.user is not None:
        name = g.user.first_name
    return render_template('about.html', name=name)

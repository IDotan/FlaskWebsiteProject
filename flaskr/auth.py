"""
| model for the site user login and register functions
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, g
from functools import wraps
from . import users_db
from flaskr.python_scripts.register_validator import check_form_data, valid_user, valid_email, valid_psw
from .models import User
from passlib.hash import sha256_crypt
from flaskr.python_scripts.random_pic_picker import pick_my_pic
from flaskr.python_scripts.send_reset_code import psw_reset_setup
from os import path
from time import time

__author__ = "Itai Dotan"

auth = Blueprint('auth', __name__)


def check_session(f):
    """
    | check if there is a logged in user
    :return: g.user = user data when logged or none when not logged
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.user = None
        if "id" in session:
            g.user = User.query.filter_by(id=session["id"]).first()
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    """
    | make sure the user is logged to use the page
    | send to log in when not logged in
    :return: the requested page when logged, redirect to login page when not logged
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            g.user.id
            return f(*args, **kwargs)
        except AttributeError:
            return redirect(url_for("auth.login"))
    return decorated_function


@auth.route('/login')
def login():
    """
    | render login.html
    :return: render template login.html
    """
    if path.exists('email.ini'):
        reset = True
    else:
        reset = False
    return render_template('login.html', reset=reset)


@auth.route('/login', methods=['POST'])
def login_post():
    """
    | check login request
    :return: redirect to 'main.index' when login was complete or render the page with error msg
    """
    user_name = request.form['username']
    psw = request.form['psw']
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(user_name=user_name).first()
    if user:
        if sha256_crypt.verify(psw, user.password):
            session["id"] = user.id
            if remember:
                session.permanent = True
            g.user = user
            return redirect(url_for("main.index"))
    return render_template('login.html', error="Wrong login information")


@auth.route('/passwordRest')
def password_reset():
    """
    | render password_reset.html
    :return: render template 'password_reset.html'
    """
    if path.exists('email.ini'):
        return render_template('password_reset.html')
    return redirect(url_for('auth.login'))


@auth.route('/passwordRest', methods=['POST'])
def password_reset_send():
    if path.exists('email.ini'):
        mail = request.form['email']
        user = User.query.filter_by(email=mail).first()
        if not user:
            error = 'This E-mail is not registered'
            return render_template('password_reset.html', error=error)
        else:
            psw_reset_setup(user)
            return render_template('password_reset.html', sent='yep', sent_to=mail)
    return redirect(url_for('auth.login'))


@auth.route('/passwordRest/<userinfo>')
def password_reset_2nd_phase(userinfo):
    temp = userinfo.split('$')
    check_id = temp[0]
    check_link = temp[1]
    user = User.query.filter_by(id=check_id).first()
    if user:
        if str(user.psw_reset_time)[::2] == check_link and time() < user.psw_reset_time:
            return render_template('password_reset_2nd_phase.html', phase='code')
    flash("Invalid link or link timed out")
    return redirect(url_for('auth.password_reset_send'))


@auth.route('/passwordRest/<userinfo>', methods=['POST'])
def password_reset_2nd_phase_code_post(userinfo):
    given_user = userinfo.split('$')[0]
    try:
        reset_code = request.form['code']
    except:
        reset_code = None
    user = User.query.filter_by(id=given_user).first()
    if user.psw_reset_time < time():
        flash("Invalid link or link timed out")
        return redirect(url_for('auth.password_reset_send'))
    if reset_code:
        if reset_code == user.psw_reset:
            user.psw_reset = 123
            # set the user open to password change for 5 min
            user.psw_reset_time = int(time() + 300)
            users_db.session.commit()
            return render_template('password_reset_2nd_phase.html', phase='psw')
        else:
            error = "Incorrect reset code"
            return render_template('password_reset_2nd_phase.html', phase='code', error=error)
    else:
        psw = request.form['psw']
        re_psw = request.form['repsw']
        if psw != re_psw:
            error = "Reentered password don't match"
            return render_template('password_reset_2nd_phase.html', phase='psw', error=error)
        if not valid_psw(psw):
            error = "Invalid password, enable site script for more info"
            return render_template('password_reset_2nd_phase.html', phase='psw', error=error)
        if user.psw_reset == str(123):
            user.password = sha256_crypt.hash(psw)
            user.psw_reset_time, user.psw_reset == ''
            users_db.session.commit()
            return redirect(url_for('auth.password_was_changed'))
        else:
            flash("Invalid link or link timed out")
            return redirect(url_for('auth.password_reset_send'))


@auth.route('/passwordChanged')
def password_was_changed():
    return render_template('password_was_changed.html')


@auth.route('/register')
def signup():
    """
    | render register.html
    :return: render template 'register.html'
    """
    return render_template('register.html')


@auth.route('/register', methods=['POST'])
def signup_post():
    """
    | check the form data and create new user in the database when valid
    | make sure all the data is valid and make sure the user ID and the E-mail is unique
    :return: redirect to 'main.new_friend' when registration was complete,
            render the page with flash msg when there is an error
    """
    user_name = request.form['username']
    psw = request.form['psw']
    mail = request.form['email']
    f_name = request.form['fname']
    l_name = request.form['lname']
    gender = request.form['gender']

    if not check_form_data(user_name, psw, mail, f_name, l_name, gender):
        flash('one or more of your info is invalid.')
        flash('please enable site scripts to be shown more info.')
        return render_template('register.html')
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        flash('User name already exists.')
        return render_template('register.html')
    email = User.query.filter_by(email=mail).first()
    if email:
        flash('Email address already in use.')
        return render_template('register.html')

    new_user = User(user_name=user_name, password=sha256_crypt.hash(psw), email=mail, first_name=f_name,
                    last_name=l_name, gender=gender, user_pic=pick_my_pic())
    users_db.session.add(new_user)
    users_db.session.commit()

    new_user_session = User.query.filter_by(user_name=user_name).first()
    session["id"] = new_user_session.id
    g.user = new_user_session
    return redirect(url_for('main.new_friend'))


@auth.route('/userIDAvailable', methods=['POST'])
def user_id_available():
    """
    | check if the user id is available before the form POST of the register page
    | the checks before the SQL query is to prevent unneeded scan of the database
    :return: dict with data response of the result
    """
    id_to_check = request.form['usernameCheck']
    if len(id_to_check) < 5:
        return {'valid': 'no'}
    if not valid_user(id_to_check):
        return {'valid': 'no'}
    if User.query.filter_by(user_name=id_to_check).first():
        return {'valid': 'no'}
    return {'valid': 'yes'}


@auth.route('/emailAvailable', methods=['POST'])
def email_available():
    """
    | check if the E-mail is available before the form POST of the register page
    | the check before the SQL query is to prevent unneeded scan of the database
    :return: dict with data response of the result
    """
    mail_to_check = request.form['emailCheck']
    if not valid_email(mail_to_check):
        return {'valid': 'no'}
    if User.query.filter_by(email=mail_to_check).first():
        return {'valid': 'no'}
    return {'valid': 'yes'}


@auth.route('/logout')
def logout():
    """
    | log out the user from the site
    :return: redirect to '/' (home page)
    """
    session.pop("id", None)
    g.user = None
    return redirect("/")

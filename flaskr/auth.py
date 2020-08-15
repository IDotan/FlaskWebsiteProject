from flask import Blueprint, render_template, redirect, url_for, request, flash, session, g
from functools import wraps
from . import users_db
from flaskr.python_scripts.register_validator import check_form_data, valid_user, valid_email
from .models import User
from passlib.hash import sha256_crypt
from flaskr.python_scripts.random_pic_picker import pick_my_pic


__author__ = "Itai Dotan"

auth = Blueprint('auth', __name__)


def check_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.user = None
        if "id" in session:
            g.user = User.query.filter_by(id=session["id"]).first()
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
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
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
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


@auth.route('/register')
def signup():
    return render_template('register.html')


@auth.route('/register', methods=['POST'])
def signup_post():
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
    # :todo new friend css and java script to go to home
    return redirect(url_for('main.new_friend'))


@auth.route('/userIDAvailable', methods=['POST'])
def user_id_available():
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
    mail_to_check = request.form['emailCheck']
    if not valid_email(mail_to_check):
        return {'valid': 'no'}
    if User.query.filter_by(email=mail_to_check).first():
        return {'valid': 'no'}
    return {'valid': 'yes'}


@auth.route('/logout')
def logout():
    session.pop("id", None)
    g.user = None
    return redirect("/")

from flask import Blueprint, render_template, redirect, url_for, request, flash, session, g
from functools import wraps
from . import users_db
from flaskr.python_scripts.register_validater import check_form_data
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

    if not check_form_data(user_name, psw,):
        flash('one or more of the following, are not allowed:')
        flash('Username, password or email')
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


@auth.route('/logout')
def logout():
    session.pop("id", None)
    g.user = None
    return redirect("/")

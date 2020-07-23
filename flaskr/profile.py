from flask import Blueprint, render_template, request, g, flash, session, redirect, url_for, Flask
from .auth import check_session, login_required
from passlib.hash import sha256_crypt
from . import users_db, toDoList_db
from .models import User, UsersToDo
from .python_scripts.register_validator import valid_psw
import os
from werkzeug.utils import secure_filename

__author__ = "Itai Dotan"

profile = Blueprint('profile', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = str(os.getcwd()) + r'\flaskr\static\img\user_pic'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@profile.route('/profile')
@check_session
@login_required
def profile_page():
    pic = g.user.user_pic
    name = g.user.first_name.capitalize() + ' ' + g.user.last_name.capitalize()
    return render_template('profile.html', profile_pic=pic, name=name)


@profile.route('/psw_change', methods=['POST'])
@check_session
def profile_psw_change():
    old_psw = request.form['old_psw']
    new_psw = request.form['new_psw']
    confirm_psw = request.form['confirm_psw']
    if not sha256_crypt.verify(old_psw, g.user.password):
        flash('Current password incorrect', 'change')
        return redirect(url_for("profile.profile_page"))
    if old_psw == new_psw:
        flash('New password can\'t be the same as the old password', 'change')
        return redirect(url_for("profile.profile_page"))
    if not valid_psw(new_psw):
        flash('New password is invalid', 'change')
        return redirect(url_for("profile.profile_page"))
    if new_psw != confirm_psw:
        flash('Current password don\'t match the confirm password', 'change')
        return redirect(url_for("profile.profile_page"))
    user = User.query.filter_by(id=g.user.id).first()
    user.password = sha256_crypt.hash(new_psw)
    users_db.session.commit()
    flash('Your password was changed', 'change')
    return redirect(url_for("profile.profile_page"))


@profile.route('/delete_account', methods=['POST'])
@check_session
@login_required
def delete_account():
    user_id = g.user.id
    psw = request.form['delete_psw']
    if not sha256_crypt.verify(psw, g.user.password):
        flash('Current password incorrect', 'delete')
        return redirect(url_for("profile.profile_page"))
    # delete user data
    user = User.query.filter_by(id=user_id).first()
    users_db.session.delete(user)
    users_db.session.commit()
    todo = UsersToDo.query.filter_by(user_id=user_id).all()
    for note in todo:
        toDoList_db.session.delete(note)
    toDoList_db.session.commit()
    # log out
    session.pop("id", None)
    g.user = None
    return '<h1>bye</h1>'


@profile.route('/upload_pic', methods=['POST'])
@check_session
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'upload')
        return redirect(url_for("profile.profile_page"))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for("profile.profile_page"))
    if file and allowed_file(file.filename):
        # filename = str(g.user.id) + '_pic' + str(file.filename[-4:])
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user = User.query.filter_by(id=g.user.id).first()
        return redirect(url_for("profile.profile_page"))

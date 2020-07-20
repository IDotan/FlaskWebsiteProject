from flask import Blueprint, render_template, redirect, url_for, request, g, flash, session
from .auth import check_session, login_required
from passlib.hash import sha256_crypt
from . import users_db, toDoList_db
from .models import User, UsersToDo

__author__ = "Itai Dotan"

profile = Blueprint('profile', __name__)


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
        return profile_page()
    if old_psw == new_psw:
        flash('New password can\'t be the same as the old password', 'change')
        return profile_page()
    if new_psw != confirm_psw:
        flash('Current password don\'t match the confirm password', 'change')
        return profile_page()
    user = User.query.filter_by(id=g.user.id).first()
    user.password = sha256_crypt.hash(new_psw)
    users_db.session.commit()
    flash('Your password was changed', 'change')
    return profile_page()


@profile.route('/delete_account', methods=['POST'])
@check_session
@login_required
def delete_account():
    user_id = g.user.id
    psw = request.form['delete_psw']
    if not sha256_crypt.verify(psw, g.user.password):
        flash('Current password incorrect', 'delete')
        return profile_page()
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

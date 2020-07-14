from flask import Blueprint, render_template, url_for, request, redirect, g, session, jsonify
from .models import UsersToDo
from . import toDoList_db
from .auth import check_session

__author__ = "Itai Dotan"

toDoList = Blueprint('toDoList', __name__)


@toDoList.route('/toDoList')
def to_do_list():
    try:
        user_id = session["id"]
        list_items = UsersToDo.query.filter_by(user_id=user_id).all()
    except KeyError:
        user_id = None
        list_items = []
    return render_template('toDoList.html', list_itemss=list_items, user_id=user_id)


@toDoList.route('/addJq', methods=['POST'])
@check_session
def add_jq():
    note = request.form['toDoItem']
    todo = UsersToDo(text=note, user_id=g.user.id, complete=False)
    toDoList_db.session.add(todo)
    toDoList_db.session.commit()
    note_id = todo.id
    return jsonify({'note': note, 'note_id': note_id})


@toDoList.route('/deleteJQ', methods=['POST'])
def delete_jp():
    note_id = request.form['note_id']
    note_text = request.form['note_text'].strip()
    note = UsersToDo.query.filter_by(id=int(note_id)).first()
    done = 'nope'
    if note.text == note_text:
        UsersToDo.query.filter_by(id=int(note_id)).delete()
        toDoList_db.session.commit()
        done = 'yep'
    return jsonify({'done': done})


@toDoList.route('/complete/<note_id>')
def complete(note_id):
    todo = UsersToDo.query.filter_by(id=int(note_id)).first()
    todo.complete = True
    toDoList_db.session.commit()

    return redirect(url_for('toDoList.to_do_list'))


@toDoList.route('/delete/<note_id>')
def delete(note_id):
    UsersToDo.query.filter_by(id=int(note_id)).delete()
    toDoList_db.session.commit()

    return redirect(url_for('toDoList.to_do_list'))

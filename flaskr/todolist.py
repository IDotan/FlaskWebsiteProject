from flask import Blueprint, render_template, request, g, session, jsonify
from .models import UsersToDo
from . import toDoList_db
from .auth import check_session

__author__ = "Itai Dotan"

toDoList = Blueprint('toDoList', __name__)


@toDoList.route('/toDoList')
@check_session
def to_do_list():
    try:
        user_id = session["id"]
        list_items = UsersToDo.query.filter_by(user_id=user_id).all()
        name = g.user.first_name
    except KeyError:
        user_id = None
        list_items = []
        name = ""
    return render_template('toDoList.html', list_itemss=list_items, user_id=user_id, name=name)


@toDoList.route('/addJq', methods=['POST'])
@check_session
def add_jq():
    if g.user is None:
        return {'done': "reload"}
    note = request.form['toDoItem'].strip()
    if note == "":
        return {'done': "nope"}
    if len(note) > 100:
        return {'done': "reload"}
    todo = UsersToDo(text=note, user_id=g.user.id, complete=False)
    toDoList_db.session.add(todo)
    toDoList_db.session.commit()
    note_id = todo.id
    return jsonify({'note': note, 'note_id': note_id, 'done': "yep"})


@toDoList.route('/deleteJQ', methods=['POST'])
@check_session
def delete_jp():
    if g.user is None:
        return {'done': "reload"}
    user_id_session = g.user.id
    note_id = request.form['note_id']
    note_text = request.form['note_text'].strip()
    note = UsersToDo.query.filter_by(id=int(note_id)).first()
    done = 'nope'
    if note.user_id == user_id_session and note_text == note.text:
        UsersToDo.query.filter_by(id=int(note_id)).delete()
        toDoList_db.session.commit()
        done = 'yep'
    return jsonify({'done': done, 'note_id': note_id})


@toDoList.route('/completeJQ', methods=['POST'])
@check_session
def complete_jq():
    if g.user is None:
        return {'done': "reload"}
    user_id_session = g.user.id
    note_id = request.form['note_id']
    note_text = request.form['note_text'].strip()
    note = UsersToDo.query.filter_by(id=int(note_id)).first()
    done = 'nope'
    if note.user_id == user_id_session and note_text == note.text:
        if note.complete is False:
            note.complete = True
        else:
            note.complete = False
        toDoList_db.session.commit()
        done = 'yep'
    return jsonify({'done': done, 'note_id': note_id})

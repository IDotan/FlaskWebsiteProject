from flask import Blueprint, render_template, url_for, request, redirect
from .models import UsersToDo
from . import toDoList_db

__author__ = "Itai Dotan"

toDoList = Blueprint('toDoList', __name__)


@toDoList.route('/toDoList')
def to_do_list():
    not_marked = UsersToDo.query.filter_by(complete=False).all()
    marked = UsersToDo.query.filter_by(complete=True).all()
    return render_template('toDoList.html', incomplete=not_marked, complete=marked)


@toDoList.route('/add', methods=['POST'])
def add():
    todo = UsersToDo(text=request.form['todoitem'], complete=False)
    toDoList_db.session.add(todo)
    toDoList_db.session.commit()

    return redirect(url_for('toDoList.to_do_list'))


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

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Task
from . import db

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    todo_tasks = Task.query.filter_by(status='todo', user_id=current_user.id).all()
    done_tasks = Task.query.filter_by(status='done', user_id=current_user.id).all()
    return render_template('index.html', todo_tasks=todo_tasks, done_tasks=done_tasks)

@main.route('/add', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title')
    new_task = Task(title=title, status='todo', user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/complete/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.query.get(task_id)
    task.status = 'done'
    db.session.commit()
    return redirect(url_for('main.index'))
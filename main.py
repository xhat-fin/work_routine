import db
import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)


################
# path_manager #
################


@app.route("/", methods=["GET", "POST"])
def path_manager():
    if request.method == "POST":
        path = request.form.get('path')
        description = request.form.get('description')
        if path:
            db.insert_path(path, description)
            return redirect(url_for('path_manager'))

    paths = db.select_all_path()
    return render_template('path.html', paths=paths)


@app.route('/start-path/<path:file_path>', methods=["GET"])
def start_path(file_path):
    if not file_path or '..' in file_path:
        return "Invalid path", 400

    safe_path = file_path.replace('/', '\\')

    if os.path.exists(safe_path):
        try:
            os.startfile(safe_path)
            return redirect(url_for('path_manager'))
        except Exception as e:
            return f"Error opening path: {str(e)}", 500
    else:
        return "Path not found", 404


@app.route('/delete-path/<int:path_id>', methods=["GET"])
def delete_path(path_id):
    db.delete_path(path_id)
    return redirect(url_for('path_manager'))


################
# task_manager #
################


@app.route("/tasks", methods=["GET", "POST"])
def task_manager():
    if request.method == "POST":
        task = request.form.get('task')
        description = request.form.get('description')
        type_task = request.form.get('type')
        if task:
            db.create_task(task, description, type_task)
            return redirect(url_for('task_manager'))

    tasks = db.select_task()
    list_type_task = ['Автоматизация', 'Аналитика', 'Лидогенерация']
    status_list = ['Создана', 'В работе', 'Стоп', 'Завершена']
    return render_template('tasks.html', tasks=tasks,
                           list_type_task=list_type_task,
                           status_list=status_list,
                           active_module='tasks')


@app.route("/edit-task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    old_task = db.select_task_id(task_id)
    if request.method == "POST":
        task = request.form.get('task')
        description = request.form.get('description')
        type_task = request.form.get('type')
        status = request.form.get('status')

        if task:
            if not old_task['start_date'] and status == 'В работе':
                with db.sql.connect('db.sqlite3') as conn:
                    cur = conn.cursor()

                    cur.execute(
                        """
                        UPDATE tasks 
                        SET start_date = ?
                        WHERE id = ?
                        """, (datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), task_id)
                    )
                    conn.commit()

            if not old_task['end_date'] and status == 'Завершена':
                with db.sql.connect('db.sqlite3') as conn:
                    cur = conn.cursor()

                    cur.execute(
                        """
                        UPDATE tasks 
                        SET end_date = ?
                        WHERE id = ?
                        """, (datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), task_id)
                    )
                    conn.commit()

            db.update_task(task_id, task, description, type_task, status)
            return redirect(url_for('task_manager'))

    list_type_task = ['Автоматизация', 'Аналитика', 'Лидогенерация']
    status_list = ['Создана', 'В работе', 'Стоп', 'Завершена']

    return render_template('edit_task.html',
                           task=old_task,
                           list_type_task=list_type_task,
                           status_list=status_list,
                           active_module='tasks')


@app.route("/delete-task/<int:task_id>", methods=["GET"])
def delete_task(task_id):
    db.delete_task(task_id)
    return redirect(url_for('task_manager'))


############################
# модуль рабочих сценариев #
############################


if __name__ == "__main__":
    db.init_db()
    app.run(port=8000, debug=True)
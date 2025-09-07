import sqlite3 as sql


def init_db():
    with sql.connect('db.sqlite3') as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS path_manager(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT,
            description TEXT 
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            description TEXT,
            type TEXT,
            status TEXT DEFAULT 'Создана',
            start_date TEXT,
            end_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.commit()
        return {"message": "bd is create or start"}


################
# path_manager #
################


def select_all_path():
    with sql.connect('db.sqlite3') as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, path, description FROM path_manager
            """
        )
        paths = cur.fetchall()

    db_response = []
    for path in paths:
        db_response.append(
            {
                "id": path[0],
                "path": path[1],
                "description": path[2],
            }
        )

    return db_response


def insert_path(path, description):
    with sql.connect('db.sqlite3') as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO path_manager(path, description) VALUES (?, ?)
            """, (path, description)
        )
        conn.commit()
    return {"message": f"{path} успешно добавлен в БД"}


def delete_path(path_id):
    with sql.connect('db.sqlite3') as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM path_manager WHERE id = ?", (path_id,))
        conn.commit()
    return {"message": f"Path {path_id} deleted"}


################
# task_manager #
################


def create_task(task, description, type_task):
    with sql.connect('db.sqlite3') as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO tasks(task, description, type) 
            VALUES (?, ?, ?)
            """, (task, description, type_task)
        )
        conn.commit()
    return {"message": "Задача создана"}


def select_task():
    with sql.connect('db.sqlite3') as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, task, description, type, status, start_date, end_date 
            FROM tasks ORDER BY created_at DESC
            """
        )
        tasks = cur.fetchall()

    db_response = []
    for task in tasks:
        db_response.append(
            {
                "id": task[0],
                "task": task[1],
                "description": task[2],
                "type": task[3],
                "status": task[4],
                "start_date": task[5],
                "end_date": task[6],
            }
        )
    return db_response


def select_task_id(task_id):
    with sql.connect('db.sqlite3') as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, task, description, type, status, start_date, end_date 
            FROM tasks WHERE id = ?
            """, (task_id, )
        )
        task = cur.fetchone()

        response = {
            "id": task[0],
            "task": task[1],
            "description": task[2],
            "type": task[3],
            "status": task[4],
            "start_date": task[5],
            "end_date": task[6],
        }
    return response


def update_task(task_id, task, description, type_task, status):
    with sql.connect('db.sqlite3') as conn:
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE tasks 
            SET task = ?, description = ?, type = ?, status = ?
            WHERE id = ?
            """, (task, description, type_task, status, task_id)
        )
        conn.commit()
    return {"message": "Задача обновлена"}


def delete_task(task_id):
    with sql.connect('db.sqlite3') as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    return {"message": "Задача удалена"}

from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "secret123"


def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn


# CREATE TABLES
conn = get_db()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    task TEXT,
    progress INTEGER DEFAULT 0,
    due_date TEXT
)
""")

conn.commit()
conn.close()


# HOME
@app.route('/', methods=['GET', 'POST'])
def home():
    if "username" not in session:
        return redirect('/login')

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        task = request.form.get("task")
        try:
            progress = int(request.form.get("progress") or 0)
        except ValueError:
            progress = 0
        due_date = request.form.get("due_date")

        cursor.execute(
            "INSERT INTO tasks (username, task, progress, due_date) VALUES (?, ?, ?, ?)",
            (session["username"], task, progress, due_date)
        )
        conn.commit()

    cursor.execute("SELECT * FROM tasks WHERE username=?", (session["username"],))
    tasks = cursor.fetchall()

    total = len(tasks)
    percent = int(sum([t["progress"] for t in tasks]) / total) if total > 0 else 0

    today = date.today().isoformat()

    conn.close()

    return render_template("index.html", tasks=tasks, username=session["username"], percent=percent, today=today)


# COMPLETE
@app.route('/complete/<int:id>')
def complete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET progress=100 WHERE id=? AND username=?", (id, session["username"]))
    conn.commit()
    conn.close()
    return redirect('/')


# DELETE
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=? AND username=?", (id, session["username"]))
    conn.commit()
    conn.close()
    return redirect('/')


# EDIT
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id=? AND username=?", (id, session["username"]))
    task = cursor.fetchone()

    if not task:
        conn.close()
        return redirect('/')

    if request.method == "POST":
        new_task = request.form.get("task")
        try:
            progress = int(request.form.get("progress") or 0)
        except ValueError:
            progress = 0
        due_date = request.form.get("due_date")

        cursor.execute("""
            UPDATE tasks
            SET task=?, progress=?, due_date=?
            WHERE id=? AND username=?
        """, (new_task, progress, due_date, id, session["username"]))

        conn.commit()
        conn.close()
        return redirect('/')

    conn.close()
    return render_template("edit.html", task=task)


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect('/login')
        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists"

    return render_template("register.html")


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"] = username
            return redirect('/')
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)
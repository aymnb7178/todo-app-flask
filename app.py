import os
import sqlite3
import uuid

from flask import Flask, g, render_template, request, redirect, url_for

SCHEMA = """
CREATE TABLE IF NOT EXISTS todos (
    id        TEXT PRIMARY KEY,
    task      TEXT NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0,
    created   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""
MAX_TASK_LENGTH = 300


def create_app(db_path=None):
    """Application factory. Tasks are stored in a SQLite file (TODO_DB, default todos.db)."""
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path or os.environ.get("TODO_DB", "todos.db")

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DB_PATH"])
            g.db.row_factory = sqlite3.Row
            g.db.execute(SCHEMA)
        return g.db

    @app.teardown_appcontext
    def close_db(_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @app.route("/")
    def index():
        rows = get_db().execute("SELECT id, task, completed FROM todos ORDER BY created, rowid").fetchall()
        todos = [{"id": r["id"], "task": r["task"], "completed": bool(r["completed"])} for r in rows]
        return render_template("index.html", todos=todos)

    @app.route("/add", methods=["POST"])
    def add_todo():
        task = (request.form.get("task") or "").strip()[:MAX_TASK_LENGTH]
        if task:
            db = get_db()
            db.execute("INSERT INTO todos (id, task) VALUES (?, ?)", (str(uuid.uuid4()), task))
            db.commit()
        return redirect(url_for("index"))

    @app.route("/complete/<todo_id>", methods=["POST"])
    def complete_todo(todo_id):
        db = get_db()
        db.execute("UPDATE todos SET completed = 1 - completed WHERE id = ?", (todo_id,))
        db.commit()
        return redirect(url_for("index"))

    @app.route("/delete/<todo_id>", methods=["POST"])
    def delete_todo(todo_id):
        db = get_db()
        db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        db.commit()
        return redirect(url_for("index"))

    return app


app = create_app()

if __name__ == "__main__":
    # Debug mode and network exposure are opt-in: the Werkzeug debugger must not
    # be reachable from other machines. Use FLASK_DEBUG=1 / FLASK_HOST=0.0.0.0
    # only on a trusted local network.
    app.run(
        debug=os.environ.get("FLASK_DEBUG") == "1",
        host=os.environ.get("FLASK_HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")),
    )

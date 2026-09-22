from flask import Flask, render_template, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "simulation.db"
def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def record_action(action):
    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "INSERT INTO responses (action, timestamp) VALUES (?, ?)",
        (action, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()


@app.route("/")
def email():
    return render_template("email.html")


@app.route("/clicked")
def clicked():
    record_action("Link clicked")
    return redirect("/awareness")


@app.route("/awareness")
def awareness():
    return render_template("awareness.html")


@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect(DATABASE)

    rows = conn.execute(
        "SELECT action, timestamp FROM responses ORDER BY id DESC"
    ).fetchall()

    conn.close()

    total = len(rows)

    return render_template(
        "dashboard.html",
        responses=rows,
        total=total
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
input("press enter to exit....")
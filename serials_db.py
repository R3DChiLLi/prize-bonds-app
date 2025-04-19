from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # Used for sessions

# MySQL config
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route("/", methods=["GET"])
def index():
    if "username" not in session:
        return render_template("index.html")

    table = request.args.get("table", "serials_1500")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, serial_start, serial_end, status FROM {table}")
    serials = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", serials=serials, table=table)


@app.route("/add-serial", methods=["POST"])
def add_serial():
    if "username" not in session:
        return redirect(url_for("index"))

    serial_start = request.form["serial_start"]
    serial_end = request.form["serial_end"]
    status = request.form.get("status", "").strip().lower()
    table = request.form["table"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO {table} (serial_start, serial_end, status)
        VALUES (%s, %s, %s)
    """, (serial_start, serial_end, status))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("index", table=table))


@app.route("/delete/<table>/<int:serial_id>", methods=["POST"])
def delete_serial(table, serial_id):
    if "username" not in session:
        return redirect(url_for("index"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE id = %s", (serial_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("index", table=table))


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result and result[0] == password:
        session["username"] = username
        return redirect(url_for("index"))
    else:
        return "Invalid username or password", 401


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

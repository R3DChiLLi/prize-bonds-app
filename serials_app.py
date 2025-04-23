from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # Used for sessions

# Configure logging
if not app.debug:
    # Set up console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    console_handler.setLevel(logging.INFO)
    app.logger.addHandler(console_handler)
    
    # Set up file handler with rotation
    log_dir = Path('/app/logs')
    try:
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / 'app.log'
        
        # Ensure the log file exists and is writable
        if not log_file.exists():
            log_file.touch()
        
        file_handler = RotatingFileHandler(
            str(log_file),
            maxBytes=10240,
            backupCount=10,
            encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
    except Exception as e:
        app.logger.error(f'Failed to set up file logging: {str(e)}')
        app.logger.warning('Continuing with console logging only')
    
    # Set the logger level
    app.logger.setLevel(logging.INFO)
    
    # Log startup message
    app.logger.info('Prize Bonds App startup')
    app.logger.info(f'Log file location: {log_file}')
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
    app.logger.info('Accessing index page')
    if "username" not in session:
        app.logger.info('User not logged in, redirecting to login')
        return render_template("index.html")

    table = request.args.get("table", "serials_1500")
    app.logger.info(f'Fetching serials from table: {table}')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT id, serial_start, serial_end, status FROM {table}")
        serials = cursor.fetchall()
        app.logger.info(f'Successfully fetched {len(serials)} serials')
    except Exception as e:
        app.logger.error(f'Error fetching serials: {str(e)}')
        raise
    finally:
        cursor.close()
        conn.close()
    return render_template("index.html", serials=serials, table=table)


@app.route("/add-serial", methods=["POST"])
def add_serial():
    if "username" not in session:
        app.logger.warning('Unauthorized attempt to add serial')
        return redirect(url_for("index"))

    serial_start = request.form["serial_start"]
    serial_end = request.form["serial_end"]
    status = request.form.get("status", "").strip().lower()
    table = request.form["table"]
    
    app.logger.info(f'Adding new serial range: {serial_start}-{serial_end} to table {table}')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            INSERT INTO {table} (serial_start, serial_end, status)
            VALUES (%s, %s, %s)
        """, (serial_start, serial_end, status))
        conn.commit()
        app.logger.info('Successfully added new serial range')
    except Exception as e:
        app.logger.error(f'Error adding serial: {str(e)}')
        raise
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("index", table=table))


@app.route("/delete/<table>/<int:serial_id>", methods=["POST"])
def delete_serial(table, serial_id):
    if "username" not in session:
        app.logger.warning('Unauthorized attempt to delete serial')
        return redirect(url_for("index"))

    app.logger.info(f'Deleting serial {serial_id} from table {table}')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM {table} WHERE id = %s", (serial_id,))
        conn.commit()
        app.logger.info(f'Successfully deleted serial {serial_id}')
    except Exception as e:
        app.logger.error(f'Error deleting serial: {str(e)}')
        raise
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for("index", table=table))


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    app.logger.info(f'Login attempt for user: {username}')
    
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
    except Exception as e:
        app.logger.error(f'Database error during login: {str(e)}')
        raise
    finally:
        cursor.close()
        conn.close()

    if result and result[0] == password:
        session["username"] = username
        app.logger.info(f'Successful login for user: {username}')
        return redirect(url_for("index"))
    else:
        app.logger.warning(f'Failed login attempt for user: {username}')
        return "Invalid username or password", 401


@app.route("/logout")
def logout():
    if "username" in session:
        app.logger.info(f'User {session["username"]} logged out')
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.logger.info('Starting application')
    app.run(host="0.0.0.0", port=5000)
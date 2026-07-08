# Make a basic landing page for a user to sign up and save information.

import os
import sqlite3
import sys

from flask import Flask, jsonify, request
import sqlite3


# Avoid the local folder named flask shadowing the real Flask installation.
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir in sys.path:
    sys.path.remove(script_dir)

# RESTORED IMPORTS: Added missing helper functions from flask
from flask import Flask, redirect, render_template_string, request, session, url_for


def dashboard_application():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config["SESSION_TYPE"] = "filesystem"

    def init_db():
        conn = sqlite3.connect("user_info_data.db")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    init_db()

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "").strip()
            if username and password:
                conn = sqlite3.connect("user_info_data.db")
                conn.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password),
                )
                conn.commit()
                conn.close()
                session["username"] = username
                return redirect(url_for("index"))

        # ENHANCED HTML: Added simple styling for a cleaner visual layout
        return render_template_string(
            """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Landing Page</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px; }
                    input { display: block; width: 100%; margin: 10px 0; padding: 8px; box-sizing: border-box; }
                    button { width: 100%; padding: 10px; background-color: #007BFF; color: white; border: none; border-radius: 4px; cursor: pointer; }
                    button:hover { background-color: #0056b3; }
                    .status { margin-top: 20px; padding: 10px; background-color: #e2f0d9; color: #385723; border-radius: 4px; }
                </style>
            </head>
            <body>
                <h1>Create Your Account</h1>
                <form method="post">
                    <input name="username" placeholder="Username" required>
                    <input name="password" type="password" placeholder="Password" required>
                    <button type="submit">Sign up</button>
                </form>
                
                {% if session.get('username') %}
                    <div class="status">
                        <strong>Success!</strong> Signed in as: {{ session['username'] }}
                    </div>
                {% endif %}
            </body>
            </html>
            """
        )

    return app


app = dashboard_application()


if __name__ == "__main__":
    app.run(debug=True)






app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    return jsonify({"message": "user created"}), 201


try:
    app.run(debug=True)
except Exception as e:
    print(f"Error starting the Flask application: {e}")


from flask import Flask, render_template, request
from utils.math_solver import solve_integral
from utils.ai_helper import ai_explain
import sqlite3
from utils.security import hash_password, is_strong_password, check_password
from flask import session, redirect, url_for
from utils.history import save_history 
from utils.agents import MultiAgentSystem
from utils.cohere_ai import explain_integral

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        expression TEXT,
        result TEXT,
        time TEXT
    )
    """)
    conn.commit()
    conn.close()

app = Flask(__name__)

app.secret_key = "supersecretkey"

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    result = None
    explanation = None

    if request.method == "POST":
        expr = request.form.get("expression")

        if expr:
            mas = MultiAgentSystem()
            result, _ = mas.run(expr)

            explanation = explain_integral(expr, result)
            save_history(session["user"], expr, result)
    
    return render_template(
    "index.html",
    result=result,
    explanation=explanation,
    session_user=session.get("user")
)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not is_strong_password(password):
            return "Пароль слишком слабый!"

        hashed = hash_password(password).decode()

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hashed, "user")
            )
            conn.commit()
        except:
            return "Пользователь уже существует!"

        conn.close()
        return "Регистрация успешна!"

    return render_template("register.html", user=session.get("user") )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        conn.close()

        if user and check_password(password, user[0]):
            session["user"] = username   # ← ВОТ ГЛАВНОЕ
            return redirect(url_for("index"))
        else:
            return "Неверные данные!"

    return render_template("login.html", user=session.get("user"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/profile")
def profile():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM history
        WHERE username=?
        ORDER BY id DESC
    """, (session["user"],))

    history = cursor.fetchall()
    conn.close()

    return render_template("profile.html", history=history, user=session.get("user"))

@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # текущий пользователь
    cursor.execute("SELECT * FROM users WHERE username=?", (session["user"],))
    current = cursor.fetchone()

    # проверка на админа
    if not current or current[3] != "admin":
        return "Доступ запрещён"

    # получаем всех пользователей
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template("admin.html", users=users, user=session.get("user"))

@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # проверка админа
    cursor.execute("SELECT * FROM users WHERE username=?", (session["user"],))
    current = cursor.fetchone()

    if not current or current[3] != "admin":
        return "Доступ запрещён"

    # нельзя удалить себя
    if current[0] == user_id:
        return "Нельзя удалить самого себя"

    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
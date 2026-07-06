from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

from db import get_db
from forms import LoginForm, RegisterForm
from models import get_user_by_username, get_user_by_id, User

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return User(user["id"], user["username"], user["password"])
    return None


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)

        if user and check_password_hash(user["password"], form.password.data):
            login_user(User(user["id"], user["username"], user["password"]))
            return redirect(url_for("dashboard"))

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        db = get_db()
        cursor = db.cursor()

        hashed = generate_password_hash(form.password.data)

        cursor.execute(
            "INSERT INTO usuarios (username, password) VALUES (%s, %s)",
            (form.username.data, hashed)
        )

        db.commit()
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
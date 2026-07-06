import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm
from models import get_user_by_username, get_user_by_id, User
from db import get_db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "clave_segura_por_defecto")

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_by_id(user_id)
    if user_data:
        return User(user_data["id"], user_data["username"], user_data["password"])
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_data = get_user_by_username(form.username.data)
        if user_data and check_password_hash(user_data["password"], form.password.data):
            user = User(user_data["id"], user_data["username"], user_data["password"])
            login_user(user)
            flash("Login exitoso ✅", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Usuario o contraseña incorrectos ❌", "danger")
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db = get_db()
        cursor = db.cursor()
        hashed_password = generate_password_hash(form.password.data)
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)",
                       (form.username.data, hashed_password))
        db.commit()
        flash("Usuario registrado correctamente ✅", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente ✅", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    # Seguridad: nunca usar debug=True en producción
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)

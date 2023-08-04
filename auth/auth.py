from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import  login_user
from models.models import database, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for("routes.index"))
        else:
            error = "Usuário e/ou senha incorretos, tentar novamente!"

    return render_template("login.html", error=error if "error" in locals() else None)

@auth_bp.route("/registro", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        nome_sgd = request.form["nome_sgd"]
        isAdmin = bool(request.form.get('isAdmin', False))
        email = request.form["email"]
        hashed_password = generate_password_hash(password)
        user = User.query.filter_by(username=username, password=hashed_password).first()
        if user:
            session["user_id"] = user.id
            error = "Usuário já cadastro!"
        else:
            new_user = User(username=username, password=hashed_password, email=email, nome_sgd=nome_sgd, isAdmin=isAdmin)
            database.session.add(new_user)
            database.session.commit()
            return redirect(url_for("auth.login"))
        
    return render_template("registro.html", error=error if "error" in locals() else None)

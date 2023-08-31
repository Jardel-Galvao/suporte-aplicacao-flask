from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import  login_user
from ..models.user import User
from ..models import database
from functools import wraps
from flask_login import current_user

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
            return render_template("login.html", error="Usuário e/ou senha incorretos, tentar novamente!"), 401
        
    return render_template("login.html")

@auth_bp.route("/registro", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        nome_sgd = request.form["nome_sgd"]
        isAdmin = bool(request.form.get('isAdmin', False))
        email = request.form["email"]
        hashed_password = generate_password_hash(password)
        user = User.query.filter_by(username=username).first()
        if user:
            session["user_id"] = user.id
            return render_template("login.html", error="Usuário já cadastro!"), 409
        else:
            new_user = User(username=username, password=hashed_password, email=email, nome_sgd=nome_sgd, isAdmin=isAdmin)
            database.session.add(new_user)
            database.session.commit()
            return redirect(url_for("auth.login"))
        
    return render_template("registro.html")

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.isAdmin:
            return func(*args, **kwargs)
        return redirect(url_for('routes.listar_meus_encaminhamentos_para_analise'))  # Redirect to the "Access Denied" page
        
    return decorated_function
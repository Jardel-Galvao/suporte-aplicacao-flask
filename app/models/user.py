from flask_login import UserMixin
from . import database

class User(database.Model, UserMixin):
    __tablename__ = 'user'
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), unique=True, nullable=False)  # Define 'username' field
    nome_sgd = database.Column(database.String(120), nullable=False)
    password = database.Column(database.String(120), nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    ativo = database.Column(database.Boolean, default=True)
    isAdmin = database.Column(database.Boolean, default=False)
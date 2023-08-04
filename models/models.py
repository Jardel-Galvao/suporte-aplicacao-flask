from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), unique=True, nullable=False)  # Define 'username' field
    nome_sgd = database.Column(database.String(120), nullable=False)
    password = database.Column(database.String(120), nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    ativo = database.Column(database.Boolean, default=True)
    isAdmin = database.Column(database.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'
class Encaminhamentos(database.Model):
    __tablename__ = 'encaminhamentos'
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)  # Unique identifier for each row
    ss = database.Column(database.Integer, index=True)
    data = database.Column(database.Date)
    tramite = database.Column(database.Integer)
    analista = database.Column(database.String)
    classificacao =database.Column(database.String)
    modulo = database.Column(database.String)
    topico = database.Column(database.String)

    def __repr__(self):
        return f'<SS {self.ss}>'

class EncaminhamentosIncorretos(Encaminhamentos):
    __tablename__ = 'encaminhamentos_incorretos'
    id = database.Column(database.Integer, database.ForeignKey('encaminhamentos.id'), primary_key=True)
    descricao_encaminahmento = database.Column(database.String)
    analise_analista = database.Column(database.Text, default="Não avaliado")
    concordancia = database.Column(database.Boolean, default=False)
    validacao = database.Column(database.Boolean, default=True)
    status = database.Column(database.Boolean, default=False)
    descricao_validacao = database.Column(database.Text, default="")

    def __repr__(self):
        return f'<SS {self.ss}>'

class DataConsultaSgd(database.Model):
    data = database.Column(database.Date, primary_key=True)

    def __repr__(self):
        return f'<Data {self.data}>'
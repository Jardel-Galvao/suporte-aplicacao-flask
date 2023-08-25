from . import database

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
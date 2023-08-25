from . import database

class IgnorarMes(database.Model):
    __tablename__ = 'IgnorarMes'
    id = database.Column(database.Integer, primary_key=True)
    id_analista = database.Column(database.Integer, database.ForeignKey('user.id'))
    mes = database.Column(database.Integer)
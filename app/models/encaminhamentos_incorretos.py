from . import database
from .encaminhamentos import Encaminhamentos

class EncaminhamentosIncorretos(Encaminhamentos):
    __tablename__ = 'encaminhamentos_incorretos'
    id = database.Column(database.Integer, database.ForeignKey('encaminhamentos.id'), primary_key=True)
    descricao_encaminahmento = database.Column(database.String)
    analise_analista = database.Column(database.Text, default="Não avaliado")
    concordancia = database.Column(database.Boolean, default=False)
    validacao = database.Column(database.Boolean, default=True)
    status = database.Column(database.Boolean, default=False)
    descricao_validacao = database.Column(database.Text, default="")

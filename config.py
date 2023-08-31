class Config:
    SECRET_KEY = 'sua_chave_secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Codigos Python/suporte-aplicacao-flask/app/instance/producao/database.db'

class TestConfig:
    SECRET_KEY = 'sua_chave_secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Codigos Python/suporte-aplicacao-flask/app/instance/teste/database_teste.db'
    TESTING = True
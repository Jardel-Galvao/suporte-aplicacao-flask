def test_adicionar_encaminhamento_manual(client, app):
    with app.app_context():
        from app.models.encaminhamentos_incorretos import EncaminhamentosIncorretos
        from datetime import date

        novo_usuario = {
            'username' : 'teste',
            'nome_sgd' : 'teste',
            'email' : 'teste@gmail.com',
            'password' : '123456',
            'isAdmin' : True,
        }

        client.post('/registro', data=novo_usuario)

        dados_login = {
            'username' : 'teste',
            'password' : '123456'
        }
        client.post('/login', data=dados_login)
        
        novo_encaminhamento = {
            'data' : date(2023, 1, 1),
            'tramite' : 1,
            'analista' : 'teste',
            'ss' : 1,
            'analise_analista' : 'analise',
        }
  
        client.post('/adicionar_encaminhamento_incorreto_manual/', data=novo_encaminhamento)
        encaminhamento = EncaminhamentosIncorretos.query.first()
        assert encaminhamento.ss == 1
        assert encaminhamento.analista == 'teste'
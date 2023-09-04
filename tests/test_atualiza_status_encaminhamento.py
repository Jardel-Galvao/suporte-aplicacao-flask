def test_atualiza_status_encaminhamento(client, app):
    with app.app_context():
        from app.models.encaminhamentos_incorretos import EncaminhamentosIncorretos
        from datetime import date
        from app.models import database

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
        
        novo_encaminhamento_incorreto = EncaminhamentosIncorretos(
            data = date(2023, 1, 1),
            tramite = 1,
            analista = 'teste',
            ss = 1,
            descricao_encaminahmento = 'Não deveria vir',
            validacao = False,
            status = True 
        )

        database.session.add(novo_encaminhamento_incorreto)
        database.session.commit()

        dados_atualizacao = {
            'opcao_selecionada' : False,
            'analise_analista' : 'Não concordo'
        }

        client.post('/atualiza_status_encaminhamento/1/', data=dados_atualizacao)
        
        encaminhamento = EncaminhamentosIncorretos.query.first()

        assert encaminhamento.status  == False
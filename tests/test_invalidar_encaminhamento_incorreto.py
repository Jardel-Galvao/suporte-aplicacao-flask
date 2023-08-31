def test_invalidar_encaminhamento_incorreto(client, app):
    with app.app_context():
        from app.models.encaminhamentos_incorretos import EncaminhamentosIncorretos

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
            'data' : '2023-01-01',
            'tramite' : 1,
            'analista' : 'teste',
            'ss' : 1,
            'descricao_encaminahmento' : 'Não deveria vir',
            'analise_analista' : 'analise',
        }

        client.post('/adicionar_encaminhamento_incorreto_manual/', data=novo_encaminhamento)
        
        invalidacao = {
            'opcao_selecionada' : 'False',
            'descricao_validacao' : 'Não concordo com essa',
        }
        client.post('/valida_inavalida_encaminhamento/1/', data=invalidacao)
        encaminhamento = EncaminhamentosIncorretos.query.first()

        assert encaminhamento.validacao == False
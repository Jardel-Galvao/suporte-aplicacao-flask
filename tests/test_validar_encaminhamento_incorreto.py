def test_validar_encaminhamento_incorreto(client, app):
    with app.app_context():
        from app.models.encaminhamentos_incorretos import EncaminhamentosIncorretos
        from app.models.user import User

        novo_usuario = {
            'username' : 'teste',
            'nome_sgd' : 'teste',
            'email' : 'teste@gmail.com',
            'password' : '123456',
            'isAdmin' : True,
        }
        client.post('/registro', data=novo_usuario)
        usuario = User.query.first()

        dados_login = {
            'username' : 'teste',
            'password' : '123456'
        }
        client.post('/login', data=dados_login)
        novo_encaminhamento = {
            'data' : '2023-01-01',
            'tramite' : 1,
            'analista' : usuario.nome_sgd,
            'ss' : 1,
            'analise_analista' : 'analise',
        }
        client.post('/adicionar_encaminhamento_incorreto_manual/', data=novo_encaminhamento)

        validacao = {
            'opcao_selecionada' : 'True',
            'descricao_validacao' : 'Concordo',
        }

        client.post('/valida_inavalida_encaminhamento/1/', data=validacao)
        encaminhamento = EncaminhamentosIncorretos.query.first()
        assert encaminhamento.validacao == True
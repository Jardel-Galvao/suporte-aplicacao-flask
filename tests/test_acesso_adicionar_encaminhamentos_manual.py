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
  
        response = client.get('/adicionar_encaminhamento_incorreto_manual/')
        print(response.data)
        assert b'name="analista"' in response.data
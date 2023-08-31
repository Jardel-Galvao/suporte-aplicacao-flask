def test_logout(client, app):
    with app.app_context():
        from app.models.user import User
        novo_usuario = {
            'username' : 'teste',
            'nome_sgd' : 'teste',
            'email' : 'teste@gmail.com',
            'password' : '123456',
        }
        client.post('/registro', data=novo_usuario)
        dados_login = {
            'username' : 'teste',
            'password' : '123456'
        }
        client.post('/login', data=dados_login)
        client.post('/logout')
        response = client.get('/listar_encaminhamentos_incorretos_invalidados')
        assert b'You should be redirected automatically' in response.data
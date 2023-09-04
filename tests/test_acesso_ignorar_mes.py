def test_acesso_ignorar_mes(client, app):
    with app.app_context():
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
        response = client.get('/ignorar_mes')
        
        assert b'<td>teste</td>' in response.data
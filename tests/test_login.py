def test_login(client, app):
    with app.app_context():
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
        
        response = client.post('/login', data=dados_login)
        

        assert response.status_code == 302
        assert response.headers['Location'] == '/'
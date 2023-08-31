def test_criar_usuario_existente(client, app):
    with app.app_context():
        from app.models.user import User

        novo_usuario = {
            'username' : 'teste',
            'nome_sgd' : 'teste',
            'email' : 'teste@gmail.com',
            'password' : '123456',
        }
        client.post('/registro', data=novo_usuario)

        novo_usuario_existente = {
            'username' : 'teste',
            'nome_sgd' : 'teste',
            'email' : 'teste2@gmail.com',
            'password' : '123456',
        }

        response = client.post('/registro', data=novo_usuario_existente)

        assert response.status_code == 409
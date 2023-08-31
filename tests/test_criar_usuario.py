def test_criar_usuario(client, app):
    with app.app_context():
        from app.models.user import User

        novo_usuario = {
            'username' : 'teste',
            'nome_sgd' : 'teste',
            'email' : 'teste@gmail.com',
            'password' : '123456',
        }
        client.post('/registro', data=novo_usuario)
        usuario = User.query.first()
        assert usuario is not None
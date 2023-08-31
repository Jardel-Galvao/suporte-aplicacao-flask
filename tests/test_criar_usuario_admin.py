def test_criar_usuario_admin(client, app):
    with app.app_context():
        from app.models.user import User
        novo_usuario = {
            'username' : 'admin',
            'nome_sgd' : 'admin',
            'email' : 'admin@gmail.com',
            'password' : '123456',
            'isAdmin' : True,
        }
        client.post('/registro', data=novo_usuario)
        usuario = User.query.filter_by(username='admin').first()
        assert usuario.username == 'admin'
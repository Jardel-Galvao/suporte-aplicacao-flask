def test_ignorar_mes(client, app):
    with app.app_context():
        from app.models.user import User
        from app.models.ignora_mes import IgnorarMes

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
        data = {
            'mes_a_ignorar' : 5,
        }
        response = client.post('/adicionar_mes_a_ignorar/1/', data=data)
        mes_ignorado = IgnorarMes.query.first()
        assert mes_ignorado.mes == 5
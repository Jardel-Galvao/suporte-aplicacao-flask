def test_listar_meus_encaminhamentos_para_analise_admin(client, app):
    with app.app_context():
        from app.models.encaminhamentos_incorretos import EncaminhamentosIncorretos
        from app.models.user import User
        from app.models import database
        from datetime import date 

        novo_usuario = {
            'username' : 'teste',
            'nome_sgd' : 'teste',
            'email' : 'teste@gmail.com',
            'password' : '123456',
        }

        client.post('/registro', data=novo_usuario)

        novo_usuario_admin = {
            'username' : 'admin',
            'nome_sgd' : 'admin',
            'email' : 'admin@gmail.com',
            'password' : '123456',
            'isAdmin' : True,
        }

        client.post('/registro', data=novo_usuario_admin)

        dados_login = {
            'username' : 'admin',
            'password' : '123456'
        }

        client.post('/login', data=dados_login)
       
        novo_encaminhamento_incorreto = EncaminhamentosIncorretos(
            data = date(2023, 1, 1),
            tramite = 1,
            analista = 'teste',
            ss = 1,
            descricao_encaminahmento = 'Não deveria vir'
        )
    
        database.session.add(novo_encaminhamento_incorreto)
        database.session.commit()

        response = client.get('/listar_meus_encaminhamentos_para_analise')

        assert b'deveria vir' in response.data
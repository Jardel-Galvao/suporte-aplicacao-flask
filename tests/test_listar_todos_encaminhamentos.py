def test_listar_todos_encaminhamentos_admin(client, app):
    with app.app_context():
        from app.models.encaminhamentos_incorretos import Encaminhamentos
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
       
        novo_encaminhamento_incorreto = Encaminhamentos(
            data = date(2023, 1, 1),
            tramite = 1,
            analista = 'teste',
            ss = 1
        )
    
        database.session.add(novo_encaminhamento_incorreto)
        database.session.commit()

        response = client.get('/listar_todos_encaminhamentos')

        assert b'<td>1</td>' in response.data

def test_listar_todos_encaminhamentos_usuario_comum(client, app):
    with app.app_context():
        from app.models.encaminhamentos_incorretos import Encaminhamentos
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
            'username' : 'teste2',
            'nome_sgd' : 'teste2',
            'email' : 'teste2@gmail.com',
            'password' : '123456'
        }

        client.post('/registro', data=novo_usuario_admin)

        dados_login = {
            'username' : 'teste',
            'password' : '123456'
        }

        client.post('/login', data=dados_login)
       
        novo_encaminhamento_incorreto = Encaminhamentos(
            data = date(2023, 1, 1),
            tramite = 1,
            analista = 'teste',
            ss = 1
        )

        novo_encaminhamento_incorreto2 = Encaminhamentos(
            data = date(2023, 1, 1),
            tramite = 1,
            analista = 'teste2',
            ss = 2
        )
    
    
        database.session.add(novo_encaminhamento_incorreto)
        database.session.add(novo_encaminhamento_incorreto2)
        database.session.commit()

        response = client.get('/listar_todos_encaminhamentos')
        
        assert b'<td>1</td>' in response.data
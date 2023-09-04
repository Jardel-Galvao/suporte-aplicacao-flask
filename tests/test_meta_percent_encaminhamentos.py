def test_meta_percent_encaminhamentos(client, app):
    with app.app_context():
        from app.models.encaminhamentos_incorretos import EncaminhamentosIncorretos
        from app.models.encaminhamentos import Encaminhamentos
        from app.models.user import User
        from app.models import database
        from datetime import date
        from app.models.ignora_mes import IgnorarMes

        novo_usuario = {
            'username' : 'teste',
            'nome_sgd' : 'teste',
            'email' : 'teste@gmail.com',
            'password' : '123456',
            'isAdmin' : True,
        }
        client.post('/registro', data=novo_usuario)
        usuario = User.query.first()
        dados_login = {
            'username' : 'teste',
            'password' : '123456'
        }

        client.post('/login', data=dados_login)
       
        novo_encaminhamento_incorreto = EncaminhamentosIncorretos(
            data = date(2023, 1, 1),
            tramite = 1,
            analista = usuario.nome_sgd,
            ss = 1,
            descricao_encaminahmento = 'Não deveria vir',
            analise_analista = 'analise',
            validacao = True,
            status = True
            
        )

        novo_encaminhamento_normal = Encaminhamentos(
            data = date(2023, 1, 1),
            tramite = 1,
            analista = usuario.nome_sgd,
            ss = 2
        )

        novo_encaminhamento_normal2 = Encaminhamentos(
            data = date(2023, 1, 1),
            tramite = 1,
            analista = usuario.nome_sgd,
            ss = 3
        )
        novo_encaminhamento_normal3 = Encaminhamentos(
            data = date(2023, 1, 1),
            tramite = 1,
            analista = usuario.nome_sgd,
            ss = 4
        )
    
        database.session.add(novo_encaminhamento_incorreto)
        database.session.add(novo_encaminhamento_normal)
        database.session.add(novo_encaminhamento_normal2)
        database.session.add(novo_encaminhamento_normal3)
        database.session.commit()

        response = client.get('/meta_percent_encaminhamentos')

        assert b'75.0' in response.data
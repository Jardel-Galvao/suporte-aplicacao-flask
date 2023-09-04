class TestListarEncaminhamentosIncorretos_validados:
    from app.models.encaminhamentos_incorretos import EncaminhamentosIncorretos
    from app.models.user import User
    from app.models import database
    from datetime import date

    def admin(self, client, app):  
        with app.app_context():    
            novo_usuario = {
                'username' : 'teste',
                'nome_sgd' : 'teste',
                'email' : 'teste@gmail.com',
                'password' : '123456',
                'isAdmin' : True,
            }
            client.post('/registro', data=novo_usuario)
            usuario = self.User.query.first()
            dados_login = {
                'username' : 'teste',
                'password' : '123456'
            }

            client.post('/login', data=dados_login)
        
            novo_encaminhamento_incorreto = self.EncaminhamentosIncorretos(
                data = self.date(2023, 1, 1),
                tramite = 1,
                analista = usuario.nome_sgd,
                ss = 1,
                descricao_encaminahmento = 'Não deveria vir',
                validacao = True,
                status = True
            )
        
            self.database.session.add(novo_encaminhamento_incorreto)
            self.database.session.commit()

            response = client.get('/listar_encaminhamentos_incorretos_validados')
            assert b'deveria vir' in response.data

    def comum(self, client, app):
        with app.app_context():
            novo_usuario = {
                'username' : 'teste',
                'nome_sgd' : 'teste',
                'email' : 'teste@gmail.com',
                'password' : '123456',
            }

            novo_usuario2 = {
                'username' : 'teste2',
                'nome_sgd' : 'teste2',
                'email' : 'teste2@gmail.com',
                'password' : '123456',
            }

            client.post('/registro', data=novo_usuario)
            client.post('/registro', data=novo_usuario2)

            usuario = self.User.query.filter_by(username='teste').first()
            usuario2 = self.User.query.filter_by(username='teste2').first()

            dados_login = {
                'username' : 'teste',
                'password' : '123456'
            }

            client.post('/login', data=dados_login)
        
            novo_encaminhamento_incorreto = self.EncaminhamentosIncorretos(
                data = self.date(2023, 1, 1),
                tramite = 1,
                analista = usuario.nome_sgd,
                ss = 1,
                descricao_encaminahmento = 'Encaminhamento incorreto',
                validacao = True,
                status = True
            )

            novo_encaminhamento_incorreto2 = self.EncaminhamentosIncorretos(
                data = self.date(2023, 1, 1),
                tramite = 1,
                analista = usuario2.nome_sgd,
                ss = 2,
                descricao_encaminahmento = 'Encaminhamento',
                validacao = True,
                status = True
            )
        
            self.database.session.add(novo_encaminhamento_incorreto)
            self.database.session.add(novo_encaminhamento_incorreto2)
            self.database.session.commit()

            response = client.get('/listar_encaminhamentos_incorretos_validados')

            assert b'Encaminhamento incorreto' in response.data
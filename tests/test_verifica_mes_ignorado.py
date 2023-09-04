def test_verifica_mes_ignorado( app):
    with app.app_context():
        from app.models.ignora_mes import IgnorarMes
        from app.routes.routes import verifica_mes_ignorado
        from app.models import database

        mes_ignorado = IgnorarMes(
            mes = 8,
            id_analista = 1
        )

        database.session.add(mes_ignorado)
        database.session.commit()

        retorno1 = verifica_mes_ignorado(8, 1)
        retorno2 = verifica_mes_ignorado(5, 1)

        assert retorno1 == True and retorno2 == False
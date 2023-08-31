def test_calcular_media(app):
    with app.app_context():
        from app.routes.routes import calcular_media
        media_zero = calcular_media(0, 10)
        media_valida = calcular_media(5, 20)

        assert media_zero == 100 and media_valida == 75.0

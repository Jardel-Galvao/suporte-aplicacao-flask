def test_importar_arquivo_sql(app):
    import os
    with app.app_context():
        from app.libs.importa_arquivo_sql import import_sql_file
        sql_statements = import_sql_file('tests/sql_teste/arquivo_teste.sql')

    assert 'SELECT' in sql_statements
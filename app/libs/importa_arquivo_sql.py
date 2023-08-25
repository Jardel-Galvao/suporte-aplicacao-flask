def import_sql_file(file_path):
    with open(file_path, 'r') as sql_file:
        sql_statements = sql_file.read()
    return sql_statements
from datetime import datetime
import os
import shutil

def realizar_backup():
    # Obtém o diretório atual do script
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Constrói o caminho para o banco de dados
    caminho_banco = os.path.join(diretorio_atual, '..', 'Instance', 'Producao', 'database.db')

    # Constrói o caminho para o diretório de backup
    diretorio_backup = os.path.join(diretorio_atual, '..', 'Instance', 'Backup')

    data_horario_backup = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    nome_backup = f'backup_{data_horario_backup}.db'

    caminho_backup = os.path.join(diretorio_backup, nome_backup)

    shutil.copy(caminho_banco, caminho_backup)

    return caminho_backup
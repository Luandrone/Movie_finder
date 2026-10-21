# Cria conexões PostgreSQL a partir das variáveis de ambiente.
import os
import psycopg
from dotenv import load_dotenv

def obter_conexao():
    # Abre uma conexão; quem chama deve encerrá-la.
    load_dotenv()
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    name = os.getenv('DB_NAME')
    port = os.getenv('DB_PORT')
    password = os.getenv('DB_PASSWORD')

    configuracoes = {
        'DB_HOST': host,
        'DB_PORT': port,
        'DB_NAME': name,
        'DB_USER': user,
        'DB_PASSWORD': password
    }

    variaveis_ausentes = [
        nome for nome, valor in configuracoes.items()
        if not valor
    ]

    if variaveis_ausentes:
        nomes = ', '.join(variaveis_ausentes)
        raise ValueError(
            f'Variáveis de ambiente obrigatórias ausentes: {nomes}'
        )

    conn = psycopg.connect(
        host = host,
        port = port,
        dbname = name,
        user = user,
        password = password
    )
    
    return conn

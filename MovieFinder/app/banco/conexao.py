import os
import psycopg
from dotenv import load_dotenv

def obter_conexao():
    load_dotenv()
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    name = os.getenv('DB_NAME')
    port = os.getenv('DB_PORT')
    password = os.getenv('DB_PASSWORD')
    conn = psycopg.connect(
        host = host,
        port = port,
        dbname = name,
        user = user,
        password = password
    )
    return conn

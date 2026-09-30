import os
import psycopg
from dotenv import load_dotenv

from app.banco.mapper import mapear_filme

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
cursor = conn.cursor()
cursor.execute('SELECT * FROM tblFilmes;')
resultado = cursor.fetchall()

lista_de_filmes = []
for linha in resultado:
    filme = mapear_filme(linha)
    lista_de_filmes.append(filme)
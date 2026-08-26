from app.banco.conexao import obter_conexao
from app.banco.mapper import mapear_filme


def buscar_filmes_banco():
    conn = obter_conexao()

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tblFilmes;')
    resultado = cursor.fetchall()

    lista_filmes = []
    for linha in resultado:
        filme = mapear_filme(linha)
        lista_filmes.append(filme)

    return lista_filmes

def salvar_filme(filme):
    conn = obter_conexao()

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tblFilmes WHERE tmdb_id = %s', (filme.id,))
    filme_existente = cursor.fetchone()




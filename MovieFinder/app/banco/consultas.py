from teste_postgres import cursor
def buscar_todos_filmes(cursor):
    cursor.execute(
        'SELECT * FROM tblFilmes;'
    )
    resultado = cursor.fetchall()
    return resultado

def buscar_por_tmdb_id(cursor, tmdb_id):

    cursor.execute('SELECT * FROM tblFilmes WHERE tmdb_id = %s;', (tmdb_id,))
    resultado = cursor.fetchone()
    return resultado

def inserir_filme(cursor, filme):
    cursor.execute(
        'INSERT INTO tblFilmes (tmdb_id, titulo, ano, nota, sinopse, duracao)'
        'VALUES (%s, %s, %s, %s, %s, %s);',
        (
            filme.id,
            filme.titulo,
            filme.ano,
            filme.nota,
            filme.sinopse,
            filme.duracao
        )
    )

def atualizar_filme(cursor,campos_atualizacao, valores):
    sql_update = 'UPDATE tblFilmes SET ' + campos_atualizacao + ' WHERE tmdb_id = %s;'
    cursor.execute(sql_update, valores)
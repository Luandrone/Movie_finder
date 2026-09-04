
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

def inserir_disponibilidade(cursor, filme, disponibilidade):
    cursor.execute(
        'INSERT INTO tblDisponibilidade (tmdb_id, provider_id, provider_name, tipo, logo_path, link)'
        'VALUES (%s, %s, %s, %s, %s, %s);',
        (
            filme.id,
            disponibilidade['provider_id'],
            disponibilidade['provider_name'],
            disponibilidade['tipo'],
            disponibilidade['logo_path'],
            disponibilidade['link']
        )
    )

def buscar_disponibilidade(cursor, tmdb_id, provider_id, tipo):
    cursor.execute(
        'SELECT * FROM tblDisponibilidade WHERE tmdb_id = %s AND provider_id = %s AND tipo = %s;',
        (tmdb_id, provider_id, tipo)
    )

    resultado = cursor.fetchone()

    return resultado























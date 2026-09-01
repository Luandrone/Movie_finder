from app.banco.comparador import comparar_filmes
from app.banco.conexao import obter_conexao
from app.banco.mapper import mapear_filme


def buscar_filmes_banco():
    conn = obter_conexao()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tblFilmes;')
        resultado = cursor.fetchall()

        lista_filmes = []
        for linha in resultado:
            filme = mapear_filme(linha)
            lista_filmes.append(filme)
    finally:
        conn.close()

    return lista_filmes


def salvar_filme(filme):
    conn = obter_conexao()

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tblFilmes WHERE tmdb_id = %s', (filme.id,))
        filme_existente = cursor.fetchone()

        if filme_existente is None:
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

            conn.commit()

            return {'status': 'novo'}

        else:
            filme_banco = mapear_filme(filme_existente)
            resultado = comparar_filmes(filme, filme_banco)
            if not resultado:
                return {'status': 'já_existe'}

            campos = []
            valores = []

            for alteracao in resultado:
                campos.append(alteracao['campo'])
                valores.append(alteracao['novo'])

            set_partes = []

            for campo in campos:
                set_partes.append(campo + ' = %s')

            set_clause = ', '.join(set_partes)

            valores.append(filme.id)

            sql_update = 'UPDATE tblFilmes SET ' + set_clause + ' WHERE tmdb_id = %s;'
            cursor.execute(sql_update, valores)

            conn.commit()

            return {
                'status': 'atualizado',
                'alteracoes': resultado
            }
    finally:
        conn.close()

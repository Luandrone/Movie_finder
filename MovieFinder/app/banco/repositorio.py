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
        if filme.nota != filme_existente[4]:
            resultado = {
                'status': 'atualizado',
                'alteracoes': [
                    {
                        'campo': 'nota',
                        'anterior': filme_existente[4],
                        'novo': filme.nota,
                    }
                ]

            }
            cursor.execute(
                'UPDATE tblFilmes '
                'SET nota = %s '
                'WHERE tmdb_id = %s; ',
                (filme.nota, filme.id)
            )

            conn.commit()

            return resultado

        return {'status': 'já_existe'}




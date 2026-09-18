from app.banco.comparador import comparar_filmes, comparar_disponibilidades
from app.banco.conexao import obter_conexao
from app.banco.consultas import buscar_por_tmdb_id, inserir_filme, atualizar_filme, buscar_todos_filmes, \
    buscar_disponibilidades_filme, sincronizar_disponibilidades
from app.banco.mapper import mapear_filme


def buscar_filmes_banco():
    conn = obter_conexao()
    try:
        cursor = conn.cursor()
        resultado = buscar_todos_filmes(cursor)

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
        filme_existente = buscar_por_tmdb_id(cursor, filme.id)

        if filme_existente is None:
            inserir_filme(cursor, filme)

            conn.commit()

            return {'status': 'novo'}

        filme_banco = mapear_filme(filme_existente)
        resultado = comparar_filmes(filme, filme_banco)

        disponibilidade_banco = buscar_disponibilidades_filme(cursor, filme.id)
        resultado_disponibilidades = comparar_disponibilidades(filme.disponibilidade, disponibilidade_banco)

        if not resultado and not any(resultado_disponibilidades.values()):
            return {'status': 'já_existe'}

        if resultado:
            campos_alterados = []
            valores_novos = []

            for alteracao in resultado:
                campos_alterados.append(alteracao['campo'])
                valores_novos.append(alteracao['novo'])

            partes_set = []

            for campo in campos_alterados:
                partes_set.append(campo + ' = %s')

            campos_atualizacao = ', '.join(partes_set)

            valores_novos.append(filme.id)

            atualizar_filme(cursor, campos_atualizacao, valores_novos)

        sincronizar_disponibilidades(cursor, filme, resultado_disponibilidades)






        conn.commit()

        return {
            'status': 'atualizado',
            'alteracoes': resultado
        }
    finally:
        conn.close()

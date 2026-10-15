# Coordena consultas, comparações e transações para salvar e carregar filmes.
from app.banco.comparador import comparar_filmes, comparar_disponibilidades, comparar_generos
from app.banco.conexao import obter_conexao
from app.banco.consultas import buscar_por_tmdb_id, inserir_filme, atualizar_filme, buscar_todos_filmes, \
    buscar_disponibilidades_filme, sincronizar_disponibilidades, buscar_genero_por_tmdb_id, inserir_genero, \
    inserir_filme_genero, buscar_generos_filme, excluir_generos_filme, excluir_disponibilidade, \
    excluir_disponibilidades_do_filme, excluir_associacoes_generos_do_filme, excluir_filme_por_id
from app.banco.mapper import mapear_filme, mapear_disponibilidade, mapear_genero


def buscar_filmes_banco():
    # Carrega os filmes salvos e mapeia cada registro para Filme.
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
    # Insere ou sincroniza filme, gêneros e provedores em uma única transação.
    conn = obter_conexao()

    try:
        cursor = conn.cursor()
        filme_existente = buscar_por_tmdb_id(cursor, filme.id)

        if filme_existente is None:
            filme_id = inserir_filme(cursor, filme)
            salvar_generos_filme(cursor, filme, filme_id)

            resultado_disponibilidades = {
                'novas': filme.disponibilidade,
                'atualizadas': [],
                'excluidas': []
            }

            sincronizar_disponibilidades(
                cursor,
                filme,
                resultado_disponibilidades
            )

            conn.commit()

            return {'status': 'novo'}

        filme_banco = mapear_filme(filme_existente)
        resultado = comparar_filmes(filme, filme_banco)

        linhas = buscar_generos_filme(cursor, filme_banco.id_banco)
        generos_banco = []

        for linha in linhas:
            generos_banco.append(mapear_genero(linha))

        resultado_generos = comparar_generos(filme.generos, generos_banco)

        disponibilidade_banco = buscar_disponibilidades_filme(cursor, filme.id)

        lista_disponibilidades = []

        for linha in disponibilidade_banco:
            disponibilidade = mapear_disponibilidade(linha)
            lista_disponibilidades.append(disponibilidade)

        resultado_disponibilidades = comparar_disponibilidades(filme.disponibilidade, lista_disponibilidades)

        if not resultado and not any(resultado_disponibilidades.values()) and not any(resultado_generos.values()):
            return {'status': 'já_existe'}

        for genero in resultado_generos['excluidos']:
            genero_atual = buscar_genero_por_tmdb_id(cursor, genero['tmdb_id'])
            excluir_generos_filme(cursor, filme_banco.id_banco, genero_atual[0])

        for genero in resultado_generos['novos']:
            genero_atual = buscar_genero_por_tmdb_id(cursor, genero['tmdb_id'])

            if genero_atual is None:
                genero_id = inserir_genero(cursor, genero)
            else:
                genero_id = genero_atual[0]

            inserir_filme_genero(cursor, filme_banco.id_banco, genero_id)

        if resultado:
            atualizar_filme(cursor, filme.id, resultado)

        sincronizar_disponibilidades(cursor, filme, resultado_disponibilidades)

        conn.commit()

        return {
            'status': 'atualizado',
            'alteracoes': resultado
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

def buscar_disponibilidades_do_filme_no_banco(filme):
    # Carrega provedores persistidos para exibir um filme salvo.
    conn = obter_conexao()

    try:
        cursor = conn.cursor()

        disponibilidades_banco = buscar_disponibilidades_filme(cursor, filme.id)

        lista_disponibilidades = []

        for linha in disponibilidades_banco:
            lista_disponibilidades.append(mapear_disponibilidade(linha))

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return lista_disponibilidades

def salvar_generos_filme(cursor, filme, filme_id):
    # Garante o cadastro de cada gênero e cria as relações com o filme.
    for genero in filme.generos:
        genero_banco = buscar_genero_por_tmdb_id(cursor, genero['tmdb_id'])
        if genero_banco is None:
            genero_id = inserir_genero(cursor, genero)
        else:
            genero_id = genero_banco[0]

        inserir_filme_genero(cursor, filme_id, genero_id)

def buscar_generos_do_filme_no_banco(filme):
    # Carrega os gêneros ligados ao ID interno do filme.
    conn = obter_conexao()

    try:
        cursor = conn.cursor()

        genero_banco = buscar_generos_filme(cursor, filme.id_banco)

        lista_generos = []

        for genero in genero_banco:
            lista_generos.append(mapear_genero(genero))

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return lista_generos

def excluir_filme_banco(filme):
    conn = obter_conexao()

    try:
        cursor = conn.cursor()

        excluir_disponibilidades_do_filme(cursor, filme.id)
        excluir_associacoes_generos_do_filme(cursor, filme.id_banco)
        excluir_filme_por_id(cursor, filme.id_banco)

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

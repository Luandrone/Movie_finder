from decimal import Decimal
from unittest.mock import Mock, patch

from app.banco.consultas import buscar_por_tmdb_id, inserir_filme, atualizar_filme, buscar_todos_filmes
from app.filme import Filme
from teste_postgres import resultado

def test_buscar_todos_filmes():
    mock_cursor = Mock()
    resultado_falso = (
        1,
        123,
        'Batman',
        2021,
        Decimal('8.0'),
        'blabla',
        210
    )

    mock_cursor.fetchall.return_value = resultado_falso

    resultado = buscar_todos_filmes(mock_cursor)

    assert resultado == resultado_falso
    mock_cursor.execute.assert_called_once_with('SELECT * FROM tblFilmes;')
    mock_cursor.fetchall.assert_called_once_with()

def test_buscar_por_tmdb_id():
    mock_cursor = Mock()
    linha_falsa = (
        1,
        212,
        'Batman',
        2020,
        Decimal('7.0'),
        'blabla',
        150
    )

    mock_cursor.fetchone.return_value = linha_falsa
    resultado = buscar_por_tmdb_id(mock_cursor, 212)

    assert resultado == linha_falsa
    mock_cursor.execute.assert_called_once_with(
        'SELECT * FROM tblFilmes WHERE tmdb_id = %s;',
        (212,)
    )
    mock_cursor.fetchone.assert_called_once_with()

def test_buscar_por_tmdb_id_nao_encontrado():
    mock_cursor = Mock()
    mock_cursor.fetchone.return_value = None

    resultado = buscar_por_tmdb_id(mock_cursor, 123)

    assert resultado is None
    mock_cursor.execute.assert_called_once_with(
        'SELECT * FROM tblFilmes WHERE tmdb_id = %s;',
        (123,)
    )

def test_inserir_filme():
    mock_cursor = Mock()
    filme_falso = Filme('Batman', 2020, 7.0, 123, 'blabla', 150)

    inserir_filme(mock_cursor, filme_falso)

    mock_cursor.execute.assert_called_once_with(
        'INSERT INTO tblFilmes (tmdb_id, titulo, ano, nota, sinopse, duracao)'
        'VALUES (%s, %s, %s, %s, %s, %s);',
        (
            filme_falso.id,
            filme_falso.titulo,
            filme_falso.ano,
            filme_falso.nota,
            filme_falso.sinopse,
            filme_falso.duracao
        )
    )

def test_atualizar_filme():
    mock_cursor = Mock()
    campos_atualizacao = 'titulo = %s, ano = %s, duracao = %s'
    valores = ['The Batman', 2022, 176, 212]
    atualizar_filme(mock_cursor, campos_atualizacao, valores)

    mock_cursor.execute.assert_called_once_with('UPDATE tblFilmes SET ' + campos_atualizacao + ' WHERE tmdb_id = %s;', valores)
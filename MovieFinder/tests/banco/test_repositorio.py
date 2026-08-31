from unittest.mock import patch, Mock, call
from decimal import Decimal
from app.banco.repositorio import buscar_filmes_banco, salvar_filme
from app.filme import Filme

@patch('app.banco.repositorio.obter_conexao')
def test_buscar_filmes_banco(mock_obter_conexao):
    linha_falsa = (
        1,
        123,
        'Batman',
        2021,
        Decimal('8.0'),
        'blabla',
        210
    )
    mock_cursor = Mock()
    mock_obter_conexao.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [linha_falsa]

    resultado = buscar_filmes_banco()
    resultado = resultado[0]

    assert resultado.titulo == 'Batman'
    assert resultado.ano == 2021
    assert resultado.nota == Decimal('8.0')
    assert resultado.id == 123
    assert resultado.sinopse == 'blabla'
    assert resultado.duracao == 210
    mock_cursor.fetchall.assert_called_once_with()
    mock_cursor.execute.assert_called_once_with('SELECT * FROM tblFilmes;')

@patch('app.banco.repositorio.obter_conexao')
def test_buscar_filmes_banco_sem_filmes(mock_obter_conexao):
    mock_cursor = Mock()
    mock_obter_conexao.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    resultado = buscar_filmes_banco()

    assert resultado == []

@patch('app.banco.repositorio.obter_conexao')
def test_salvar_filme_novo(mock_obter_conexao):
    filme_falso = Filme('Batman', 2020, 7.0, 212)
    mock_cursor = Mock()
    mock_obter_conexao.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    resultado = salvar_filme(filme_falso)

    assert resultado == {'status': 'novo'}
    assert mock_cursor.execute.call_args_list[1] == call(
        'INSERT INTO tblFilmes (tmdb_id, titulo, ano, nota, sinopse, duracao)'
        'VALUES (%s, %s, %s, %s, %s, %s);',
        (212, 'Batman', 2020, 7.0, '', '')
    )

@patch('app.banco.repositorio.obter_conexao')
def test_salvar_filme_ja_existente(mock_obter_conexao):
    filme_falso_existente = Filme('Batman', 2020, 7.0, 212,)
    mock_cursor = Mock()
    linha_do_banco_existente = (
        1,
        212,
        'Batman',
        2020,
        7.0,
        '',
        ''
    )
    mock_obter_conexao.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = linha_do_banco_existente

    resultado = salvar_filme(filme_falso_existente)

    assert resultado == {'status': 'já_existe'}
    assert len(mock_cursor.execute.call_args_list) == 1

@patch('app.banco.repositorio.obter_conexao')
def test_salvar_filme_atualizar_nota(mock_obter_conexao):
    filme_falso_existente = Filme('Batman', 2020, 8.0, 212,)
    mock_cursor = Mock()
    linha_do_banco_existente = (
        1,
        212,
        'Batman',
        2020,
        7.0,
        '',
        ''
    )

    mock_obter_conexao.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = linha_do_banco_existente
    resultado = salvar_filme(filme_falso_existente)
    assert resultado == {
        'status': 'atualizado',
        'alteracoes':[
            {
                'campo': 'nota',
                'anterior': 7.0,
                'novo': 8.0
            }
        ]
    }

    assert len(mock_cursor.execute.call_args_list) == 2
    assert mock_cursor.execute.call_args_list[1] == call(
        'UPDATE tblFilmes SET nota = %s WHERE tmdb_id = %s;',
        [8.0, 212]
    )
    mock_obter_conexao.return_value.commit.assert_called_once_with()


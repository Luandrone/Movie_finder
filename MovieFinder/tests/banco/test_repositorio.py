from unittest.mock import patch, Mock, call
from decimal import Decimal

import pytest

from app.banco.repositorio import buscar_filmes_banco, salvar_filme
from app.filme import Filme
from teste_postgres import resultado


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
    mock_obter_conexao.return_value.close.assert_called_once_with()


@patch('app.banco.repositorio.obter_conexao')
def test_buscar_filmes_banco_sem_filmes(mock_obter_conexao):
    mock_cursor = Mock()
    mock_obter_conexao.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    resultado = buscar_filmes_banco()

    assert resultado == []
    mock_obter_conexao.return_value.close.assert_called_once_with()


@patch('app.banco.repositorio.obter_conexao')
def test_buscar_filmes_fecha_conexao_em_erro(mock_obter_conexao):
    mock_cursor = Mock()
    mock_obter_conexao.return_value.cursor.return_value = mock_cursor

    mock_cursor.execute.side_effect = RuntimeError

    with pytest.raises(RuntimeError):
        buscar_filmes_banco()

    mock_obter_conexao.return_value.close.assert_called_once_with()


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

    mock_obter_conexao.return_value.close.assert_called_once_with()


@patch('app.banco.repositorio.obter_conexao')
def test_salvar_filme_ja_existente(mock_obter_conexao):
    filme_falso_existente = Filme('Batman', 2020, 7.0, 212, )
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
    mock_cursor.fetchall.return_value = []

    resultado = salvar_filme(filme_falso_existente)

    assert resultado == {'status': 'já_existe'}
    assert len(mock_cursor.execute.call_args_list) == 2
    mock_obter_conexao.return_value.close.assert_called_once_with()


@patch('app.banco.repositorio.obter_conexao')
def test_salvar_filme_atualizar_multiplos_campos(mock_obter_conexao):
    filme_falso_existente = Filme('The Batman', 2022, 8.0, 212, 'blabla', 176)
    filme_do_banco_existente = (
        1,
        212,
        'Batman',
        2020,
        7.0,
        'blabla',
        150
    )
    mock_cursor = Mock()

    mock_obter_conexao.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = filme_do_banco_existente
    mock_cursor.fetchall.return_value = []

    resultado = salvar_filme(filme_falso_existente)

    assert resultado == {
        'status': 'atualizado',
        'alteracoes': [
            {
                'campo': 'titulo',
                'anterior': 'Batman',
                'novo': 'The Batman'
            },
            {
                'campo': 'ano',
                'anterior': 2020,
                'novo': 2022
            },
            {
                'campo': 'nota',
                'anterior': 7.0,
                'novo': 8.0
            },
            {
                'campo': 'duracao',
                'anterior': 150,
                'novo': 176
            }
        ]
    }

    assert mock_cursor.execute.call_args_list[2] == call(
        'UPDATE tblFilmes SET titulo = %s, ano = %s, nota = %s, duracao = %s WHERE tmdb_id = %s;',
        ['The Batman', 2022, 8.0, 176, 212]
    )

    mock_obter_conexao.return_value.commit.assert_called_once_with()
    mock_obter_conexao.return_value.close.assert_called_once_with()


@patch('app.banco.repositorio.obter_conexao')
def test_salvar_filme_somente_disponibilidade_nova(mock_obter_conexao):
    filme = Filme('The Batman', 2020, 7.0, 212)
    filme.disponibilidade = [
        {
            'provider_id': 8,
            'provider_name': 'Netflix',
            'tipo': 'flatrate',
            'logo_path': '/netflix.png',
            'link': None
        }
    ]
    mock_cursor = Mock()
    mock_obter_conexao.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (
        1,
        212,
        'The Batman',
        2020,
        7.0,
        '',
        ''
    )
    mock_cursor.fetchall.return_value = []
    with    patch('app.banco.repositorio.sincronizar_disponibilidades') as mock_sincronizar, \
            patch('app.banco.repositorio.atualizar_filme') as mock_atualizar:
        resultado_disponibilidades = {
            'novas': [
                {
                    'provider_id': 8,
                    'provider_name': 'Netflix',
                    'tipo': 'flatrate',
                    'logo_path': '/netflix.png',
                    'link': None
                }
            ],
            'atualizadas': [],
            'excluidas': []
        }

        resultado = salvar_filme(filme)
        mock_sincronizar.assert_called_once_with(
            mock_cursor,
            filme,
            resultado_disponibilidades
        )
    mock_atualizar.assert_not_called()


@patch('app.banco.repositorio.obter_conexao')
def test_salvar_filme_somente_disponibilidade_atualizada(mock_obter_conexao):
    filme = Filme('The Batman', 2020, 7.0, 212)
    filme.disponibilidade = [
        {
            'provider_id': 8,
            'provider_name': 'Netflix',
            'tipo': 'flatrate',
            'logo_path': '/netflix.png',
            'link': 'https://link-novo.com'
        }
    ]
    mock_cursor = Mock()
    mock_obter_conexao.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (
        1,
        212,
        'The Batman',
        2020,
        7.0,
        '',
        ''
    )
    mock_cursor.fetchall.return_value = [
        {
            'provider_id': 8,
            'provider_name': 'Netflix',
            'tipo': 'flatrate',
            'logo_path': '/netflix.png',
            'link': 'https://link-antigo.com'
        }
    ]

    with    patch('app.banco.repositorio.sincronizar_disponibilidades') as mock_sincronizar, \
            patch('app.banco.repositorio.atualizar_filme') as mock_atualizar:
        resultado_disponibilidades = {
            'novas': [],
            'atualizadas': [
                {
                    'provider_id': 8,
                    'tipo': 'flatrate',
                    'alteracoes': [
                        {
                            'campo': 'link',
                            'anterior': 'https://link-antigo.com',
                            'novo': 'https://link-novo.com'
                        }
                    ]
                }
            ],
            'excluidas': []
        }
        salvar_filme(filme)

        mock_sincronizar.assert_called_once_with(
            mock_cursor,
            filme,
            resultado_disponibilidades
        )

        mock_atualizar.assert_not_called()


@patch('app.banco.repositorio.obter_conexao')
def test_salvar_filme_somente_disponibilidade_excluida(mock_obter_conexao):
    filme = Filme('The Batman', 2020, 7.0, 212)
    filme.disponibilidade = [
        {
            'provider_id': 8,
            'provider_name': 'Netflix',
            'tipo': 'flatrate',
            'logo_path': '/netflix.png',
            'link': None
        }
    ]
    mock_cursor = Mock()
    mock_obter_conexao.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (
        1,
        212,
        'The Batman',
        2020,
        7.0,
        '',
        ''
    )
    mock_cursor.fetchall.return_value = [
        {
            'provider_id': 8,
            'provider_name': 'Netflix',
            'tipo': 'flatrate',
            'logo_path': '/netflix.png',
            'link': None
        },
        {
            'provider_id': 119,
            'provider_name': 'Amazon Video',
            'tipo': 'flatrate',
            'logo_path': '/amazon.png',
            'link': None
        }
    ]

    with    patch('app.banco.repositorio.sincronizar_disponibilidades') as mock_sincronizar, \
            patch('app.banco.repositorio.atualizar_filme') as mock_atualizar:
        resultado_disponibilidades = {
            'novas': [],
            'atualizadas': [],
            'excluidas': [
                {
                    'provider_id': 119,
                    'provider_name': 'Amazon Video',
                    'tipo': 'flatrate',
                    'logo_path': '/amazon.png',
                    'link': None
                }
            ]
        }

        salvar_filme(filme)
        mock_sincronizar.assert_called_once_with(
            mock_cursor,
            filme,
            resultado_disponibilidades
        )
        mock_atualizar.assert_not_called()

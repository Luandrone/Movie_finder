from unittest.mock import patch

from app.filme import Filme
from app.menu import confirmar_exclusao_filme, confirmar_alteracao_favorito, confirmar_salvamento_filme, \
    solicitar_nome_filme


@patch('builtins.input', return_value='s')
def test_confirmar_exclusao_retorna_true(mock_input):
    filme = Filme('The Batman', 2022)

    resultado = confirmar_exclusao_filme(filme)

    assert resultado is True
    mock_input.assert_called_once_with(
        'Você deseja excluir The Batman ? (S/N): '
    )


@patch('builtins.input', return_value='n')
def test_cancelar_exclusao_retorna_false(mock_input):
    filme = Filme('The Batman', 2022)

    resultado = confirmar_exclusao_filme(filme)

    assert resultado is False

@patch('builtins.input', return_value='s')
def test_confirmar_adicao_aos_favoritos_retorna_true(
    mock_input, capsys
):
    filme = Filme('The Batman', 2022)

    resultado = confirmar_alteracao_favorito(filme)

    assert resultado is True
    mock_input.assert_called_once_with(
        'Você gostaria de adicionar esse filme aos favoritos ? (S/N): '
    )
    assert 'ainda não está nos favoritos' in capsys.readouterr().out


@patch('builtins.input', return_value='s')
def test_confirmar_remocao_dos_favoritos_retorna_true(
    mock_input, capsys
):
    filme = Filme('The Batman', 2022, favorito=True)

    resultado = confirmar_alteracao_favorito(filme)

    assert resultado is True
    mock_input.assert_called_once_with(
        'Você deseja remover esse filme dos favoritos ? (S/N): '
    )
    assert 'já está adicionado aos favoritos' in capsys.readouterr().out

@patch('builtins.input', return_value='s')
def test_confirmar_salvamento_retorna_true(mock_input):
    resultado = confirmar_salvamento_filme()

    assert resultado is True
    mock_input.assert_called_once_with(
        'Deseja salvar o filme ? (S/N): '
    )


@patch('builtins.input', return_value='n')
def test_cancelar_salvamento_retorna_false(mock_input):
    resultado = confirmar_salvamento_filme()

    assert resultado is False

@patch('builtins.input', return_value='The Batman')
def test_solicitar_nome_filme(mock_input):
    resultado = solicitar_nome_filme()

    assert resultado == 'The Batman'
    mock_input.assert_called_once_with(
        'Digite o nome do filme: '
    )
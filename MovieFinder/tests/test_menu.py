from unittest.mock import patch

from app.filme import Filme
from app.menu import confirmar_exclusao_filme


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
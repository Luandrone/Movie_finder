from app.filme import Filme
from app.serviço import buscar_e_mostrar_filme
from unittest.mock import patch, Mock

@patch('app.serviço.buscar_filme')
@patch('builtins.input', return_value='The Batman')
@patch('app.serviço.selecionar_filme')
def test_buscar_e_mostrar_filme(mock_selecionar_filme, mock_input, mock_buscar_filme):
    filme = Filme('The Batman', 2020, 7.0, 212)
    mock_buscar_filme.return_value = [filme]
    mock_selecionar_filme.return_value = filme
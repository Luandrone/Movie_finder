from app.excecoes import ErroApi
from app.filme import Filme
from app.serviço import buscar_e_mostrar_filme
from unittest.mock import patch, Mock

@patch('app.serviço.buscar_filme')
@patch('builtins.input', return_value='The Batman')
@patch('app.serviço.selecionar_filme')
@patch('app.serviço.mostrar_resultado')
@patch('app.serviço.buscar_detalhes')
@patch('app.serviço.buscar_disponibilidade')
@patch('app.serviço.salvar_filme')
@patch('app.serviço.mostrar_filme')
def test_buscar_e_mostrar_filme(
        mock_mostrar_filme,
        mock_salvar_filme,
        mock_buscar_disponibilidade,
        mock_buscar_detalhes,
        mock_mostrar_resultado,
        mock_selecionar_filme,
        mock_input,
        mock_buscar_filme):
    filme = Filme('The Batman', 2020, 7.0, 212)
    mock_buscar_filme.return_value = [filme]
    mock_selecionar_filme.return_value = filme

    buscar_e_mostrar_filme()

    mock_buscar_filme.assert_called_once_with('The Batman')
    mock_mostrar_resultado.assert_called_once_with([filme])
    mock_selecionar_filme.assert_called_once_with([filme])
    mock_buscar_detalhes.assert_called_once_with(filme)
    mock_buscar_disponibilidade.assert_called_once_with(filme)
    mock_salvar_filme.assert_called_once_with(filme)
    mock_mostrar_filme.assert_called_once_with(filme)

@patch('app.serviço.buscar_filme')
@patch('builtins.input', return_value='The Batman')
@patch('app.serviço.selecionar_filme')
@patch('app.serviço.mostrar_resultado')
@patch('app.serviço.buscar_detalhes')
@patch('app.serviço.buscar_disponibilidade')
@patch('app.serviço.salvar_filme')
@patch('app.serviço.mostrar_filme')
def test_buscar_filme_nao_encontrado(
        mock_mostrar_filme,
        mock_salvar_filme,
        mock_buscar_disponibilidade,
        mock_buscar_detalhes,
        mock_mostrar_resultado,
        mock_selecionar_filme,
        mock_input,
        mock_buscar_filme):

    mock_buscar_filme.return_value = []

    buscar_e_mostrar_filme()

    mock_mostrar_resultado.assert_not_called()
    mock_selecionar_filme.assert_not_called()
    mock_buscar_detalhes.assert_not_called()
    mock_buscar_disponibilidade.assert_not_called()
    mock_salvar_filme.assert_not_called()
    mock_mostrar_filme.assert_not_called()

@patch('app.serviço.buscar_filme')
@patch('builtins.input', return_value='The Batman')
def test_buscar_filme_erro_conexao(mock_input, mock_buscar_filme, capsys):
    mock_buscar_filme.side_effect = ErroApi('Erro', 'Problema de conexão')

    buscar_e_mostrar_filme()

    capturado = capsys.readouterr()

    assert 'Não foi possível conectar à API.' in capturado.out

@patch('app.serviço.buscar_filme')
@patch('builtins.input', return_value='The Batman')
def test_buscar_filme_erro_http(mock_input, mock_buscar_filme, capsys):
    mock_buscar_filme.side_effect = ErroApi('Erro', 'Problema de Http')

    buscar_e_mostrar_filme()

    capturado = capsys.readouterr()

    assert 'A API retornou um erro.' in capturado.out

@patch('app.serviço.buscar_filme')
@patch('builtins.input', return_value='The Batman')
def test_buscar_filme_outro_erro(mock_input, mock_buscar_filme, capsys):
    mock_buscar_filme.side_effect = ErroApi('Erro', 'Outro Problema')

    buscar_e_mostrar_filme()

    capturado = capsys.readouterr()

    assert 'Algum problema ocorreu!' in capturado.out
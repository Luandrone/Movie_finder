from app.excecoes import ErroApi
from app.filme import Filme
from app.serviço import buscar_e_mostrar_filme, _completar_dados_filme_salvo, _salvar_filme_se_confirmado, \
    excluir_filme_salvo, gerenciar_favoritos
from unittest.mock import patch, Mock
import pytest

@patch('app.serviço.buscar_filme')
@patch('builtins.input', side_effect=['The Batman', 's'])
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

def test_completar_dados_filme_salvo():
    filme = Filme('The Batman', 2022)

    disponibilidades = [
        {'tipo': 'flatrate', 'provider_name': 'Netflix'}
    ]
    generos = [
        {'tmdb_id': 80, 'nome': 'Crime'}
    ]

    with patch(
        'app.serviço.buscar_disponibilidades_do_filme_no_banco'
    ) as buscar_disponibilidades, patch(
        'app.serviço.buscar_generos_do_filme_no_banco'
    ) as buscar_generos:

        buscar_disponibilidades.return_value = disponibilidades
        buscar_generos.return_value = generos

        resultado = _completar_dados_filme_salvo(filme)

    buscar_disponibilidades.assert_called_once_with(filme)
    buscar_generos.assert_called_once_with(filme)

    assert resultado is filme
    assert filme.disponibilidade == disponibilidades
    assert filme.generos == generos

@pytest.mark.parametrize(
    ("status", "mensagem"),
    [
        ("atualizado", "Filme atualizado no banco com sucesso!"),
        ("já_existe", "Não houve mudança no banco!"),
        ("novo", "Filme salvo no banco com sucesso!"),
    ],
)
def test_salvar_filme_se_confirmado_exibe_mensagem(
    status, mensagem, capsys
):
    filme = Filme("The Batman", 2022)

    with patch("builtins.input", return_value="s"), patch(
        "app.serviço.salvar_filme",
        return_value={"status": status}
    ) as salvar:

        _salvar_filme_se_confirmado(filme)

    salvar.assert_called_once_with(filme)
    assert mensagem in capsys.readouterr().out

def test_nao_salvar_filme_se_nao_confirmado(capsys):
    filme = Filme("The Batman", 2022)

    with patch("builtins.input", return_value="n"), patch(
        "app.serviço.salvar_filme"
    ) as salvar:

        _salvar_filme_se_confirmado(filme)

    salvar.assert_not_called()
    assert "Filme não foi salvo." in capsys.readouterr().out

def test_cancelar_exclusao_filme(capsys):
    filme = Filme('The Batman', 2022)

    with patch(
        'app.serviço.buscar_filmes_banco',
        return_value=[filme]
    ), patch(
        'app.serviço.selecionar_filme',
        return_value=filme
    ), patch(
        'builtins.input',
        return_value='n'
    ), patch(
        'app.serviço.excluir_filme_banco'
    ) as excluir:

        excluir_filme_salvo()

    excluir.assert_not_called()
    assert 'A exclusão foi cancelada!' in capsys.readouterr().out

def test_confirmar_exclusao_filme(capsys):
    filme = Filme('The Batman', 2022)

    with patch(
        'app.serviço.buscar_filmes_banco',
        return_value=[filme]
    ), patch(
        'app.serviço.mostrar_resultado'
    ), patch(
        'app.serviço.selecionar_filme',
        return_value=filme
    ), patch(
        'builtins.input',
        return_value='s'
    ), patch(
        'app.serviço.excluir_filme_banco'
    ) as excluir:

        excluir_filme_salvo()

    excluir.assert_called_once_with(filme)
    assert 'Filme excluído com sucesso!' in capsys.readouterr().out

def test_cancelar_alteracao_favorito(capsys):
    filme = Filme('The Batman', 2022)

    with patch(
        'app.serviço.buscar_filmes_banco',
        return_value=[filme]
    ), patch(
        'app.serviço.mostrar_resultado'
    ), patch(
        'app.serviço.selecionar_filme',
        return_value=filme
    ), patch(
        'builtins.input',
        return_value='n'
    ), patch(
        'app.serviço.atualizar_favorito_banco'
    ) as atualizar:

        gerenciar_favoritos()

    atualizar.assert_not_called()
    assert 'O filme não foi alterado.' in capsys.readouterr().out

def test_confirmar_adicao_aos_favoritos(capsys):
    filme = Filme('The Batman', 2022)

    def simular_atualizacao(filme, favorito):
        filme.favorito = favorito

    with patch(
        'app.serviço.buscar_filmes_banco',
        return_value=[filme]
    ), patch(
        'app.serviço.mostrar_resultado'
    ), patch(
        'app.serviço.selecionar_filme',
        return_value=filme
    ), patch(
        'builtins.input',
        return_value='s'
    ), patch(
        'app.serviço.atualizar_favorito_banco',
        side_effect=simular_atualizacao
    ) as atualizar:

        gerenciar_favoritos()

    atualizar.assert_called_once_with(filme, True)
    assert filme.favorito is True
    assert (
        'Filme foi adicionado aos favoritos com sucesso!'
        in capsys.readouterr().out
    )

def test_confirmar_remocao_dos_favoritos(capsys):
    filme = Filme('The Batman', 2022, favorito=True)

    def simular_atualizacao(filme, favorito):
        filme.favorito = favorito

    with patch(
        'app.serviço.buscar_filmes_banco',
        return_value=[filme]
    ), patch(
        'app.serviço.mostrar_resultado'
    ), patch(
        'app.serviço.selecionar_filme',
        return_value=filme
    ), patch(
        'builtins.input',
        return_value='s'
    ), patch(
        'app.serviço.atualizar_favorito_banco',
        side_effect=simular_atualizacao
    ) as atualizar:

        gerenciar_favoritos()

    atualizar.assert_called_once_with(filme, False)
    assert filme.favorito is False
    assert (
        'Filme foi removido dos favoritos com sucesso!'
        in capsys.readouterr().out
    )

@patch('app.serviço.buscar_filme')
@patch('builtins.input', return_value='The Batman')
def test_buscar_filme_erro_timeout(mock_input, mock_buscar_filme, capsys):
    mock_buscar_filme.side_effect = ErroApi(
        'Erro',
        'Problema de tempo limite'
    )

    buscar_e_mostrar_filme()

    capturado = capsys.readouterr()

    assert (
        'A API demorou para responder. Tente novamente.'
        in capturado.out
    )
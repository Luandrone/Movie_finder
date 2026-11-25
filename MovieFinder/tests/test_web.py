from unittest.mock import patch

from fastapi.testclient import TestClient

from app.excecoes import ErroApi
from app.filme import Filme
from app.web import app, FilmeResumo, converter_filme_resumo

client = TestClient(app)


def test_verificar_saude():
    resposta = client.get("/health")

    assert resposta.status_code == 200
    assert resposta.json() == {
        "status": "ok",
        "aplicacao": "MovieFinder"
    }

@patch(
    "app.web.pesquisar_filmes_por_nome",
    return_value=[
        Filme("The Batman", "2022", 7.7, 414906),
        Filme("Batman Begins", "2005", 7.6, 272)
    ]
)
def test_rota_buscar_filmes(mock_pesquisar):
    resposta = client.get(
        "/filmes/buscar",
        params={"nome": "Batman"}
    )

    assert resposta.status_code == 200
    assert resposta.json() == [
        {
            "id": 414906,
            "titulo": "The Batman",
            "ano": "2022",
            "nota": 7.7
        },
        {
            "id": 272,
            "titulo": "Batman Begins",
            "ano": "2005",
            "nota": 7.6
        }
    ]

def test_rota_buscar_filmes_sem_nome():
    resposta = client.get("/filmes/buscar")

    assert resposta.status_code == 422

@patch("app.web.pesquisar_filmes_por_nome")
def test_buscar_filmes_chama_servico(mock_pesquisar):
    mock_pesquisar.return_value = [
        Filme("The Batman", "2022", 7.7, 414906)
    ]

    resposta = client.get(
        "/filmes/buscar",
        params={"nome": "The Batman"}
    )

    assert resposta.status_code == 200
    assert resposta.json() == [
        {
            "id": 414906,
            "titulo": "The Batman",
            "ano": "2022",
            "nota": 7.7
        }
    ]

    mock_pesquisar.assert_called_once_with("The Batman")

def test_modelo_filme_resumo():
    filme = FilmeResumo(
        id=414906,
        titulo="The Batman",
        ano="2022",
        nota=7.7
    )

    assert filme.id == 414906
    assert filme.titulo == "The Batman"
    assert filme.ano == "2022"
    assert filme.nota == 7.7

def test_converter_filme_resumo():
    filme = Filme("The Batman", 2022, 7.7, 414906)

    resultado = converter_filme_resumo(filme)

    assert resultado.id == 414906
    assert resultado.titulo == "The Batman"
    assert resultado.ano == "2022"
    assert resultado.nota == 7.7

def test_buscar_filmes_retorna_somente_campos_do_modelo():
    filme = Filme("The Batman", 2022, 7.7, 414906)

    dados_com_campo_extra = {
        "id": 414906,
        "titulo": "The Batman",
        "ano": "2022",
        "nota": 7.7,
        "sinopse": "Um vigilante protege Gotham."
    }

    with patch(
        "app.web.pesquisar_filmes_por_nome",
        return_value=[filme]
    ), patch(
        "app.web.converter_filme_resumo",
        return_value=dados_com_campo_extra
    ):

        resposta = client.get(
            "/filmes/buscar",
            params={"nome": "The Batman"}
        )

    assert resposta.status_code == 200

    assert resposta.json() == [
        {
            "id": 414906,
            "titulo": "The Batman",
            "ano": "2022",
            "nota": 7.7
        }
    ]

@patch("app.web.pesquisar_filmes_por_nome")
def test_buscar_filmes_timeout_retorna_504(mock_pesquisar):
        mock_pesquisar.side_effect = ErroApi(
            "Tempo limite",
            "Problema de tempo limite"
        )

        resposta = client.get(
            "/filmes/buscar",
            params={"nome": "The Batman"}
        )

        assert resposta.status_code == 504
        assert resposta.json() == {
            "detail": "O TMDB demorou para responder."
        }
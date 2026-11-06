from unittest.mock import patch

from fastapi.testclient import TestClient

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
    return_value=["filme1", "filme2", "filme3"]
)
def test_rota_buscar_filmes(mock_pesquisar):
    resposta = client.get(
        "/filmes/buscar",
        params={"nome": "The Batman"}
    )

    assert resposta.status_code == 200
    assert resposta.json() == {
        "quantidade_encontrada": 3
    }

def test_rota_buscar_filmes_sem_nome():
    resposta = client.get("/filmes/buscar")

    assert resposta.status_code == 422

@patch("app.web.pesquisar_filmes_por_nome")
def test_buscar_filmes_chama_servico(mock_pesquisar):
    mock_pesquisar.return_value = ["filme1", "filme2"]

    resposta = client.get(
        "/filmes/buscar",
        params={"nome": "The Batman"}
    )

    assert resposta.status_code == 200
    assert resposta.json() == {
        "quantidade_encontrada": 2
    }

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
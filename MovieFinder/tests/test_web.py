from unittest.mock import patch

from fastapi.testclient import TestClient
from app.web import app


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